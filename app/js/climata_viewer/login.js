define(['jquery', 'wq/app', 'wq/pages', 'wq/store',
        'wq/spinner', 'wq/template'],
function($, app, pages, ds, spin, tmpl) {

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
    var meta = [
      'webservices',
      'authorities',
      'states',
      'counties',
      'basins',
      'sites',
      'parameters',
      'relationshiptypes'
    ];
    var user = [
      'datarequests',
      'projects',
      'relationships',
      'inverserelationships'
    ];
    _prefetch(meta);
    if (_listExists('projects') && _listExists('relationships')) {
        _setLatestProject();
    }
    _prefetch(user, _setLatestProject);

    function _prefetch(lists, then) {
        var data = {
            'url': 'multi',
            'lists': lists.join(',')
        };
        ds.fetch(data, true, function(result) {
            _saveResult(result);
            if (then)
                then();
        }, true);
    }

    function _saveResult(result) {
        var query, data, key;
        for (key in result) {
            query = {'url': key, 'page': 1};
            data = result[key];
            ds.setPageInfo(query, data);
            ds.set(query, data.list);
            if (key == 'projects') {
                _setLatestProject();
            }
        }
    }
    function _setLatestProject() {
        ds.getList({'url': 'projects'}, function(plist) {
            ds.getList({'url': 'relationships'}, function(rlist) {
                tmpl.setDefault('latest_project',
                    _latest.bind(this, plist, rlist)
                );
            });
        });

        function _latest(plist, rlist) {
            var latest = null;
            plist.forEach(function(project) {
                if (!project['public'])
                    return;
                if (!latest || project.created > latest.created)
                    latest = project;
            });
            if (!latest)
                return;
            return {
                'id': latest.id,
                'label': latest.label,
                'relationships': latest.relationships || rlist.filter({
                    'project_id': latest.id
                 })
            };
        }
    }
}

function _action(page, itemid, action, field, value, ontrue, onfalse) {
    var baseurl = app.config.pages[page].url;
    var post = {
        'csrfmiddlewaretoken': ds.get('csrftoken')
    };
    post[field] = value;
    $.post(
        "/" + baseurl + "/" + itemid + "/" + action + ".json",
        post,
        function success(result) {
            var msg = result[field] ? ontrue : onfalse;
            ds.getList({'url': baseurl}, function(list) {
                var req = list.find(itemid);
                if (!req) return;
                req[field] = result[field];
                list.update([req], 'id');
            });
            spin.start(msg, 2, {'textonly': true});
        }
    );
}

function toggle(page, itemid, value) {
    _action(
        page, itemid, 'toggle', 'public', value,
        "Set to Shared", "Set to Private"
    );
}

function del(page, itemid) {
    /* global confirm */
    if (confirm("Are you sure you want to delete this data request?")) {
        _action(
            page, itemid, 'delete', 'deleted', true,
            "Deleted", "Not Deleted"
        );
        setTimeout(function() {
            $.mobile.changePage('/');
        }, 3000);
    }
}

function setProject(projectid) {
    ds.getList({'url': 'projects'}, function(list) {
        tmpl.setDefault('current_project', list.find(projectid));
    });
    tmpl.setDefault('current', function() {
        return this.id == projectid;
    });
}

// Need to ensure relationships is updated after datarequest save
var _postsave = app.postsave;
app.postsave = function(item, result, conf) {
    if (conf.name == 'datarequest') {
        ds.getList({'url': 'relationships'}, function(list) {
            list.prefetch();
        });
    }
    _postsave(item, result, conf);
};

// Customize inverserelationship items auto-generated for new datarequests
var iropts = app.attachmentTypes.inverserelationship;
 
// Only show relationship types valid for the selected webservice
iropts.getTypeFilter = function(page, context) {
    if (page == 'datarequest')
        return _drRelTypeFilter(context);
    return {'to_type': page};
};

function _drRelTypeFilter(context) {
    var webservice = context.webservice.call(context),
        from_types = ['project'],
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
        'to_type': 'datarequest'
    };
}


// Limit site and parameter choices to the same authority as the webservice
// (e.g. only show Hydromet site codes for Hydromet webservices)
iropts.getChoiceListFilter = function(type, context) {
    var webservice;
    if (type.from_type == 'parameter' || type.from_type == 'site') {
        webservice = context.webservice.call(context);
        return {'authority_id': webservice.authority_id};
    }
    if (type.from_type == 'project') {
        return {'mine': true};
    }
    return {};
};

// Don't show authority identifiers for new projects
var idopts = app.attachmentTypes.identifier;
idopts.getTypeFilter = function(page, context) {
    /* jshint unused: false */
    if (page == 'project')
        return {'id': null};
    return {};
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
            $county = _getInput('county'),
            $project = _getInput('project'),
            $newproject = $page.find('.new-project'),
            $projname = $newproject.find('input');

        // Auto-filter county by state
        if ($state.length) {
            $state.change(_filterByState);
        }
        // Hide New Project text input if existing project is set
        if ($project.length && $projname.length) {
            $project.change(function() {
                if ($project.val()) {
                    $newproject.hide();
                    $projname.attr('required', false);
                } else {
                    $newproject.show();
                    $projname.attr('required', true);
                }
            });
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

function _listExists(url) {
    return ds.exists({'url': url, 'page': 1});
}

return {
    'setup': setup,
    'prefetch': prefetch,
    'toggle': toggle,
    'del': del,
    'setProject': setProject
};

});
