var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
var API_ENDPOINT = '/api/v1'

var branch = [];
var planner_lines = { 'lines': {} };

$(document).ready(function() {
    $.ajax({
        url: API_ENDPOINT + '/branch_settings',
        success: function(data) {
            list = data['list']
            for (j in list) {
                item = list[j]
                branch[item['id']] = {
                    'name': item['name'],
                    'default_time': parseInt(item['default_time']),
                    'default_interval': parseInt(item['default_interval']),
                    'default_time_wait': parseInt(item['default_time_wait']),
                    'start_time': new Date(item['start_time']),
                    'is_pump': parseInt(item['is_pump'])
                }
            }
        }
    });

    $(".card-footer").on('click', function(event) {
        var card = $(event.target).closest(".card");

        toogle_card_state(card);
    });

    $(".card-block").on('dblclick', function(event) {
        var card = $(event.target).closest(".card");

        toogle_card_state(card);
    });

    $('.more-water').on('click', function(event) {        
        var card = $(event.target).closest('.card');
        var footer = $(card).find('.card-footer');
        var more_water = $(card).find('.more-water')
        var more_water_mode = $(card).data('more-water');

        if (card.hasClass("card-selected") == false) {
            card.addClass("card-selected");
            footer.addClass("footer-selected");
            card.find(".select").hide().addClass("hidden");
            card.find(".deselect").css('display', 'inline-block').removeClass("hidden");
        }

        var time = parseInt($(card).find('.irrigation_minutes').val());
        if (more_water_mode == 1) {
            $(card).find('.irrigation_minutes').val(time - 5);
            more_water.addClass('greyout');
            $(card).data('more-water', 0)
        } else {
            $(card).find('.irrigation_minutes').val(time + 5);
            more_water.removeClass('greyout');
            $(card).data('more-water', 1)
        }
    });


    $("#next").click(function() {
        planner_lines = { 'lines': {} };
        var at_least_one = false;

        $(".card").each(function() {
            var selected = $(this).hasClass('card-selected');
            console.log(selected == true);
            var id = $(this).data('line_id');
            var time = $(this).find('.irrigation_minutes').val();
            var intervals = $(this).find('.irrigation_intervals').val();
            var time_wait = $(this).find('.irrigation_time_wait').val();
            if (selected == true) {
                planner_lines['lines'][id] = {
                    'id': id,
                    'time': time,
                    'intervals': intervals,
                    'time_wait': time_wait
                };
                at_least_one = true;
            }
        });

        if (at_least_one == false) {
            alert("Виберіть хоча б одну лінію. Дякую.");
            return;
        }

        $('#plan_modal').data('lines', JSON.stringify(planner_lines));
        $('#plan_modal').modal('show');
    });

    update_branches_request();
});

function update_branches_request() {
    $.ajax({
        url: API_ENDPOINT + '/irrigation_status',
        success: function(data) {
            update_branches(data);
        },
        error: function() {
            console.error("Branches statuses are out-of-date");
            set_status_error();
        }
    });
}

function update_branches(json) {
    arr = json['branches'];
    branch_status = arr;

    for (key in arr) {
        toogle_card(key, arr[key]);
    }
}

function toogle_card(element_id, branch) {
    if (branch == null)
        return;

    var options_datetime = {
        weekday: "long",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    };

    var options_time = {
        hour: "2-digit",
        minute: "2-digit"
    };

    var now = new Date();
    if (branch['last_rule']) {
        last_rule = convertDateToUTC(new Date(branch['last_rule']['timer']))
        if (daydiff(now, last_rule) == 0) {
            last_rule = "сьогодні, о " + last_rule.toLocaleTimeString("uk-UA", options_time);
        } else if (daydiff(now, last_rule) == -1) {
            last_rule = "вчора, о " + last_rule.toLocaleTimeString("uk-UA", options_time);
        } else {
            last_rule = last_rule.toLocaleTimeString("uk-UA", options_datetime);
        }
    } else {
        last_rule = "немає запису"
    }
    $('#last-' + element_id).html("Останній полив: " + last_rule)

    if (branch['next_rule'] && branch['next_rule']['rule_id'] == 1) {
        next_rule = convertDateToUTC(new Date(branch['next_rule']['timer']))
        if (daydiff(now, next_rule) == 0) {
            next_rule = "сьогодні, о " + next_rule.toLocaleTimeString("uk-UA", options_time);
        } else if (daydiff(now, next_rule) == 1) {
            next_rule = "завтра, о " + next_rule.toLocaleTimeString("uk-UA", options_time);
        } else if (daydiff(now, next_rule) == 2) {
            next_rule = "післязавтра, о " + next_rule.toLocaleTimeString("uk-UA", options_time);
        } else {
            next_rule = next_rule.toLocaleTimeString("uk-UA", options_datetime);
        }

        $('#next-' + element_id).css('display', 'inline-block').removeClass("hidden");
        $('#next-' + element_id).html("Наступний полив: " + next_rule);

        $('#btn-cancel-' + element_id).data('id', branch['next_rule']['interval_id'])
        $('#btn-cancel-' + element_id).css('display', 'inline-block').removeClass("hidden");

    } else if (branch['next_rule'] && branch['next_rule']['rule_id'] == 2) {
        next_rule = convertDateToUTC(new Date(branch['next_rule']['timer']))
        if (daydiff(now, next_rule) == 0) {
            next_rule = "сьогодні, о " + next_rule.toLocaleTimeString("uk-UA", options_time);
        } else if (daydiff(now, next_rule) == 1) {
            next_rule = "завтра, о " + next_rule.toLocaleTimeString("uk-UA", options_time);
        } else if (daydiff(now, next_rule) == 2) {
            next_rule = "післязавтра, о " + next_rule.toLocaleTimeString("uk-UA", options_time);
        } else {
            next_rule = next_rule.toLocaleTimeString("uk-UA", options_datetime);
        }

        $('#next-' + element_id).css('display', 'inline-block').removeClass("hidden");
        $('#next-' + element_id).html("Полив зупиниться: " + next_rule);
        $('#btn-cancel-' + element_id).hide().addClass("hidden");
    } else {
        $('#next-' + element_id).html("</br>Наступний полив: немає запису");
        $('#next-' + element_id).hide().addClass("hidden");
        $('#btn-cancel-' + element_id).hide().addClass("hidden");
    }
}

function toogle_card_state(card) {
    var footer = $(card).find('.card-footer');
    var more_water = $(card).find('.more-water')
    var more_water_mode = $(card).data('more-water');
    
    if (card.hasClass("card-selected")) {
        card.removeClass("card-selected");
        footer.removeClass("footer-selected");
        card.find(".deselect").hide().addClass("hidden");
        card.find(".select").css('display', 'inline-block').removeClass("hidden");
        

        var time = parseInt($(card).find('.irrigation_minutes').val());
        if (more_water_mode == 1) {
            $(card).find('.irrigation_minutes').val(time - 5);
            more_water.addClass('greyout');
            $(card).data('more-water', 0)
        }

    } else {
        card.addClass("card-selected");
        footer.addClass("footer-selected");
        card.find(".select").hide().addClass("hidden");
        card.find(".deselect").css('display', 'inline-block').removeClass("hidden");
    }
}