let dataInputDisplay = function() {
    if ($('input:radio[name="inputChoose"]:checked').val() === "0") {
        $('#fileSelection')[0].setAttribute("hidden", true);
        $('#autoMachineConnection')[0].removeAttribute("hidden");
    }
    else {
        $('#autoMachineConnection')[0].setAttribute("hidden", true);
        $('#fileSelection')[0].removeAttribute("hidden");
    }
}

$(document).ready(dataInputDisplay())

$('input:radio[name="inputChoose"]').change(function() {
    dataInputDisplay();
    console.log("caught");
});

$('#testConnection').click(function() {
    $('#connectionState')[0].innerText = "连接成功!";
    setTimeout(function() {
        $('#connectionState')[0].innerText = "";
    }, 2000);
})

$('#conformDataFormat').click(function() {
    $('#conformState')[0].innerText = "数据合法!";
    setTimeout(function() {
        $('#conformState')[0].innerText = "";
    }, 2000);
});