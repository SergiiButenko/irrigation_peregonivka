var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');

$(document).ready(function() {
    //Add arduino touch script to determine if connection is alive

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



    (function() {
        state = $("#all_rules").is(":checked")
        $('#rules_table tr td:nth-child(2)').each(function() {
            if (($(this).text().indexOf("Остановить") != -1 || $(this).text().indexOf("Зупинити") != -1) & !state)
                $(this).closest("tr").hide();

            if (($(this).text().indexOf("Остановить") != -1 || $(this).text().indexOf("Зупинити") != -1) & state)
                $(this).closest("tr").show();
        });
    })();

    $(".btn-refresh-history").click(function() {
        $.ajax({
            url: '/list_all',
            type: "get",
            data: {
                'days': $(this).data('value'),
            },
            success: function(data) {
                $('#rules_table').html(data);
            }
        });
    });

    $("#all_rules").change(function() {
        state = $("#all_rules").is(":checked")
        $('#rules_table tr td:nth-child(2)').each(function() {
            if (($(this).text().indexOf("Остановить") != -1 || $(this).text().indexOf("Зупинити") != -1) & !state)
                $(this).closest("tr").hide();

            if (($(this).text().indexOf("Остановить") != -1 || $(this).text().indexOf("Зупинити") != -1) & state)
                $(this).closest("tr").show();
        });
    });
});


function cancel_rule(that) {
    index = $(that).data('id');
    console.log(index + " irrigation schedule will be canceled");

    $.ajax({
        url: server + '/cancel_rule',
        type: "get",
        data: {
            'id': index
        },
        success: function(data) {
            console.log('Line ' + index + ' wont be started');
        },
        error: function() {
            console.error("Can't cancel next rule for " + index);
        }
    });
}