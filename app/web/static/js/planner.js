var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');
var API_ENDPOINT = '/api/v1'

var branch = [];
var planner_lines = { 'lines': {} };

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
        planner_lines = { 'lines': {} };
        var at_least_one = false;

        $(".card").each(function() {
            var selected = $(this).hasClass('card-selected');
            var id = $(this).data('line_id');
            if (selected == true) {
                planner_lines['lines'][id] = { 'id': id };
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
});