from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory
from twendsweb.models import get_root
import redis

def main(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'twends-web')

    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    config = Configurator(root_factory=get_root, settings=settings, session_factory = my_session_factory)


    config.add_translation_dirs('locale/')
    config.include('pyramid_jinja2')

    config.add_static_view('static', 'static')
    
    config.add_view('twendsweb.views.my_view',
                    context='twendsweb.models.RootModel', 
                    renderer='mytemplate.jinja2')
    
    config.add_view('twendsweb.views.view',
            #name='node_view',
            context='twendsweb.models.Node', 
            renderer='tweets.jinja2')
    
    config.add_subscriber(add_redis,
                      'pyramid.events.NewRequest')
    
    return config.make_wsgi_app()
    
def add_redis(event):
    settings = event.request.registry.settings
    #event.request.redis = event.request.registry.mongo_con[settings['db_name']]
    event.request.redis = redis.StrictRedis(host='192.168.86.132')    
