define(['jquery.mobile', 'wq/template', './config'],
function(jqm, tmpl, config) {

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
    if (color_i > config.color_names.length - 1)
        color_i = 0;
    return config.color_names[color_i];
}

function getLayers($page) {
    if (!$page)
        $page = jqm.activePage;
    var list = jqm.activePage.find('.layer-list [data-item_id]').get();

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
    'colors': config.color_names,
    'hexColors': config.hex_colors,
    'getLayers': getLayers
};

});
