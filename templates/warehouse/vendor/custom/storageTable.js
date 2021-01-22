function getFormatIndex(n) {
    let n_str = n.toString();
    return "0".repeat(8 - n_str.length) + n_str;
}


let data = "";
data += "<tbody>";

for (let i = 0; i < 10; ++i) {
    data += "<tr>";
    for (let j = 0; j < 11; ++j) {
        data += "<td>3A" + getFormatIndex(10 * i + j) + "</td>";
    }
    data += "</tr>";
}


for (let i = 0; i < 20; ++i) {
    data += "<tr'>";
    for (let j = 0; j < 11; ++j) {
        data += "<td>3B" + getFormatIndex(10 * i + j) + "</td>";
    }
    data += "</tr>";
}

data += "</tbody>";

let table = document.getElementById('storageTable')
table.innerHTML = data;

for (let i = 0; i < 40; ++i) {
    let _row = Math.floor(Math.random()*30);
    let _col = Math.floor(Math.random()*10);
    table.rows[_row].cells[_col].bgColor = "#FF3300";
}
