import unittest
from pyramid import testing
from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('twendsweb')


class ViewTests(unittest.TestCase):

    def setUp(self):
        testing.setUp()
        
    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from twendsweb.views import my_view
        request = testing.DummyRequest()
        response = my_view(request)
        self.assertEqual(response['project'], 'twends-web')


class ModelTests(unittest.TestCase):

    def setUp(self):
        testing.setUp()
        
    def tearDown(self):
        testing.tearDown()

    def test_hydrate_tweet(self):
        from twendsweb.models import _hydrate_tweet
        test_string = "nocompany: Lead .NET Developer (Not Specified, London) http://t.co/lENwcjmo\n  http://t.co/tttt\n #Jobs"
        urls = [    { "indices": [55, 75],"url": "http://t.co/lENwcjmo"  },
                    { "indices": [78, 94],"url": "http://t.co/tttt"  } ]
        tweet = { 'text':test_string, 'urls':urls }  
        _hydrate_tweet(tweet)
        self.assertEqual("nocompany: Lead .NET Developer (Not Specified, London) <a href='http://t.co/lENwcjmo' >http://t.co/lENwcjmo</a>\n  <a href='http://t.co/tttt' >http://t.co/tttt</a>\n #Jobs", tweet['text'])
