var server = location.protocol + '//' + location.hostname + (location.port ? ':' + location.port : '');

var arduino_check_connect_sec = 60 * 5;
var arduino_check_broken_connect_sec = 60;

var branch = [];
var settings = {};

$(document).ready(function() {
    var socket = io.connect(server, {
        'sync disconnect on unload': true,
        'secure': true
    });

    socket.on('disconnect', function(data) {
        console.log("sockets disconnect!");
    });

    socket.on('connect', function() {
        console.log("connected to websocket");
    });

    socket.on('branch_status', function(msg) {
        console.log('Message received. New brach status: ' + msg.data);
        update_branches(JSON.parse(msg.data));
    });


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
            settings = data['data'];
            console.log(settings);
            toggle_buttons();
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

                set_status_ok();
                update_branches(data);
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
        if (settings['greenhouse_auto']['enabled'] == "1") {
            var returnVal = confirm("Автоматичне керування увімкнено. \nВимкнути і перейти до ручного керування?");
            if (returnVal == false)
                return;

            var json = {
                'list': { 'greenhouse_auto': { 'enabled': '0' } }
            }
            $.ajax({
                url: '/set_settings',
                type: "post",
                data: JSON.stringify(json),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(data) {
                    settings = data['data'];
                    console.log(settings);
                    toggle_buttons();
                },
            error: function(data) {
                console.error("Can't save settings");
                console.error(data);
                alert("Сталася помилка при збереженні параметрів. Спробуйте ще раз.")
            }
            });
        }


        index = $(this).data('id');
        console.log(branch[index]['name'] + " will be activated on " + branch[index]['default_time'] + " minutes ");
        branch_on(index, branch[index]['default_time']);
    });

    //Function to stop greenhouse
    $(".stop-greenhouse").click(function() {
        if (settings['greenhouse_auto']['enabled'] == "1") {
            var returnVal = confirm("Автоматичне керування увімкнено. \nВимкнути і перейти до ручного керування?");
            if (returnVal == false)
                return;

            var json = {
                'list': { 'greenhouse_auto': { 'enabled': '0' } }
            }
            $.ajax({
                url: '/set_settings',
                type: "post",
                data: JSON.stringify(json),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(data) {
                    settings = data['data'];
                    console.log(settings);
                    toggle_buttons();
                },
                error: function(data) {
                    console.error("Can't save settings");
                    console.error(data);
                    alert("Сталася помилка при збереженні параметрів. Спробуйте ще раз.")
                }
            });
        }

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
                settings = data['data'];
                console.log(settings);
                $('#greenhouse_settings_modal').modal('hide');
            },
            error: function(data) {
                console.error("Can't save settings");
                console.error(data);
                $('#greenhouse_settings_modal').modal('hide');
                alert("Сталася помилка при збереженні параметрів. Спробуйте ще раз.")
            }
        });

    });


    $(".greenhouse_auto_enable").click(function() {
        var returnVal = confirm("Увімкнути автоматичне керування?");
        if (returnVal == false)
            return;

        var json = {
            'list': { 'greenhouse_auto': { 'enabled': '1' } }
        }
        $.ajax({
            url: '/set_settings',
            type: "post",
            data: JSON.stringify(json),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                settings = data['data'];
                console.log(settings);
                toggle_buttons();
                alert("Aвтоматичне керування увімкнено");
            },
            error: function(data) {
                console.error("Can't save settings");
                console.error(data);
                alert("Сталася помилка при збереженні параметрів. Спробуйте ще раз.")
            }
        });

    });

    $(".greenhouse_auto_disable").click(function() {
        var returnVal = confirm("Вимкнути автоматичне керування?");
        if (returnVal == false)
            return;

        var json = {
            'list': { 'greenhouse_auto': { 'enabled': '0' } }
        }
        $.ajax({
            url: '/set_settings',
            type: "post",
            data: JSON.stringify(json),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data) {
                settings = data['data'];
                console.log(settings);
                toggle_buttons();
                alert("Aвтоматичне керування вимкнено");
            },
            error: function(data) {
                console.error("Can't save settings");
                console.error(data);
                alert("Сталася помилка при збереженні параметрів. Спробуйте ще раз.")
            }
        });
    });
});


