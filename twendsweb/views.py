import logging

from pyramid.i18n import TranslationStringFactory



_ = TranslationStringFactory('twends-web')

log = logging.getLogger(__name__)

def my_view(request):
    return {'project':'twends-web'}
    
def view(context, request):
    log.debug("stuff")
    return dict( context=context, project='twends-web')
