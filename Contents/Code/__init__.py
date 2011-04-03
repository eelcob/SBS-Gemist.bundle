# -*- coding: utf-8 -*-
import re

###################################################################################################

PLUGIN_TITLE = 'SBS Gemist'

CHANNELS = {
  'NET 5': {
    'base': 'http://www.net5.nl',
    'home': '/web/show/id=1017155',
    'art': 'art-net5.png',
    'icon': 'icon-net5.png'
  },
  'SBS 6': {
    'base': 'http://www.sbs6.nl',
    'home': '/web/show/id=985609',
    'art': 'art-sbs6.png',
    'icon': 'icon-sbs6.png'
  },
  'Veronica': {
    'base': 'http://www.veronicatv.nl',
    'home': '/web/show/id=997234',
    'art': 'art-veronica.png',
    'icon': 'icon-veronica.png'
  }
}

CHANNEL_ORDER      = ('NET 5', 'SBS 6', 'Veronica')
SILVERLIGHT_PLAYER = 'http://www.plexapp.com/player/silverlight.php?stream=%s&width=%s&height=%s'

# 2 programmes haven't got episodes, instead the menu item links directly to the latest episode (local 'news' and weather)
DIFFERENT          = ('Hart van Nederland', 'Piets Weerbericht')

# XPATH_PROGRAMS_PAGES is so specific to prevent capturing the wrong pagination navigation
XPATH_PROGRAMS     = '//h3[contains(.,"Programma Gemist overzicht") or contains(.,"Programma gemist overzicht")]/parent::div/parent::div//span[@class="title"]/a[@href]'
XPATH_EPISODES     = '//div[@class="block-large"]//div[contains(@class,"item")]'

# Art and icons
ART_DEFAULT        = 'art-default.jpg'
ICON_DEFAULT       = 'icon-default.png'
ICON_MORE          = 'icon-more.png'

###################################################################################################

def Start():
  Plugin.AddPrefixHandler('/video/sbsgemist', MainMenu, PLUGIN_TITLE, ICON_DEFAULT, ART_DEFAULT)
  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

  # Set the default MediaContainer attributes
  MediaContainer.title1    = PLUGIN_TITLE
  MediaContainer.viewGroup = 'List'
  MediaContainer.art       = R(ART_DEFAULT)

  # Set the default cache time
  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16'

###################################################################################################

def MainMenu():
  dir = MediaContainer()

  for c in CHANNEL_ORDER:
    dir.Append(Function(DirectoryItem(Programs, title=c, thumb=R(CHANNELS[c]['icon']), art=R(CHANNELS[c]['art'])), c=c))

  return dir

####################################################################################################

def Programs(sender, c):
  dir = MediaContainer(title2=c, art=R(CHANNELS[c]['art']))
  url = CHANNELS[c]['base'] + CHANNELS[c]['home']

  for programme in HTML.ElementFromURL(url, errors='ignore').xpath(XPATH_PROGRAMS):
    title = programme.xpath('./text()')[0].strip()

    # Filter out Wimbledon stuff for Net 5
    if title.find('Wimbledon') == -1:
      programme_url = programme.get('href')

      if title in DIFFERENT:
        dir.Append(Function(VideoItem(PlayVideo, title=title, thumb=R(CHANNELS[c]['icon'])), url=programme_url))
      else:
        dir.Append(Function(DirectoryItem(Episodes, title=title, thumb=R(CHANNELS[c]['icon'])), title=title, url=CHANNELS[c]['base'] + programme_url, c=c))

  if len(dir) == 0:
    return MessageContainer('Geen items', 'Deze directory is leeg')
  else:
    return dir

####################################################################################################

def Episodes(sender, title, url, c):
  dir = MediaContainer(viewGroup='InfoList', title2=title, art=R(CHANNELS[c]['art']))

  for episode in HTML.ElementFromURL(url, errors='ignore').xpath(XPATH_EPISODES):
    ep_title = episode.xpath('./div[@class="title"]/a/span')[0].text
    airtime = episode.xpath('./div[@class="airtime"]/a/span')[0].text
    summary = episode.xpath('./div[@class="text"]/a/span')[0].text
    thumb = CHANNELS[c]['base'] + episode.xpath('./div[@class="thumb"]/a/img')[0].get('src')
    ep_url = CHANNELS[c]['base'] + episode.xpath('./div[@class="title"]/a')[0].get('href')
    dir.Append(Function(VideoItem(PlayVideo, title=ep_title, subtitle=airtime, summary=summary, thumb=Function(GetThumb, url=thumb, alt=CHANNELS[c]['icon'])), url=ep_url))

  next = HTML.ElementFromURL(url, errors='ignore').xpath('//span[@class="next"]/a')
  if len(next) == 1:
    next_url = CHANNELS[c]['base'] + next[0].get('href')
    dir.Append(Function(DirectoryItem(Episodes, title='Meer...', thumb=R(ICON_MORE)), title=title, url=next_url, c=c))

  if len(dir) == 0:
    return MessageContainer('Geen items', 'Deze directory is leeg')
  else:
    return dir

####################################################################################################

def PlayVideo(sender, url):
  content = HTTP.Request(url, cacheTime=0).content
  content = HTTP.Request(url, cacheTime=0).content # Intentionally!

  # Almost all videos on the website are in Windows Media format (Silverlight), except for a couple program that have Flash videos
  # The Silverlight stuff uses the Silverlight player on plexapp.com, for the Flash stuff links to the .flv files are looked up
  vid = re.compile('(http://asx.sbsnet.nl/(.+?)\.(wmv|asx))').findall(content, re.DOTALL)
  if len(vid) > 0:
    url = String.Quote(vid[0][0], usePlus=True)
    return Redirect(WebVideoItem( SILVERLIGHT_PLAYER % (url, '424', '240') ))
  else:
    vid = re.compile('(http://playlist.sbsnet.nl/flv/(.+?))"').findall(content, re.DOTALL)
    if len(vid) > 0:
      playlist = HTTP.Request(vid[0][0], errors='ignore').content
      vid = re.compile('<location>(.+?)</location>').findall(playlist, re.DOTALL)
      if len(vid) > 0:
        return Redirect(vid[0])
  return None

####################################################################################################

def GetThumb(url, alt):
  try:
    data = HTTP.Request(url, cacheTime=CACHE_1MONTH).content
    return DataObject(data, 'image/jpeg')
  except:
    pass
  return Redirect(R(alt))
