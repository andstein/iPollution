function retrieveData() {
    $.ajax({
        url:values_url,
        dataType:"jsonp",
        data:{
            location:$("#location").val()
        },
        success:function (data) {
            var years = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007'];
            var associativeO3 = data.o3;
            var associateNo2 = data.no2;
            var associatepm10 = data.pm10;
            var o3 = [];
            var no2 = [];
            var pm10 = [];
            for (var i = 0; i < years.length; i++) {
                var o3val = associativeO3[years[i]] == undefined ? null : associativeO3[years[i]];
                o3.push(o3val);
                var no2Val = associateNo2[years[i]] == undefined ? null : associateNo2[years[i]];
                no2.push(no2Val);
                var pm10Val = associatepm10[years[i]] == undefined ? null : associatepm10[years[i]];
                pm10.push(pm10Val);
            }

            // calculate totals; interpolate simply by repeating
            var totals={};
            var guesseds={};
            for(var substance in {o3:'o3',no2:'no2',pm10:'pm10'}) 
            {
                var total=0,guessed=0,dept=0,last=-1;
                for(var y=year_start; y<=year_stop; y++) 
                {
                    if (y in data[substance]) {
                        last= data[substance][y];
                        total+= last * (1+dept);
                        dept=0;
                    } else {
                        guessed++;
                        if (last<0)
                            dept++;
                        else
                            total+= last;
                    }
                }
                totals[substance] = total;
                guesseds[substance] = guessed;
            }

            renderTotals( totals,guesseds );
            renderChart(o3, no2, pm10);
        }
    });
}

function renderTotals( totals, guesseds ) {
    console.log('--totals');
    $.each(totals,function(k,v) {
        console.log('k='+k+'; v='+v);
    });
    console.log('--guesseds');
    $.each(guesseds,function(k,v) {
        console.log('k='+k+'; v='+v);
    });
    $('#row_head').append($('<th></th>').append(
                $('#location').val()
                ));
    // an average persons breathes 12m3 / day ...
    $('#row_pm10').append($('<td></td>').append(
                (totals['pm10'] * 12 * 365 / 1e6) + ' g'
                ));
    $('#row_no2').append($('<td></td>').append(
                (totals['no2'] * 12 * 365 / 1e6) / 2.62 + ' l'
                ));
    $('#row_o3').append($('<td></td>').append(
                (totals['o3']) + ' h'
                ));
}

function renderChart(o3, no2, finedust) {
    new Highcharts.Chart({
        chart:{
            renderTo:'result_container',
            zoomType:'xy'
        },
        title:{
            text:'Durchschnittliche jährliche Belastung'
        },
        subtitle:{
            text:'Quelle: Bundesamt für Umwelt'
        },
        xAxis:[
            {
                categories:['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007']
            }
        ],
        yAxis:[
            { // Primary yAxis
                title:{
                    text:'Ozon',
                    style:{
                        color:'#4572A7'
                    }
                },
                labels:{
                    formatter:function () {
                        return this.value + 'Stunden';
                    },
                    style:{
                        color:'#4572A7'
                    }
                }
            },
            { // Secondary yAxis
                title:{
                    text:'Stickstoffdioxid',
                    style:{
                        color:'#89A54E'
                    }
                },
                labels:{
                    formatter:function () {
                        return this.value + 'μg/m3';
                    },
                    style:{
                        color:'#89A54E'
                    }
                },
                opposite:true
            },
            { // Ternary yAxis
                title:{
                    text:'Feinstaub',
                    style:{
                        color:'red'
                    }
                },
                labels:{
                    formatter:function () {
                        return this.value + 'μg/m3';
                    },
                    style:{
                        color:'red'
                    }
                },
                opposite:true
            }
        ],
        legend:{
            layout:'vertical',
            align:'left',
            x:120,
            verticalAlign:'top',
            y:100,
            floating:true,
            backgroundColor:'#FFFFFF'
        },
        series:[
            {
                name:'Ozon',
                color:'#4572A7',
                type:'spline',
                yAxis:1,
                data:o3

            },
            {
                name:'Stickstoffdioxid',
                color:'#89A54E',
                type:'spline',
                yAxis:2,
                data:no2
            },
            {
                name:'Feinstaub',
                color:'red',
                type:'spline',
                yAxis:2,
                data:finedust
            }
        ]
    });

}
