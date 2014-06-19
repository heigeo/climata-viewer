define(['jquery', 'wq/app', 'wq/store', 'wq/pages', 'wq/progress',
        './config', './templates'],
function($, app, ds, pages, progress, config, templates) {

// Initialize wq/app and connect to auth events
app.init(config, templates);

$('body').on('login', function() {
    $('body').addClass('logged-in');
    $('body').removeClass('logged-out');
});

$('body').on('logout', function() {
    $('body').addClass('logged-out');
    $('body').removeClass('logged-in');
});

// Initialize data import progress bar
progress.init('datarequests/<slug>/auto', onComplete, onFail, onProgress);

function onComplete($progress, data) {
    $progress.siblings('.complete').show();
}

function onFail($progress, data) {
    $progress.siblings('.message').html(
        "Error loading data:<br>" +
        "<pre><code>" + data.error + "</code></pre>"
    );
}

function onProgress($progress, data) {
    $progress.siblings('.message').html(data.message || "");
    if (data.action) {
        var url = $progress.data('url');
        var match = url.match(/\/datarequests\/(\d+)\/status/);
        if (match) {
            url = "datarequests/" + match[1] + "/" + data.action;
            ds.getList({'url': 'datarequests'}, function(list) {
                var context = $.extend({'result': data}, list.find(match[1]));
                pages.go(url, 'datarequest_' + data.action, context);
            });
        }
    }
}

// Prefetch important data lists
['webservices',
 'authorities',
 'states',
 'counties',
 'basins',
 'sites',
 'parameters',
 'datarequests',
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
        filters = ['site', 'state', 'county', 'basin', 'parameter'],
        filterNames = {
            'site': 'station'
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
    if (type.from_type != 'parameter' && type.from_type != 'site')
        return {};

    var webservice = context.webservice.call(context);
    return {'authority_id': webservice.authority_id};
};

});
