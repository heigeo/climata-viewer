define(['jquery.mobile', 'wq/template'],
function(jqm, tmpl) {

var colors = [
    'blue',
    'green',
    'purple',
    'red',
    'orange'
];
var hexColors = [
    '#4292c6',
    '#41ab5d',
    '#807dba',
    '#ef3b2c',
    '#f16913'
];

function setup() {
    tmpl.setDefault('reset_color', _resetColor);
    tmpl.setDefault('get_color', _getColor);
}

var color_i = -1;

function _resetColor() {
    color_i = -1;
}

function _getColor() {
    color_i++;
    if (color_i > colors.length - 1)
        color_i = 0;
    return colors[color_i];
}

function getLayers($page) {
    if (!$page)
        $page = jqm.activePage;
    var list = jqm.activePage.find('.layer-list li[data-item_id]').get();

    _resetColor();
    var layers = list.map(function(item) {
        var data = item.dataset;
        return {
            'id': data.item_id,
            'label': data.item_label.split(' from ')[0],
            'color': _getColor()
        };
    });

    return layers;
}

return {
    'setup': setup,
    'colors': colors,
    'hexColors': hexColors,
    'getLayers': getLayers
};

});
