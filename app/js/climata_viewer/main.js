define(['wq/app', 'wq/progress', './config', './templates'],
function(app, progress, config, templates) {

app.init(config, templates);
progress.init('datarequests/<slug>/data', onComplete);

function onComplete($progress, data) {
    $progress.siblings('.complete').show();
}

});
