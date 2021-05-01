var server_address = "http://api.uc3m.tk:80/"
var get_data = function() {
    $.get( server_address + "current_sensor_data/" ,function(data) {
        $(".result").html("Temperature: " + data.temperature + "ºC | Humidity " + data.himidity + "%");
    });
}

setInterval(get_data, 2000)