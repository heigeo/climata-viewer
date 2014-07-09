define(['wq/app', './login', './process', './config', './templates'],
function(app, login, process, config, templates) {

// Initialize wq/app and connect to auth events
app.init(config, templates);

login.setup();
process.setup();

});
