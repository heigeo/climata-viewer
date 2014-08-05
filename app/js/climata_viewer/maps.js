define(['leaflet', 'wq/map', './config'],
function(L, map, config) {
L.Icon.Default.imagePath = "/css/lib/images";

function setup() {
    map.init(config.map);
    map.getLayerConfs = function(page, itemid) {
        return _maps[page](itemid);
    };
}

var _maps = {
    'datarequest': function(itemid) {
        return [{
            'url': 'datarequests/' + itemid + '/sites',
            'name': 'Sites',
            'oneach': map.renderPopup('site')
        }];
    },
    'project': function(itemid) {
        return []; // FIXME
    }
};

return {
    'setup': setup
};

});
