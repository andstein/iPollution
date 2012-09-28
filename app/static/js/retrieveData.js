function retrieveData() {
    $.ajax({
        url:values_url,
        dataType:"jsonp",
        data:{
            location:$("#location").val()
        },
        success:function (data) {

            // calculate totals; interpolate simply by repeating
            var realdatas={};
            var fakedatas={};
            var totals={};
            var guesseds={};
            var years=null;
            $.each(['o3','no2','pm10'],function (i,substance) 
            {
                var total=0,guessed=0,dept=0,last=-1;
                var realdata=[],fakedata=[];
                years=[];
                for(var y=year_start; y<=year_stop; y++) 
                {
                    if (y in data[substance]) {

                        last= data[substance][y];
                        total+= last * (1+dept);
                        while(dept > 0) {
                            fakedata.push( last );
                            dept--;
                        }

                        realdata.push(data[substance][y]);
                        fakedata.push(null);

                    } else {

                        guessed++;
                        if (last<0)
                            dept++;
                        else
                            total+= last;

                        realdata.push(null);
                        fakedata.push(last);

                    }
                    years.push(y);
                }
                totals[substance] = total;
                guesseds[substance] = guessed;
                realdatas[substance] = realdata;
                fakedatas[substance] = fakedata;
            });

            renderTotals( totals,guesseds );
            renderChart( years,realdatas,fakedatas );
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

function renderChart( years,realdatas,fakedatas ) {

    new Highcharts.Chart({
        chart:{
            renderTo:'result_container',
            zoomType:'xy'
        },
        title:{
            text:'Yearly averages'
        },
        subtitle:{
            text:'Source: Bundesamt für Umwelt'
        },
        xAxis:[
            {
                categories:years
            }
        ],
        yAxis:[
            { // Primary yAxis
                title:{
                    text:'Ozone',
                    style:{
                        color:'#4572A7'
                    }
                },
                labels:{
                    formatter:function () {
                        return this.value + ' hours';
                    },
                    style:{
                        color:'#4572A7'
                    }
                },
            },
            { // Secondary yAxis
                title:{
                    text:'Nitrogen dioxide',
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
                opposite:true,
            },
            { // Ternary yAxis
                title:{
                    text:'Particulates',
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
                opposite:true,
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
                name:'Ozone',
                color:'#4572A7',
                type:'spline',
                yAxis:1,
                data:realdatas['o3']

            },
            {
                name:'Nitrogen dioxide',
                color:'#89A54E',
                type:'spline',
                yAxis:2,
                data:realdatas['no2']
            },
            {
                name:'Particulates',
                color:'red',
                type:'spline',
                yAxis:2,
                data:realdatas['pm10']
            }
        ]
    });

}
