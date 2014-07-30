define(['jquery', 'wq/app', 'wq/pages', 'wq/store'],
function($, app, pages, ds) {

$('body').on('login', function() {
    $('body').addClass('logged-in');
    $('body').removeClass('logged-out');
});

$('body').on('logout', function() {
    $('body').addClass('logged-out');
    $('body').removeClass('logged-in');
});

function setup() {
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
    pages.addRoute('datarequests/new', 's', _addStateFilter);
}

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

function _addStateFilter(match, ui, params, hash, evt, $page) {
    ds.getList({'url': 'relationshiptypes'}, function(list) {
        var stype = list.find('state', 'from_type');
        var sid = "d-ir-" + stype.id;
        var $select = $page.find('select#' + sid);
        if (!$select)
            return;
        $select.change(function() {
            var $opts = $page.find('option[data-state_id]'),
                state = $select.val();
            $opts.filter('[data-state_id="' + state + '"]').show();
            $opts.filter('[data-state_id!="' + state + '"]').hide();
        });
    });
}

return {'setup': setup};

});
