define(['wq/app', './login', './process', './graph',
        './config', './templates'],
function(app, login, process, graph, config, templates) {

// Initialize wq/app and connect to auth events
app.init(config, templates);

login.setup();
process.setup();
graph.setup();

});
