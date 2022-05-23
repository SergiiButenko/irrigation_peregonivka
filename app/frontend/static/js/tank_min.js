var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
var API_ENDPOINT = '/api/v1'

var arduino_check_connect_sec = 60 * 5;
var arduino_check_broken_connect_sec = 60;

var branch = [];
var devices = {};

$(document).ready(function() {
    var socket = io.connect(server, {
        'sync disconnect on unload': true,
        'secure': true,
        cors: {
            origin: server,
            methods: ["GET", "POST"]
          }
    });
    
    socket.on('connect', function() {
        console.log("connected to websocket");
    });

    socket.on('disconnect', function(data) {
        console.log("sockets disconnect!");
    });

    socket.on('branch_status', function(msg) {
        console.log('Message received. New brach status: ' + msg.data);
        update_branches(JSON.parse(msg.data));
    });


    //Rename branches
    $.ajax({
        url: API_ENDPOINT + '/tank_settings',
        success: function(data) {
            list = data['list']
            for (j in list) {
                item = list[j]
                branch[item['id']] = {
                    'name': item['name'],
                    'default_time': parseInt(item['default_time']),
                    'start_time': new Date(item['start_time'])
                }
            }
        }
    });


    

    (function worker2() {
        $.ajax({
            url: API_ENDPOINT + '/tank_status',
            beforeSend: function(xhr, opts) {
                set_status_spinner();

                if ($('#tank_modal').hasClass('in')) {
                    xhr.abort();
                }
            },
            success: function(data) {
                console.log("connected to raspberry");

                update_branches(data);
                update_devices_request();

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

    // http://rosskevin.github.io/bootstrap-material-design/components/card/

    $('#tank_modal').on('hidden.bs.modal', function() {
        update_branches_request();
    })

    $(".btn-open-modal").click(function() {
        index = $(this).data('id');
        name = branch[index]['name'];
        time = branch[index]['default_time'];
        start_time = branch[index]['start_time']

        $('#tank_minutes').val(time);
        $('#tank_modal').data('id', index);

        $('.modal-title').html(name);

        var tomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
        irrigation_date = $('#tank_modal').find('.irrigation_date');
        $(irrigation_date).val(convert_date(tomorrow));        

        irrigation_time = $('#tank_modal').find('.irrigation_time');
        $(irrigation_time).val(convert_date_to_time(start_time));
        $('#tank_modal').modal('show');
    });

    //Function to start tank
    $(".start-tank").click(function() {
        index = $('#tank_modal').data('id');
        time = parseInt($("#tank_minutes").val());
        if (time == 0 || isNaN(time)) {
            $('#tank_minutes_group').addClass("has-danger");
        } else {
            $('#tank_minutes_group').removeClass("has-danger");
        }


        if ($('#tank_minutes_group').hasClass("has-danger")) {
            console.log("Fill in form correctly");
        } else {
            var json = { 'rules': [] }
            var branch_id = index;
            var name = branch[branch_id]['name'];
            var time = time;
            var interval = 1;
            var time_wait = 0;
            var date_start = $('#tank_modal').find('.irrigation_date').val();
            var time_start = $('#tank_modal').find('.irrigation_time').val();
            json['rules'].push({
                "line_id": branch_id,
                'line_name': name,
                "time": time,
                "intervals": interval,
                "time_wait": time_wait,
                "date_start": date_start,
                'time_start': time_start,
                'end_date': date_start,
                'repeat_value': 4
            });

            console.log(json)
            $.ajax({
                url: API_ENDPOINT + '/add_ongoing_rule',
                type: "post",
                data: JSON.stringify(json),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                beforeSend: function(xhr, opts) {
                    set_status_spinner();
                },
                success: function() {
                    $('#tank_modal').modal('hide');
                    set_status_ok();
                },
                error: function() {
                    alert("Помилка. Перевірте з'єднання і спробуйте ще раз");
                    set_status_ok();
                }
            });
        }
    });

    $(".btn-start").click(function() {
        index = $(this).data('id');
        console.log(branch[index]['name'] + " will be activated on " + branch[index]['default_time'] + " minutes ");
        branch_on(index, branch[index]['default_time']);
    });

    //Function to stop tank
    $(".stop-tank").click(function() {
        index = $(this).data('id');
        console.log(branch[index]['name'] + " will be deactivated now");
        branch_off(index);
    });


    $(".cancel-filling").click(function() {
        var interval_id = $(this).data('id');
        console.log(interval_id + " filling schedule will be canceled");

        $.ajax({
            url: API_ENDPOINT + '/cancel_rule',
            type: "post",
            data: JSON.stringify({ 'list': [interval_id] }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            beforeSend: function(xhr, opts) {
                set_status_spinner();
            },
            success: function(data) {
                set_status_ok();
            },
            error: function() {
                set_status_ok();
            }
        });
    });
});

function branch_on(index, time_minutes) {
    $.ajax({
        url: API_ENDPOINT + '/activate_branch',
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
        url: API_ENDPOINT + '/deactivate_branch',
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
        url: API_ENDPOINT + '/tank_status',
        success: function(data) {
            update_branches(data);
        },
        error: function() {
            console.error("Branches statuses are out-of-date");
            set_status_error();
        }
    });
}

function update_devices_request() {
    //Check devices
    $.ajax({
        url: API_ENDPOINT + '/linked_device_status',
            success: function(data) {
                devices = data['devices']
                update_devices(data);
            },
            error: function() {
                set_device_error();
            }});
}

function update_devices(json) {
    arr = json['devices']
    console.log(arr)
    for (key in arr) {
        toogle_device_for_card(key, arr[key]);
        console.log(arr[key])
    }    
}

function toogle_device_for_card(element_id, device) {
    device_state = device['device_state']
    if (device_state == 1) {
        $('#device-error-' + element_id).hide().addClass("hidden");
        $('#device-ok-' + element_id).css('display', 'inline-block').removeClass("hidden");
    } else {
        $('#device-ok-' + element_id).hide().addClass("hidden");
        $('#device-error-' + element_id).css('display', 'inline-block').removeClass("hidden");
    }
}

function set_device_error() {
    $("[id^=device-ok]").hide().addClass("hidden");
    $("[id^=device-error]").css('display', 'inline-block').removeClass("hidden");
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
    $('#last-' + element_id).html("Останнє наповнення: " + last_rule)

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
        $('#next-' + element_id).html("Наступне наповнення: " + next_rule);

        $('#btn-cancel-' + element_id).data('id', branch['next_rule']['interval_id'])
        $('#btn-start-with-options-' + element_id).hide().addClass("hidden");
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
        $('#next-' + element_id).html("Заповнення вимкнеться: " + next_rule);
        $('#btn-cancel-' + element_id).hide().addClass("hidden");
    } else {
        $('#next-' + element_id).html("</br>Наступне заповнення: немає запису");
        $('#next-' + element_id).hide().addClass("hidden");
        $('#btn-cancel-' + element_id).hide().addClass("hidden");
        $('#btn-start-with-options-' + element_id).css('display', 'inline-block').removeClass("hidden");
    }
}