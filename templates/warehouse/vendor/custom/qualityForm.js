let formDisplay = function() {
    switch($('#activityType').val()) {
        case "1":
            $('#repair').hide();
            $('#wasteCheck').hide();
            $('#lossCheck').show();
            break;
        case "2":
            $('#lossCheck').hide();
            $('#wasteCheck').hide();
            $('#repair').show();
            break;
        case "3":
            $('#lossCheck').hide();
            $('#repair').hide();
            $('#wasteCheck').show();
            break;
        default:
            console.log($('#activityType').val());
    }
}

$(document).ready(function () {
    $('#lossCheck').hide();
    $('#wasteCheck').hide();
    $('#repair').hide();
});