function toggle_buttons() {
    if (settings['greenhouse_auto']['enabled'] == "1") {
        $('.greenhouse_auto_enable').hide().addClass("hidden");
        $('.greenhouse_auto_disable').css('display', 'inline-block').removeClass("hidden");
        $('#automode_header').text('Aвтоматичне керування увімкнено')
    }

    if (settings['greenhouse_auto']['enabled'] == "0") {
        $('.greenhouse_auto_disable').hide().addClass("hidden");
        $('.greenhouse_auto_enable').css('display', 'inline-block').removeClass("hidden");
        $('#automode_header').text('Aвтоматичне керування вимкнено')
    }
}


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
        // $('#card-' + element_id).addClass("card-irrigate-active");
        // $('#btn-start-' + element_id).hide().addClass("hidden");
        // $('#btn-start-with-options-' + element_id).hide().addClass("hidden");
        // $('#btn-stop-' + element_id).css('display', 'inline-block').removeClass("hidden");

        $('#card-' + element_id).removeClass("status-error");
        $('#card-' + element_id).addClass("card-irrigate-active");


        $('#btn-start-' + element_id).hide().addClass("hidden");
        $('#btn-start-with-options-' + element_id).hide().addClass("hidden");
        $('#btn-stop-' + element_id).css('display', 'inline-block').removeClass("hidden");
        $('#card-' + element_id + ' > div.card-footer > span').hide().addClass("hidden");
    }

    if (branch_state == 0) {
        // $('#card-' + element_id).removeClass("card-irrigate-active");
        // $('#btn-stop-' + element_id).hide().addClass("hidden");
        // $('#btn-start-' + element_id).css('display', 'inline-block').removeClass("hidden");
        // $('#btn-start-with-options-' + element_id).css('display', 'inline-block').removeClass("hidden");
        $('#card-' + element_id).removeClass("status-error");
        $('#card-' + element_id).removeClass("card-irrigate-active");

        $('#btn-stop-' + element_id).hide().addClass("hidden");
        $('#btn-start-' + element_id).css('display', 'inline-block').removeClass("hidden");
        $('#btn-start-with-options-' + element_id).css('display', 'inline-block').removeClass("hidden");
        $('#card-' + element_id + ' > div.card-footer > span').hide().addClass("hidden");
    }

    if (branch_state == -1) {
        // $('#card-' + element_id).removeClass("card-irrigate-active");
        // $('#btn-stop-' + element_id).hide().addClass("hidden");
        // $('#btn-start-' + element_id).css('display', 'inline-block').removeClass("hidden");
        // $('#btn-start-with-options-' + element_id).css('display', 'inline-block').removeClass("hidden");
        $('#card-' + element_id).removeClass("card-irrigate-active");
        $('#card-' + element_id).addClass("status-error");
        $('#btn-stop-' + element_id).hide().addClass("hidden");
        $('#btn-start-' + element_id).hide().addClass("hidden");
        $('#btn-start-with-options-' + element_id).hide().addClass("hidden");
        $('#card-' + element_id + ' > div.card-footer > span').css('display', 'inline-block').removeClass("hidden");
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


function draw_d3js(data) {
    var dataset = []
    console.log(data);
    var hours = []
    for (hour in data) {
        hours.push(hour + "");
        dataset.push(data[hour]);
    }
    console.log(dataset);


    var parent_el = $('#greenhouse_chart');

    // 2. Use the margin convention practice 
    var margin = { top: 20, right: 20, bottom: 20, left: 50 },
        width = parent_el.width() - margin.left - margin.right // Use the window's width 
        ,
        height = 250 - margin.top - margin.bottom; // Use the window's height

    // 5. X scale will use the index of our data
    var xScale = d3.scalePoint()
        .domain([dataset[0], dataset[dataset.length - 1]]) // input
        .rangeRound([0, width]); // output

    // 6. Y scale will use the randomly generate number 
    var yScale = d3.scaleLinear()
        .domain([
            0,
            d3.max(dataset, function(c) { return c.temp_air })
        ]) // input 
        .range([height, 0]); // output 

    // 7. d3's line generator
    var line_air = d3.line()
        .x(function(d) { return xScale(d.hour); }) // set the x values for the line generator
        .y(function(d) { return yScale(d.temp_air); }) // set the y values for the line generator 
        .curve(d3.curveMonotoneX) // apply smoothing to the line

    // var line_hum = d3.line()
    //     .x(function(d) { return xScale(d.hour); }) // set the x values for the line generator
    //     .y(function(d) { return yScale(d.hum_air); }) // set the y values for the line generator 
    //     .curve(d3.curveMonotoneX) // apply smoothing to the line

    var line_out = d3.line()
        .x(function(d) { return xScale(d.hour); }) // set the x values for the line generator
        .y(function(d) { return yScale(d.temp_out); }) // set the y values for the line generator 
        .curve(d3.curveMonotoneX) // apply smoothing to the line



    xScale.domain(hours.sort());

    // 1. Add the SVG to the page and employ #2
    var svg = d3.select('#greenhouse_chart').append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // 3. Call the x axis in a group tag
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(xScale)); // Create an axis component with d3.axisBottom

    // 4. Call the y axis in a group tag
    svg.append("g")
        .attr("class", "y axis")
        .call(d3.axisLeft(yScale)); // Create an axis component with d3.axisLeft



    svg.append("path")
        .datum(dataset) // 10. Binds data to the line 
        .attr("class", "line_air") // Assign a class for styling 
        .attr("d", line_air); // 11. Calls the line generator 

    // // 9. Append the path, bind the data, and call the line generator 
    // svg.append("path")
    //     .datum(dataset) // 10. Binds data to the line 
    //     .attr("class", "line") // Assign a class for styling 
    //     .attr("d", line_hum); // 11. Calls the line generator 

    svg.append("path")
        .datum(dataset) // 10. Binds data to the line 
        .attr("class", "line_out") // Assign a class for styling 
        .attr("d", line_out); // 11. Calls the line generator 

    // 12. Appends a circle for each datapoint 
    svg.selectAll(".dot")
        .data(dataset)
        .enter().append("circle") // Uses the enter().append() method
        .attr("class", "dot_air") // Assign a class for styling
        .attr("cx", function(d, i) { return xScale(d.hour) })
        .attr("cy", function(d) { return yScale(d.temp_air) })
        .attr("r", 5)
        .on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div.html("В теплиці: " + d.temp_air + "<br/>" + "На вулиці: " + d.temp_out)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        })
        .on("scroll", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        });

    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    svg.selectAll(".dot")
        .data(dataset)
        .enter().append("circle") // Uses the enter().append() method
        .attr("class", "dot_out") // Assign a class for styling
        .attr("cx", function(d, i) { return xScale(d.hour) })
        .attr("cy", function(d) { return yScale(d.temp_out) })
        .attr("r", 5)
        .on("mouseover", function(d) {
            div.transition()
                .duration(200)
                .style("opacity", .9);
            div.html("В теплиці: " + d.temp_air + "<br/>" + "На вулиці: " + d.temp_out)
                .style("left", (d3.event.pageX) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        })
        .on("scroll", function(d) {
            div.transition()
                .duration(500)
                .style("opacity", 0);
        });

}