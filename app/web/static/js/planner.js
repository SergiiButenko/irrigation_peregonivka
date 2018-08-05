var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
var API_ENDPOINT = '/api/v1'

var branch = [];
var json = { 'lines': {} };

$(document).ready(function() {
    $(".card-block, .card-footer").on('click', function(event) {
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
    });

    $("#next").click(function() {
        json = { 'lines': {} };
        var at_least_one = false;

        $(".card").each(function() {
            var selected = $(this).hasClass('card-selected');
            var id = $(this).data('line_id');
            if (selected == true) {
                json['lines'][id] = { 'id': id };
                at_least_one = true;
            }
        });

        if (at_least_one == false) {
            alert("Виберіть хоча б одну лінію. Дякую.");
            return;
        }

        $('#plan_modal').modal('show');
    });

    $('.master_plan').click(function() {
        json['timer'] = parseInt($("#select_line option:selected").val());

        $.ajax({
            url: API_ENDPOINT + '/plan',
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