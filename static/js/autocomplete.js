$(function() {
    function log( message ) {
        $( "#location").text(message);
        $( "<div/>" ).text( message ).prependTo( "#log" );
        $( "#log" ).scrollTop( 0 );
    }

    $( "#location" ).autocomplete({
        source: function( request, response ) {
            $.ajax({
                url: "http://ws.geonames.org/searchJSON",
                dataType: "jsonp",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function( data ) {
                    response( $.map( data.geonames, function( item ) {
                        return {
                            value: item.name
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $( this ).removeClass( "ui-corner-all" ).addClass( "ui-corner-top" );
        },
        close: function() {
            $( this ).removeClass( "ui-corner-top" ).addClass( "ui-corner-all" );
        }
    });
});