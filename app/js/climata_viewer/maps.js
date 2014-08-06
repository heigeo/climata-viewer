define(['leaflet', 'wq/map', './config', './layers'],
function(L, map, config, layers) {
L.Icon.Default.imagePath = "/css/lib/images";

layers.colors.forEach(function(color) {
    map.createIcon(color, {
        'iconUrl': '/images/' + color + '.png',
        'shadowUrl': L.Icon.Default.imagePath + '/marker-shadow.png'
    });
});

function setup() {
    map.init(config.map);
    map.getLayerConfs = function(page, itemid) {
        return _maps[page](itemid);
    };
}

var _maps = {
    'datarequest': function(itemid) {
        return [_siteLayer({
            'id': itemid,
            'label': 'Sites',
            'color': 'blue'
        })];
    },
    'project': function() {
        return layers.getLayers().map(_siteLayer);
    }
};

function _siteLayer(item) {
    return {
        'url': 'datarequests/' + item.id + '/sites',
        'name': item.label,
        'oneach': map.renderPopup('site'),
        'icon': item.color
    };
}

return {
    'setup': setup
};

});
