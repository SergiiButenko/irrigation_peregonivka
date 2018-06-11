var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
var branch = [];
var json = { 'lines': {} };

$(document).ready(function() {
    $(".select").click(function(event) {
        var card = $(event.target).closest(".card");
        card.toggleClass("card-selected");
    });


    $("#next").click(function() {
        json = { 'lines': {} }

        $(".card").each(function() {
            var selected = $(this).hasClass('card-selected');
            var id = $(this).data('line_id');
            if (selected == true) {
                json['lines'][id] = { 'id': id }
            }
        });

        $('#plan_modal').modal('show');
    });

    $('.plan').click(function() {
        json['timer'] = parseInt($("#select_line option:selected").val());

        $.ajax({
            url: server + '/plan',
            type: "post",
            data: JSON.stringify(json),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            beforeSend: function(xhr, opts) {
                set_status_spinner();
            },
            success: function(data) {
                set_status_ok();
            },
            error: function() {
                alert("Сталася помилка. Спробуйте ще.")
                set_status_ok();
            }
        });
    });
});