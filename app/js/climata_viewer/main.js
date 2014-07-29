define(['wq/app', 'wq/autocomplete', './login', './process', './graph',
        './config', './templates'],
function(app, auto, login, process, graph, config, templates) {

// Initialize wq/app and connect to auth events
app.init(config, templates);
auto.init(templates.autocomplete);

login.setup();
process.setup();
graph.setup();

});
