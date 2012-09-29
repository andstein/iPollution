function retrieveData() {
    var location = $('#location').val()
    $.ajax({
        url:values_url,
        dataType:"jsonp",
        data:{
            location:location
        },
        success:function (data) {

            // calculate totals; interpolate simply by repeating
            var realdatas={};
            var fakedatas={};
            var totals={};
            var guesseds={};
            $.each(['o3','no2','pm10'],function (i,substance) 
            {
                if (!( substance in data ))
                    data[substance]={ year_start:0 };

                var total=0,guessed=0,dept=0,last=-1;
                var realdata=[],fakedata=[];
                for(var y=year_start; y<=year_stop; y++) 
                {
                    if (y in data[substance]) {

                        last= data[substance][y];
                        total+= last * (1+dept);
                        while(dept > 0) {
                            realdata.push(null);
                            fakedata.push( last );
                            dept--;
                        }

                        realdata.push(data[substance][y]);
                        fakedata.push(null);

                    } else {

                        guessed++;
                        if (last<0)
                            dept++;
                        else {
                            total+= last;
                            realdata.push(null);
                            fakedata.push(last);
                        }


                    }
                }
                totals[substance] = total;
                guesseds[substance] = guessed;
                realdatas[substance] = realdata;
                fakedatas[substance] = fakedata;
            });

            all_data[location]= { 'real':realdatas, 'fake':fakedatas };

            $('#row_head').append($('<th></th>').append(
                        $('#location').val()
                        ));
            // an average persons breathes 12m3 / day ...
            $('#row_pm10').append($('<td></td>').append(
                        formatFloat(totals['pm10'] * 12 * 365 / 1e6) + ' g'
//                        ));
                        ).click(function(){ renderOneChart(location,'pm10') }));
            $('#row_no2').append($('<td></td>').append(
                        formatFloat(totals['no2'] * 12 * 365 / 1e6 / 2.62) + ' l'
                        ).click(function(){ renderOneChart(location,'no2') }));
            $('#row_o3').append($('<td></td>').append(
                        formatHours(totals['o3'])
                        ).click(function(){ renderOneChart(location,'o3') }));

        }
    });
}

function formatFloat(f) {
    return Math.round(100* f)/100;
}
function formatHours(h) {
    if (h>24*365)
        return Math.floor(h/24/365)+" y "+Math.floor((h%(24*365)/24))+" d "+(h%24)+" h";
    if (h>48)
        return Math.floor(h/24)+" d "+(h%24)+" h";
    return h + " h";
}

function renderOneChart( location,substance ) {
    new Highcharts.Chart({
        chart:{
            renderTo:'result_container',
            zoomType:'xy'
        },
        title:{
            text:'Yearly averages of ' + all_names[substance] + ' in ' + location
        },
        subtitle:{
            text:'Source: Bundesamt für Umwelt'
        },
        plotOptions: {
            series: {
                point: {
                    events: {
                        click: function() {
                            window.open(dump_url + '?location=' + location + '&substance=' + substance + '&year=' + year_labels_complete[this.x]);
                        }
                    }
                }
            }
        },
        xAxis:[
            {
                categories:year_labels,
            }
        ],
        yAxis:[
            { // needs 2nd axis -- doesn't show values anyway... bug ?
                title:{
                    text:'',
                    style:{
                        color:'#4572A7'
                    }
                },
                labels:{
                    style:{
                        color:'#4572A7'
                    }
                },
            },
            {
                title:{
                    text:all_names[substance],
                    style:{
                        color:'#4572A7'
                    }
                },
                labels:{
                    formatter:function () {
                        return this.value + ' ' + all_units[substance];
                    },
                    style:{
                        color:'#4572A7'
                    }
                },
            },
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
                name:'extracted data',
                color:'#4572A7',
                type:'spline',
                yAxis:1,
                data:all_data[location]['real'][substance],

            },
            {
                name:'interpolated data',
                color:'#a0bdbb',
                type:'spline',
                yAxis:1,
                data:all_data[location]['fake'][substance],
            }
        ]
    });

}
