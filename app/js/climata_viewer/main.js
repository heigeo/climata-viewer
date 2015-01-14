define(['jquery', 'wq/app', 'wq/autocomplete',
        './login', './process', './graph', './maps', './layers',
        './config', 'data/templates'],
function($, app, auto, login, process, graph, maps, layers,
         config, templates) {

// Initialize wq/app and connect to auth events
app.init(config, templates);
auto.init(templates.autocomplete);

login.setup();
process.setup();
graph.setup();
maps.setup();
layers.setup();

app.jqmInit();

$('document').ready(login.prefetch);

});
