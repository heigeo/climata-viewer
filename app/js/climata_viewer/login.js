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
    pages.addRoute('datarequests/new', 's', _initFilters);
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

function action(pid, action, field, value, ontrue, onfalse) {
    var post = {
        'csrfmiddlewaretoken': ds.get('csrftoken')
    }
    post[field] = value;
    $.post(
        "/datarequests/" + pid + "/" + action + ".json",
        post,
        function success(result) {
            var msg = result[field] ? ontrue : onfalse;
            ds.getList({'url': 'datarequests'}, function(list) {
                var req = list.find(pid);
                if (!req) return;
                req[field] = result[field];
                list.update([req], 'id');
            });
            spin.start(msg, 2, {'textonly': true});
        }
    );
}

function toggle(pid, value) {
    action(pid, 'toggle', 'public', value, "Set to Public", "Set to Private");
}

function del(pid) {
    if (confirm("Are you sure you want to delete this data request?")) {
        action(pid, 'delete', 'deleted', true, "Deleted", "Not Deleted");
        setTimeout(function() {
            $.mobile.changePage('/');
        }, 3000);
    }
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

function _initFilters(match, ui, params, hash, evt, $page) {
    ds.getList({'url': 'relationshiptypes'}, function(list) {
        // Find the <select> menu or <input> corresponding to the filter name
        function _getInput(name) {
            var stype = list.find(name, 'from_type');
            var sid = "d-ir-" + stype.id;
            return $page.find('#' + sid);
        }

        var $state = _getInput('state'),
            $basin = _getInput('basin'),
            $county = _getInput('county');

        // Auto-filter county by state
        if ($state.length) {
            $state.change(_filterByState);
        }

        function _filterByState() {
            var $opts = $page.find('option[data-state_id]'),
                state = $state.val(), $enable, $disable;
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
        }

        // Only one of county or basin can be specified
        if ($county.length && $basin.length) {
            _exclude($county, $basin);
            _exclude($basin, $county);
        }

        function _exclude($l1, $l2) {
            $l1.change(function() {
                $l2.attr('disabled', !!$l1.val());
                if ($l2.is('select'))
                    $l2.selectmenu('refresh');
            });
        }
    });
}

return {
    'setup': setup,
    'prefetch': prefetch,
    'toggle': toggle,
    'del': del
};

});
