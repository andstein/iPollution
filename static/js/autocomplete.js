$(function() {
    $( "#location" ).autocomplete({
        source:
            function( request, response ) {
            $.ajax({
                url: "http://192.168.51.57:5000/search",
                dataType: "jsonp",
                data: {
                    maxRows: 12,
                    term: request.term
                },
                success: function( data ) {
                    response( data);
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