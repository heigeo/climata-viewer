define(['wq/app', 'wq/store', 'wq/progress', './config', './templates'],
function(app, ds, progress, config, templates) {

app.init(config, templates);

// Initialize data import progress bar
progress.init('datarequests/<slug>/data', onComplete, onFail);

function onComplete($progress, data) {
    $progress.siblings('.complete').show();
}

function onFail($progress, data) {
    $progress.siblings('.complete').html("Error loading data.").show();
}

// Prefetch important data lists
['webservices',
 'datarequests',
 'parameters',
 'sites',
 'relationshiptypes',
 'inverserelationships'].forEach(function(name) {
    ds.prefetch({'url': name});
});

// Customize inverserelationship items auto-generated for new datarequests
var iropts = app.attachmentTypes.inverserelationship;
 
// Only show relationship types valid for the selected webservice
iropts.getTypeFilter = function(page, context) {
    var webservice = context.webservice.call(context),
        from_types = [],
        filters = ['site', 'region', 'parameter'],
        filterNames = {
            'site': 'station',
            'region': 'basin'
        };

    filters.forEach(function(field) {
        var name = filterNames[field] || field;
        if (!webservice.opts[name].ignored)
            from_types.push(field);
    });

    return {
        'from_type': from_types,
        'to_type': page
    };

};


// Limit site and parameter choices to the same authority as the webservice
// (e.g. only show Hydromet site codes for Hydromet webservices)
iropts.getChoiceListFilter = function(type, context) {
    if (type.from_type == 'region')
        return {};

    var webservice = context.webservice.call(context);
    return {'authority_id': webservice.authority_id};
};

});
