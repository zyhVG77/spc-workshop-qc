function hex (c) {
    let s = "0123456789abcdef";
    let i = parseInt (c);
    if (i === 0 || isNaN(c))
        return "00";
    i = Math.round (Math.min (Math.max (0, i), 255));
    return s.charAt ((i - i % 16) / 16) + s.charAt (i % 16);
}

/* Convert an RGB triplet to a hex string */
function convertToHex (rgb) {
    return hex(rgb[0]) + hex(rgb[1]) + hex(rgb[2]);
}

/* Remove '#' in color hex string */
function trim (s) {
    return (s.charAt(0) === '#') ? s.substring(1, 7) : s;
}

/* Convert a hex string to an RGB triplet */
function convertToRGB (hex) {
    let color = [];
    color[0] = parseInt((trim(hex)).substring (0, 2), 16);
    color[1] = parseInt((trim(hex)).substring (2, 4), 16);
    color[2] = parseInt((trim(hex)).substring (4, 6), 16);
    return color;
}

export
function generateColor(colorStart,colorEnd,colorCount){
    let start = convertToRGB (colorStart);
    let end   = convertToRGB (colorEnd);
    let len = colorCount;

    let alpha = 0.0;
    let res = [];

    for (let i = 0; i < len; i++) {
        let c = [];
        alpha += (1.0/len);
        c[0] = start[0] * alpha + (1 - alpha) * end[0];
        c[1] = start[1] * alpha + (1 - alpha) * end[1];
        c[2] = start[2] * alpha + (1 - alpha) * end[2];
        res.push(convertToHex (c));
    }

    return res;
}
