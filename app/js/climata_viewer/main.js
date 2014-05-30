define(['wq/app', 'wq/store', 'wq/progress', './config', './templates'],
function(app, ds, progress, config, templates) {

app.init(config, templates);
progress.init('datarequests/<slug>/data', onComplete);

['webservices', 'datarequests'].forEach(function(name) {
    ds.prefetch({'url': name});
});

function onComplete($progress, data) {
    $progress.siblings('.complete').show();
}

});
