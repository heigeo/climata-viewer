define(['jquery', 'wq/app', 'wq/autocomplete',
        './login', './process', './graph', './map',
        './config', './templates'],
function($, app, auto, login, process, graph, map, config, templates) {

// Initialize wq/app and connect to auth events
app.init(config, templates);
auto.init(templates.autocomplete);

login.setup();
process.setup();
graph.setup();
map.setup();

$('document').ready(function() {
    graph.showLatest();
    login.prefetch();
});

});
