define(["wq/store", "wq/router", "wq/pages", "data/config",
        "data/version", "data/climata_version"],
function(ds, router, pages, config, version, climata_version) {

var defaultYear = new Date().getFullYear() - 1;

config.defaults = {
    'version': version,
    'climata_version': climata_version,
    'use_select': function() {
        var info = _getContextInfo.call(this);
        var from_type = info.reltype.from_type;
        if (config.pages[from_type].partial)
            return false;
        if (!info)
            return false;
        var url = config.pages[from_type].url;
        var filter;
        if (from_type == 'site' || from_type == 'parameter')
            filter = {'authority_id': info.webservice.authority_id};
        else
            filter = {};
        var choices = ds.filter({'url': url}, filter);
        if (choices.length <= 200)
            return true;
        return false;
    },
    'use_remote': function() {
        var info = _getContextInfo.call(this);
        var from_type = info.reltype.from_type;
        if (config.pages[from_type].partial)
            return true;
        else
            return false;
    },
    'filter_auth': function() {
        var info = _getContextInfo.call(this);
        var from_type = info.reltype.from_type;
        if (from_type == 'site')
            return true;
    },
    'required': function() {
        var info = _getContextInfo.call(this);
        if (!info)
            return false;
        var type_id = info.reltype.from_type;
        if (type_id == 'project')
            return false;
        if (type_id == 'site')
            type_id = 'station';
        if (type_id)
            return info.webservice.opts[type_id].required;
        return false;
    },
    'select_prompt': function() {
        var info = _getContextInfo.call(this);
        if (!info)
            return "Any / All";
        if (config.defaults.required.call(this))
            return "Pick an option...";
        var type_id = info.reltype.from_type;
        if (type_id == 'project')
            return "None";
        return "Any / All";
    },
    'start_date': defaultYear + '-01-01',
    'end_date': defaultYear + '-12-31'
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

config.map = {
    'zoom': 3,
    'center': [40, -96]
};

return config;

});
