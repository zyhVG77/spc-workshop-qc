let current = 1

function getOneItemHTML(n) {
    return '    <div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">' +
        '        <div class="form-group">' +
        '            <label for="index">编号</label>' +
        '            <input type="text" class="form-control" id="index" value="'+n.toString()+'" readOnly>' +
        '        </div>' +
        '    </div>' +
        '    <div class="col-xl-3 col-lglg-3 col-md-3 col-sm-3 col-12">' +
        '        <div class="form-group">' +
        '            <label For="inputGroupSelect06">属性</label>' +
        '            <select class="custom-select" aria-label="Example select with button addon">' +
        '                <option selected="">选择属性</option>' +
        '                <option value="1">属性1</option>' +
        '                <option value="2">属性2</option>' +
        '                <option value="3">属性3</option>' +
        '            </select>' +
        '        </div>' +
        '    </div>'
}

function addItem() {
    let lastItem = $('#itemList')[0].lastElementChild;
    let item = document.createElement("div");
    item.setAttribute("class", "row gutters");
    item.innerHTML = getOneItemHTML(++current);
    $('#itemList')[0].insertBefore(item, lastItem);
}