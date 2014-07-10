define(['jquery', 'wq/progress', 'wq/pages', 'wq/store', './graph'],
function($, progress, pages, ds, graph) {

// Initialize data import progress bar
function setup() {
    progress.init('datarequests/<slug>/auto', onComplete, onFail, onProgress);
}

function onComplete($progress, data) {
    /* jshint unused: false */
    $progress.siblings('.complete').show();
    var id =_getId($progress);
    var elems = $progress.siblings('svg');
    if (id && elems.length)
        graph.showData(id, elems[0]);
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
    if (data.action && id) {
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
