var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');

var arduino_check_connect_sec = 60 * 5;
var arduino_check_broken_connect_sec = 60;

var branch = [];
var settings = {};

$(document).ready(function() {

    //Rename branches
    $.ajax({
        url: '/greenhouse_settings',
        success: function(data) {
            list = data['list']
            for (j in list) {
                item = list[j]
                branch[item['id']] = {
                    'name': item['name'],
                    'default_time': parseInt(item['default_time'])
                }
            }
        }
    });


    $.ajax({
        url: '/app_settings',
        success: function(data) {
            settings = data['data']
        }
    });


    (function worker2() {
        $.ajax({
            url: '/greenhouse_status',
            beforeSend: function(xhr, opts) {
                set_status_spinner();

                if ($('#greenhouse_modal').hasClass('in')) {
                    xhr.abort();
                }
            },
            success: function(data) {
                console.log("connected to raspberry");

                update_branches(data);

                set_status_ok();
                setTimeout(worker2, arduino_check_connect_sec * 1000);
            },
            error: function() {
                console.error("Can't connect to raspberry");

                set_status_error();
                setTimeout(worker2, arduino_check_broken_connect_sec * 1000);
            }
        });
    })();

    var socket = io.connect(server, {
        'sync disconnect on unload': true
    });
    socket.on('connect', function() {
        console.log("connected to websocket");
    });

    socket.on('branch_status', function(msg) {
        console.log('Message received. New brach status: ' + msg.data);
        update_branches(JSON.parse(msg.data));
    });


    // http://rosskevin.github.io/bootstrap-material-design/components/card/

    $('#greenhouse_modal').on('hidden.bs.modal', function() {
        update_branches_request();
    })

    $(".btn-open-modal").click(function() {
        index = $(this).data('id');
        name = branch[index]['name'];
        time = branch[index]['default_time'];

        $('#greenhouse_minutes').val(time);
        $('#greenhouse_modal').data('id', index);

        $('.modal-title').html(name);
        $('#greenhouse_modal').modal('show');
    });

    //Function to start greenhouse
    $(".start-greenhouse").click(function() {
        index = $('#greenhouse_modal').data('id');
        time = parseInt($("#greenhouse_minutes").val());
        if (time == 0 || isNaN(time)) {
            $('#greenhouse_minutes_group').addClass("has-danger");
        } else {
            $('#greenhouse_minutes_group').removeClass("has-danger");
        }


        if ($('#greenhouse_minutes_group').hasClass("has-danger")) {
            console.log("Fill in form correctly");
        } else {
            console.log(branch[index]['name'] + " will be activated on " + time + " minutes ");
            branch_on(index, time);
            $('#greenhouse_modal').modal('hide');
        }
    });

    $(".btn-start").click(function() {
        index = $(this).data('id');
        console.log(branch[index]['name'] + " will be activated on " + branch[index]['default_time'] + " minutes ");
        branch_on(index, branch[index]['default_time']);
    });

    //Function to stop greenhouse
    $(".stop-greenhouse").click(function() {
        index = $(this).data('id');
        console.log(branch[index]['name'] + " will be deactivated now");
        branch_off(index);
    });


    //Function to change settings
    $(".setup_greenhouse").click(function() {
        $('#greenhouse_min_temp').val(settings['temp_min_max']['min']);
        $('#greenhouse_max_temp').val(settings['temp_min_max']['max']);

        $('#greenhouse_settings_modal').modal('show');
    });

    $(".save-greenhouse_settings").click(function() {
        var min = $('#greenhouse_min_temp').val();
        var max = $('#greenhouse_max_temp').val();

        console.log("MIN:" + min + "; MAX:" + max);
        var json = {
            'list': { 'temp_min_max': { 'min': min, 'max': max } }
        }
        $.ajax({
            url: '/set_settings',
            type: "post",
            data: JSON.stringify(json),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                $('#greenhouse_settings_modal').modal('hide');
            }
        });
        
    });



});

function branch_on(index, time_minutes) {
    $.ajax({
        url: '/activate_branch',
        type: "get",
        data: {
            'id': index,
            'time_min': time_minutes,
            'mode': 'single'
        },
        success: function(data) {
            console.log('Line ' + branch[index]['name'] + ' should be actived now');
            update_branches(data);
        },
        error: function() {
            console.error("Can't update " + branch[index]['name']);
            toogle_card(index, 0);

            set_status_error();
        }
    });
}

function branch_off(index) {
    $.ajax({
        url: '/deactivate_branch',
        type: "get",
        data: {
            'id': index,
            'mode': 'manually'
        },
        success: function(data) {
            console.log('Line ' + branch[index]['name'] + ' should be deactivated now');
            update_branches(data);
        },
        error: function() {
            console.error("Can't update " + branch[index]['name']);
            toogle_card(index, 1);
            set_status_error();
        }
    });
}

function update_branches_request() {
    $.ajax({
        url: '/greenhouse_status',
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

    for (key in arr) {
        toogle_card(key, arr[key]);
    }
}

function toogle_card(element_id, branch) {
    if (branch == null)
        return;

    branch_state = branch['status']
    if (branch_state == 1) {
        $('#card-' + element_id).addClass("card-irrigate-active");
        $('#btn-start-' + element_id).hide().addClass("hidden");
        $('#btn-start-with-options-' + element_id).hide().addClass("hidden");
        $('#btn-stop-' + element_id).css('display', 'inline-block').removeClass("hidden");
    } else {
        $('#card-' + element_id).removeClass("card-irrigate-active");
        $('#btn-stop-' + element_id).hide().addClass("hidden");
        $('#btn-start-' + element_id).css('display', 'inline-block').removeClass("hidden");
        $('#btn-start-with-options-' + element_id).css('display', 'inline-block').removeClass("hidden");
    }

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
    $('#last-' + element_id).html("Останнє включення: " + last_rule)

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
        $('#next-' + element_id).html("Наступне включення: " + next_rule);

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
        $('#next-' + element_id).html("Вимкнеться: " + next_rule);
        $('#btn-cancel-' + element_id).hide().addClass("hidden");
    } else {
        $('#next-' + element_id).html("</br>Наступне включення: немає запису");
        $('#next-' + element_id).hide().addClass("hidden");
        $('#btn-cancel-' + element_id).hide().addClass("hidden");
    }
}