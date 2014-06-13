from climata.version import VERSION


def climata_version(request):
    return {'climata_version': VERSION}
