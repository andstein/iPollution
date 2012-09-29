

function realfake(data) {
    // calculate totals; interpolate simply by repeating
    var realdatas={};
    var fakedatas={};
    $.each(['o3','no2','pm10'],function (i,substance) 
    {
        if (!( substance in data ))
            data[substance]={ year_start:0 };

        var dept=0,last=-1;
        var realdata=[],fakedata=[];
        for(var y=year_start; y<=year_stop; y++) 
        {
            if (y in data[substance]) {

                last= data[substance][y];
                while(dept > 0) {
                    realdata.push(null);
                    fakedata.push( last );
                    dept--;
                }

                realdata.push(data[substance][y]);
                fakedata.push(null);

            } else {

                if (last<0)
                    dept++;
                else {
                    realdata.push(null);
                    fakedata.push(last);
                }


            }
        }
        realdatas[substance] = realdata;
        fakedatas[substance] = fakedata;
    });

    return { 'real':realdatas , 'fake':fakedatas };
}

function addTableColumn(location) {

    var totals=[];
    var realdata= all_data[location].real;
    var fakedata= all_data[location].fake;

    $.each(['o3','no2','pm10'],function (i,substance) {
        total=0;
        for(var y=year_start,i=0; y<=year_stop; y++,i++) 
            if (realdata[substance][i])
                total += realdata[substance][i];
            else
                total += fakedata[substance][i];

        totals[substance]= total;
    });

    $('#row_head').append($('<th></th>').append(
                location
                ).addClass('total'));
    // an average persons breathes 12m3 / day ...
    $('#row_pm10').append($('<td></td>').append(
                formatFloat(totals['pm10'] * 12 * 365 / 1e6) + ' g'
                ).addClass('total').click(function(){ renderOneChart(location,'pm10') }));
    $('#row_no2').append($('<td></td>').append(
                formatFloat(totals['no2'] * 12 * 365 / 1e6 / 2.62) + ' l'
                ).addClass('total').click(function(){ renderOneChart(location,'no2') }));
    $('#row_o3').append($('<td></td>').append(
                formatHours(Math.round(totals['o3']))
                ).addClass('total').click(function(){ renderOneChart(location,'o3') }));
}

function retrieveData() {
    var location = $('#location').val()
    $.ajax({
        url:values_url,
        dataType:"jsonp",
        data:{
            location:location
        },
        success:function (data) {

            locations.push( location );
            raw_data[location]= data;
            all_data[location]= realfake(data);
            addTableColumn(location);

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
            renderTo:'charts_container',
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
                            Shadowbox.open({
                                content: dump_url + '?location=' + location + '&substance=' + substance + '&year=' + year_labels_complete[this.x],
                            height: 326,
                            width: 515,
                            player: 'iframe'
                            });
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
