function getFormatIndex(n) {
    let n_str = n.toString();
    return "0".repeat(8 - n_str.length) + n_str;
}

let data = "";
for (let i = 0; i < 70; i++) {
    data += "<tr>";

    // Storage block index
    data += "<td>3A" + getFormatIndex(i) + "</td>";
    // Warehouse index
    data += "<td>A001</td>";
    // Total capacity
    data += "<td>50</td>";
    // Current occupy
    data += "<td>20</td>";
    // Rest
    data += "<td>30</td>";
    // Type of the block
    data += "<td>" + ["线材", "零件"][Math.round(Math.random())] + "</td>";

    data += "</tr>";
}

$("#freeBlocks")[0].innerHTML = data;