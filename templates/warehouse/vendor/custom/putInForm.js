current = 1

function getOneItemHTML(index) {
    return '    <div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">' +
    '        <div class="form-group">' +
    '            <input type="text" class="form-control" value="' + index.toString() + '" readonly>' +
    '        </div>' +
    '    </div>' +
    '    <div class="col-xl-3 col-lglg-3 col-md-3 col-sm-3 col-12">' +
    '        <div class="form-group">' +
    '            <input type="text" class="form-control">' +
    '        </div>' +
    '    </div>' +
    '    <div class="col-xl-2 col-lglg-2 col-md-2 col-sm-2 col-12">' +
    '        <div class="form-group">' +
    '            <input type="text" class="form-control">' +
    '        </div>' +
    '    </div>' +
    '    <div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">' +
    '        <div class="form-group">' +
    '            <input type="text" class="form-control">' +
    '        </div>' +
    '    </div>' +
    '    <div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">' +
    '        <div class="form-group">' +
    '            <input type="text" class="form-control">' +
    '        </div>' +
    '    </div>' +
    '    <div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">' +
    '        <div class="form-group">' +
    '            <input type="text" class="form-control">' +
    '        </div>' +
    '    </div>' +
    '    <div class="col-xl-1 col-lglg-1 col-md-1 col-sm-1 col-12">' +
    '        <div class="form-group">' +
    '            <input type="text" class="form-control">' +
    '        </div>' +
    '    </div>\n' +
    '    <div class="col-xl-2 col-lglg-2 col-md-2 col-sm-2 col-12">' +
    '        <div class="form-group">' +
    '            <input type="text" class="form-control">' +
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