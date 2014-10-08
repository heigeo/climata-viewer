define(['jquery', 'wq/progress', 'wq/pages', 'wq/store', 'wq/map', './graph'],
function($, progress, pages, ds, map, graph) {

// Initialize data import progress bar
function setup() {
    progress.init('datarequests/<slug>/auto', onComplete, onFail, onProgress);
}

function onComplete($progress, data) {
    /* jshint unused: false */
    $progress.siblings('.message').html("Data successfully imported.");
    $progress.siblings('.complete').show();
    var id =_getId($progress);
    var $elems = $progress.siblings('svg');
    if (!id)
        return;

    ds.getList({'url': 'datarequests'}, _updateReqs);

    if ($elems.length) {
        $elems.show();
        graph.showData([id], $elems[0]);
    }

    function _updateReqs(list) {
        // Mark local copy of request as completed
        var req = list.find(id);
        if (!req)
            return;
        req.completed = true;
        req.completed_label = 'just now';
        list.update([req], 'id');

        // Mark any related projects as having data
        ds.getList({'url': 'inverserelationships'}, function(rels) {
            var prels = rels.filter(
                {'datarequest_id': req.id, 'item_page': 'project'}
            );
            prels.forEach(function(prel) {
                ds.getList({'url': 'projects'}, function(plist) {
                    var project = plist.find(prel.item_id);
                    if (!project) return;
                    project.has_data = true;
                    list.update([project], 'id');
                });
            });
        });
    }
}

function onFail($progress, data) {
    $progress.siblings('.message').html(
        "Error loading data:<br>" +
        "<pre><code>" + data.error + "</code></pre>"
    );
    $progress.siblings('.retry').show();
}

function onProgress($progress, data) {
    $progress.siblings('.message').html(data.message || "");
    var id = _getId($progress);
    var last = $progress.data('last-current') || 0;
    if (!id)
        return;

    if (data.stage == "data" && !$progress.data('map-inited')) {
        var $map = $progress.siblings('.map');
        $map.show();
        map.config.maps.datarequest.div = $map[0];
        map.createMap('datarequest', id);
        delete map.config.maps.datarequest.div;
        $progress.data('map-inited', true);
    }

    var $elems = $progress.siblings('svg');
    if (data.stage == "data" && $elems.length && data.current >= last + 100) {
        $elems.show();
        graph.showData([id], $elems[0]);
        $progress.data('last-current', data.current);
    }

    if (data.action) {
        var url = "datarequests/" + id + "/" + data.action;
        ds.getList({'url': 'datarequests'}, function(list) {
            var context = $.extend({'result': data}, list.find(id));
            pages.go(url, 'datarequest_' + data.action, context);
        });
    }
}

function _getId($progress) {
    var url = $progress.data('url');
    var match = url.match(/\/datarequests\/(\d+)\/status/);
    if (match)
        return match[1];
}

return {'setup': setup};

});
