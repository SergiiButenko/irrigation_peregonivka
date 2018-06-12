var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
var branch = [];
var json = { 'lines': {} };

$(document).ready(function() {
    $(".card-block, .card-footer").on('click', toogle_selected(event));
    $(".select, .deselect").on('click', toogle_selected(event));

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

    $('.master_plan').click(function() {
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
                $('#plan_modal').modal('hide');
                window.location.replace("/ongoing_rules");
            },
            error: function() {
                alert("Сталася помилка. Спробуйте ще.")
                set_status_ok();
                $('#plan_modal').modal('hide');
            }
        });
    });
});



function toogle_selected(event) {
    var card = $(event.target).closest(".card");
    if (card.hasClass("card-selected")) {
        card.removeClass("card-selected");
        card.find(".deselect").hide().addClass("hidden");
        card.find(".select").css('display', 'inline-block').removeClass("hidden");
    } else {
        card.addClass("card-selected");
        card.find(".select").hide().addClass("hidden");
        card.find(".deselect").css('display', 'inline-block').removeClass("hidden");
    }
}