function retrieveData() {
    $.ajax({
        url: "http://192.168.51.57:5000/values",
        dataType: "jsonp",
        data: {
            location: $("#location").val()
        },
        success: function( data ) {
            alert($("#location").val());
        }
    });
}