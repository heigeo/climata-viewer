requirejs.config({
    'baseUrl': '/js/lib',
    'paths': {
        'climata_viewer': '../climata_viewer',
        'db': '../../'
    }
});

requirejs(['climata_viewer/main']);
