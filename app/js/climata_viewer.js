requirejs.config({
    'baseUrl': '/js/lib',
    'paths': {
        'climata_viewer': '../climata_viewer',
        'data': '../data/',
        'db': '../../'
    }
});

requirejs(['climata_viewer/main']);
