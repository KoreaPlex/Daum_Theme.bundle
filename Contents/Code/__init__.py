#Plex Theme Music
import unicodedata
import re, time, unicodedata, hashlib, types , random
THEME_URL = 'https://tvthemes.plexapp.com/%s.mp3'
try:
  server_url = Prefs['server_url']
  if Prefs['server_url'] != "" and Prefs['server_url'][-1] == '/':
    Log('Server Url has an error. correct it : %s' % server_url)
    server_url = Prefs['server_url'][:-1]
except:
  server_url = 'http://103.208.222.5:34567'


def Start():
  HTTP.CacheTime = None
  HTTP.Headers[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
  HTTP.Headers['Accept-Language'] = 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'



def safe_unicode(s, encoding='utf-8'):
  if s is None:
    return None
  if isinstance(s, basestring):
    if isinstance(s, types.UnicodeType):
      return s
    else:
      return s.decode(encoding)
  else:
    return str(s).decode(encoding)




class DaumTheme(Agent.TV_Shows):
  name = 'Daum Theme'
  languages = [Locale.Language.NoLanguage]
  primary_provider = False
  accepts_from = ['com.plexapp.agents.localmedia', 'com.plexapp.agents.sj_daum']
  contributes_to = ['com.plexapp.agents.sj_daum']
  def search(self, results, media, lang):
    Log(media.primary_agent)
    self.genres = []
    if  media.primary_agent in ['com.plexapp.agents.sj_daum']:
      Log(str(media.primary_metadata.id))
      self.genres = [str(item) for item in media.primary_metadata.genres]
      results.Append(MetadataSearchResult(
        id=media.primary_metadata.id,
        score=100
      ))

  def update(self, metadata, media, lang, force=False):
    Log(str(media.title))
    Log(str(metadata.title))
    Log(self.genres)
    for item in self.genres:
      Log(str(item))
      Log(item.encode('utf-8'))
    try:
      tmp = JSON.ObjectFromURL(server_url + '/theme', values=dict(keyword=media.title , id=metadata.id , cacheTime=0 ,apikey = Prefs['apikey'] , genre=str(self.genres[0]) if len(self.genres) > 0 else ""))['result']
    except:
      tmp = None
      pass
    prefer_time = Prefs['prefer_time'].split(',')
    prefer_time = [(int(item) - 10)/10 for item in prefer_time]
    Log(str(prefer_time))

    Log(str(tmp))
    if tmp:
      for index in prefer_time:
        if tmp[index].count('http') == 0 : continue
        url = tmp[index]
        metadata.themes[THEME_URL % str(random.randint(10000000,99999999))+metadata.id] = Proxy.Media(HTTP.Request(str(url)))
        Log('Get theme music... %s' % str(url))
        break
