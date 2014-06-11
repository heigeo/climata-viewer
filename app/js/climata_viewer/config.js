define(["wq/store", "wq/router", "wq/pages", "db/config", "./version"],
function(ds, router, pages, config, version) {

config.defaults = {
    'version': version,
    'use_select': function() {
        var info = _getContextInfo.call(this);
        var from_type = info.reltype.from_type;
        if (!info)
            return false;
        var url = config.pages[from_type].url;
        var filter;
        if (from_type == 'site' || from_type == 'parameter')
            filter = {'authority_id': info.webservice.authority_id};
        else
            filter = {};
        var choices = ds.filter({'url': url}, filter);
        if (choices.length <= 20)
            return true;
        return false;
    },
    'required': function() {
        var info = _getContextInfo.call(this);
        if (!info)
            return false;
        var type_id = info.reltype.from_type;
        if (type_id == 'site')
            type_id = 'station';
        if (type_id)
            return info.webservice.opts[type_id].required;
        return false;
    }
};

function _getContextInfo() {
    var info = {};
    var params = router.getParams(pages.info.path);
    if (!params.webservice_id || !this.type_id)
        return null;
    info.webservice = ds.find({'url': 'webservices'}, params.webservice_id);
    info.reltype = ds.find({'url': 'relationshiptypes'}, this.type_id);
    return info;
}

config.transitions = {
    'default': "slide",
    'save': "flip"
};

return config;

});
