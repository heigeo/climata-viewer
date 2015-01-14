from climata.version import VERSION
from django.conf import settings


color_index = -1


def climata_version(request):
    return {'climata_version': VERSION}


def reset_color(request):
    global color_index
    color_index = -1
    return {}


def get_color(request):
    def next_color():
        global color_index
        color_index += 1
        if color_index > len(settings.COLOR_NAMES) - 1:
            color_index = 0
        return settings.COLOR_NAMES[color_index]
    return {'get_color': next_color}
