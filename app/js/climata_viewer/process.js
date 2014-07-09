define(['jquery', 'wq/progress', 'wq/pages', 'wq/store'],
function($, progress, pages, ds) {

// Initialize data import progress bar
function setup() {
    progress.init('datarequests/<slug>/auto', onComplete, onFail, onProgress);
}

function onComplete($progress, data) {
    /* jshint unused: false */
    $progress.siblings('.complete').show();
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

return {'setup': setup};

});
