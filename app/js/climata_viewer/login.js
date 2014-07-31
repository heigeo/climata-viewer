define(['jquery', 'wq/app', 'wq/pages', 'wq/store', 'wq/spinner'],
function($, app, pages, ds, spin) {

$('body').on('login', function() {
    $('body').addClass('logged-in');
    $('body').removeClass('logged-out');
});

$('body').on('logout', function() {
    $('body').addClass('logged-out');
    $('body').removeClass('logged-in');
});

function setup() {
    pages.addRoute('datarequests/new', 's', _addStateFilter);
}

function prefetch() {
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
}

function toggle(pid, value) {
    $.post(
        "/datarequests/" + pid + "/toggle.json",
        {
            'public': value,
            'csrfmiddlewaretoken': ds.get('csrftoken')
        },
        function success(result) {
            var msg;
            if (result['public'])
                msg = "Set to Public";
            else
                msg = "Set to Private";
            ds.getList({'url': 'datarequests'}, function(list) {
                var req = list.find(pid);
                if (!req) return;
                req['public'] = result['public'];
                list.update([req], 'id');
            });
            spin.start(msg, 2, {'textonly': true});
        }
    );
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
                state = $select.val(), $enable, $disable;
            if (!state) {
                $enable = $opts;
                $disable = null;
            } else {
                $enable = $opts.filter('[data-state_id="' + state + '"]');
                $disable = $opts.filter('[data-state_id!="' + state + '"]');
            }
            $enable.show().attr('disabled', false);
            if ($disable)
                $disable.hide().attr('disabled', true);
        });
    });
}

return {
    'setup': setup,
    'prefetch': prefetch,
    'toggle': toggle
};

});
