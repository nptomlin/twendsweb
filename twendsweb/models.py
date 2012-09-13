import logging
import json as json
import pyramid.compat as html

log = logging.getLogger(__name__)

class RootModel(object):
    __name__ = None
    __dotted_path__ = 'jobs.uk'
    __parent__ = None
    __redis__ = None
    __dict__ = None
    
    
    def __init__(self, request):
        self.__redis__ = request.redis
        
    def __getitem__(self, name):
        #test if context
        exists = None
        lowerName = _fix_name(name.lower())
        #dotted_path = self.__dotted_path__ + '.' + lowerName
        dotted_path = lowerName # use canonical path for laters
        log.debug(dotted_path + ' resource requested')
        if(self.__redis__.sismember('categories', dotted_path)):
            context = Node(dotted_path, self.__redis__)
            _assign(context, name, self)
            log.debug(context.__dotted_path__)
            log.debug(context.__name__)
        else:
            log.debug('No resource found')
            raise KeyError()        
        return context


class Node:
    __name__=None
    __parent__=None
    __redis__= None
    __dotted_path__ = None
    
    def __init__(self, dotted_path, redis):
        self.__dotted_path__ = dotted_path
        self.__redis__ = redis
        
    def __len__(self):
        return self.__redis__.llen(self.__dotted_path__)

    def __iter__(self):
        return (  _fixup_tweet(x) for x in self.__redis__.lrange(self.__dotted_path__, 0, -1)  )
        #return ( _assign(Post(x), str(x['_id']), self) for x in self.collection.find().sort('updated', DESCENDING) )

    def __getitem__(self, name):
        #test if exists
        context = None
        lowerName = _fix_name(name.lower())
        dotted_path = self.__dotted_path__ + '.' + lowerName
        log.debug(dotted_path + ' resource requested')
        if(self.__redis__.sismember('categories', dotted_path)):
            context = Node(dotted_path, self.__redis__)
            _assign(context, name, self)
            log.debug(context.__dotted_path__)
            log.debug(context.__name__)
        else:
            log.debug('No resource found')
            raise KeyError()        
        return context

def _assign(obj, name, parent):
    obj.__name__ = name
    obj.__parent__ = parent
    return obj

def _fix_name(name):
    return 'c#' if name == 'c_sharp' else name

def _fixup_tweet(obj):
    tweet = json.loads(obj)
    return _hydrate_tweet(tweet)

def _hydrate_tweet(tweet):
    text = tweet['text']
    text_pointer = 0
    tail = ''
    new_text = ''
    if('urls' in tweet and tweet['urls']):
        urls = sorted(tweet['urls'], key=lambda url: url['indices'][0])
        for url in urls:
            start, stop = url['indices']
            actual_url = url['url']
            new_text += text[:start] if text_pointer == 0 else text[text_pointer:start]
            new_text += _get_link(actual_url)
            tail = text[stop:]
            text_pointer = stop
        new_text += tail
    tweet['text'] = new_text
    return tweet

def _get_link(url):
    return '<a href=\'{0}\' >{0}</a>'.format(url)  

def get_root(environ):
    return RootModel(environ)
