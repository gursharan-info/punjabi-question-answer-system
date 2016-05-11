$(document).ready(function() {

    question = $.parseJSON($('#q_cog').val());
    //console.log( question );
    answers = $.parseJSON($('#a_cog').val());
    //console.log(answers);
    var question_points = [
        [question.X1, question.Y1],
        [question.X2, question.Y2],
        [question.X3, question.Y3],
    ];
    var question_cog = [[question.cogX, question.cogY]];

    var question_data = [ { label: "Que. X,Y", data: question_points, points: { radius: 8, symbol: "triangle", fillColor: "#058DC7" }, color: "#058DC7" },
        { label: "Que. CoG", data: question_cog, points: { radius: 10, symbol: "circle", fillColor: "#50B432" }, color: "#50B432" }
    ];
    colors = ['#DC143C','#FF3E96','#7D26CD','#9F79EE','#6E7B8B','#00FA9A','#00FF00','#FFFF00','#8B5A00','#FF4500','#FFC0CB','#000000','#C67171','#8B4513','#FF8C00','#FFD700','#6E8B3D','#00C957','#00BFFF','#D02090','#48D1CC','#556B2F','#C76114'];
    x_max_array = [];
    y_max_array = [];
    $.each( answers, function( key, value ) {
        point_data = [
            [value.sentence_cog.X1, value.sentence_cog.Y1],
            [value.sentence_cog.X2, value.sentence_cog.Y2],
            [value.sentence_cog.X3, value.sentence_cog.Y3],
        ];
       // console.log(point_data);
        cog_data = [[value.sentence_cog.cogX, value.sentence_cog.cogY]];
        x_max_array.push(Math.max(value.sentence_cog.X1,value.sentence_cog.X2,value.sentence_cog.X3));
        y_max_array.push(Math.max(value.sentence_cog.Y1,value.sentence_cog.Y2,value.sentence_cog.Y3));

      answer_point = {label: "S"+key+". X,Y", data: point_data, points: { symbol: "triangle", fillColor: colors[key] }, color: colors[key] };
      answer_cog = {label: "S"+key+". CoG", data: cog_data, points: { symbol: "circle", fillColor: colors[key] }, color: colors[key] };
      question_data.push(answer_point);
      question_data.push(answer_cog);
    });
    x_max = Math.max(...x_max_array);
    y_max = Math.max(...y_max_array);
    //console.log(x_max, y_max);

    //console.log(question_data);
    $.plot($("#question_graph"), question_data, {
        series: {
            points: {
                radius: 4,
                show: true,
                fill: true,
            },
            color: "#058DC7"
        },
        xaxis: {
            min: -1,
            max: x_max + 1
        },
        yaxis: {
            min: -1,
            max: y_max + 1
        },
        grid: {
            hoverable: true,
            aboveData: true
        }
    });
    function showTooltip(x, y, contents) {
        $("<div id='tooltip'>" + contents + "</div>").css({
            position: "absolute",
            display: "none",
            top: y + 5,
            left: x + 5,
            border: "1px solid #fdd",
            padding: "2px",
            "background-color": "#fee",
            opacity: 0.80
        }).appendTo("body").fadeIn(200)
    }
    $("#question_graph").bind("plothover", function (event, pos, item) {
        if (item) {
            //console.log(item);
            if (previousPoint != item.dataIndex) {
                previousPoint = item.dataIndex;
                $("#tooltip").remove();
                var x = item.datapoint[0],
                y = item.datapoint[1];
                showTooltip(item.pageX, item.pageY,
                item.series.label + "= " + x + ", " + y);
            }
        } else {
            $("#tooltip").remove();
            previousPoint = null;
        }
    });

});