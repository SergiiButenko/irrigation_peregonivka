var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
var API_ENDPOINT = '/api/v1'

$(document).ready(function() {
    var socket = io.connect(server, {
        'sync disconnect on unload': true,
        'secure': true,
        cors: {
            origin: server,
            methods: ["GET", "POST"]
          }
    });


    socket.on('disconnect', function(data) {
        console.log("sockets disconnect!");
    });

    socket.on('connect', function() {
        console.log("connected to websocket");
    });

    socket.on('refresh_history', function(msg) {
        console.log('Reload received');
        reload_history();
    });

    $(".card-rule").each(function() {
        form_text($(this))
    });
    set_events();
});


function form_text(el_in) {
    var card = $(el_in).closest('.top');

    var time = convertDateToUTC(new Date($(card).data('timer')));
    var minutes = $(card).data('time');
    var interval = $(card).data('intervals');
    var time_wait = $(card).data('time_wait');

    var options_time = {
        hour: "2-digit",
        minute: "2-digit"
    };

    $(card).find("#summary").html(
        'O ' + time.toLocaleTimeString("uk-UA", options_time) + ', ' +
        interval + ' рази, по ' + minutes + ' хвилин, з інтервалом в ' + time_wait + ' хвилин'
    );
}


function set_events() {
    $('.close').off().click(function(e) {
        var returnVal = confirm("Видалити правило?");
        if (returnVal == false) {
            return;
        }

        var schedule_card = $(e.target).closest('.top');
        interval_id = $(schedule_card).data('interval_id');

        $.ajax({
            url: API_ENDPOINT + '/cancel_rule',
            type: "post",
            data: JSON.stringify({ 'list': [interval_id] }),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            beforeSend: function(xhr, opts) {
                set_status_spinner();
            },
            error: function(data) {
                alert("Сталася помилка. Cпробуйте ще раз");
            }
        });
    });

    $('.disable-all').off().click(function(e) {
        var returnVal = confirm("Вiдмiнити усi правила на цей день?");
        if (returnVal == false) {
            return;
        }

        var schedule_cards = $(e.target).closest('.rule-container').find('.top');
        var list = { 'list': [] }
        $(schedule_cards).each(function() {
            list.list.push($(this).data('interval_id'))
        });

        $.ajax({
            url: API_ENDPOINT + '/cancel_rule',
            type: "post",
            data: JSON.stringify(list),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            beforeSend: function(xhr, opts) {
                set_status_spinner();
            },
            error: function(data) {
                alert("Сталася помилка. Cпробуйте ще раз");
            }
        });
    });
}