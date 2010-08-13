# -*- coding: utf-8 -*-
from PMS import *
import re

###################################################################################################

PLUGIN_TITLE                = 'SBS Gemist'
PLUGIN_PREFIX               = '/video/sbsgemist'

CHANNELS = {
  'NET5': {
    'base': 'http://www.net5.nl',
    'home': '/web/show/id=1017155',
    'art': 'art-net5.png',
    'icon': 'icon-net5.png'
  },
  'SBS6': {
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

CHANNEL_ORDER               = ('NET5', 'SBS6', 'Veronica')
SILVERLIGHT_PLAYER          = 'http://www.plexapp.com/player/silverlight.php?stream=%s&width=%s&height=%s'

# 2 programs that haven't got episodes, instead the menu item links directly to the latest episode (local 'news' and weather)
DIFFERENT                   = ('Hart van Nederland', 'Piets Weerbericht')

# XPATH_PROGRAMS_PAGES is so specific to prevent capturing the wrong pagination navigation
XPATH_PROGRAMS              = '/html/body//h3[contains(.,"Programma Gemist overzicht") or contains(.,"Programma gemist overzicht")]/parent::div/parent::div//span[@class="title"]/a[@href]'
XPATH_EPISODES              = '/html/body//div[@class="block-large"]//div[contains(@class,"item")]'

# Art and icons
ART_DEFAULT                 = 'art-default.png'
ICON_DEFAULT                = 'icon-default.png'
ICON_MORE                   = 'icon-more.png'

###################################################################################################

def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, MainMenu, PLUGIN_TITLE, ICON_DEFAULT)
  Plugin.AddViewGroup('Category', viewMode='List', mediaType='items')
  Plugin.AddViewGroup('Details', viewMode='InfoList', mediaType='items')

  # Set the default MediaContainer attributes
  MediaContainer.title1    = PLUGIN_TITLE
  MediaContainer.viewGroup = 'Category'
  MediaContainer.art       = R(ART_DEFAULT)

  # Set the default cache time
  HTTP.SetCacheTime(CACHE_1HOUR)
  HTTP.SetHeader('User-agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6')

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

  content = XML.ElementFromURL(url, isHTML=True, errors='ignore')
  programs = content.xpath(XPATH_PROGRAMS)

  for p in programs:
    title = p.xpath('./text()')[0].strip()
    programUrl = p.get('href')

    if title in DIFFERENT:
      dir.Append(Function(VideoItem(PlayVideo, title=title, thumb=R(CHANNELS[c]['icon'])), url=programUrl))
    else:
      dir.Append(Function(DirectoryItem(Episodes, title=title, thumb=R(CHANNELS[c]['icon'])), title=title, url=CHANNELS[c]['base']+programUrl, c=c))

  return dir

####################################################################################################

def Episodes(sender, title, url, c):
  dir = MediaContainer(viewGroup='Details', title2=title, art=R(CHANNELS[c]['art']))

  eps = HTTP.Request(url, errors='ignore')
  episodes = XML.ElementFromString(eps, isHTML=True).xpath(XPATH_EPISODES)
  for episode in episodes:
    epTitle = episode.xpath('./div[@class="title"]/a/span')[0].text
    epAirtime = episode.xpath('./div[@class="airtime"]/a/span')[0].text
    epSummary = episode.xpath('./div[@class="text"]/a/span')[0].text
    epThumb = CHANNELS[c]['base'] + episode.xpath('./div[@class="thumb"]/a/img')[0].get('src')
    epUrl = CHANNELS[c]['base'] + episode.xpath('./div[@class="title"]/a')[0].get('href')
    dir.Append(Function(VideoItem(PlayVideo, title=epTitle, subtitle=epAirtime, summary=epSummary, thumb=epThumb), url=epUrl))

  next = XML.ElementFromString(eps, isHTML=True).xpath('/html/body//span[@class="next"]/a')
  if len(next) == 1:
    nextUrl = CHANNELS[c]['base'] + next[0].get('href')
    dir.Append(Function(DirectoryItem(Episodes, title='Meer ...', thumb=R(ICON_MORE)), title=title, url=nextUrl, c=c))

  return dir

####################################################################################################

def PlayVideo(sender, url):
  content = HTTP.Request(url, cacheTime=0)
  content = HTTP.Request(url, cacheTime=0) # Intentionally!

  # Almost all videos on the website are in Windows Media format (Silverlight), except for a couple program that have Flash videos
  # The Silverlight stuff uses the Silverlight player on plexapp.com, for the Flash stuff links to the .flv files are looked up
  vid = re.compile('(http://asx.sbsnet.nl/(.+?)\.(wmv|asx))').findall(content, re.DOTALL)
  if len(vid) > 0:
    url = String.Quote(vid[0][0], usePlus=True)
    return Redirect(WebVideoItem( SILVERLIGHT_PLAYER % (url, '424', '240') ))
  else:
    vid = re.compile('(http://playlist.sbsnet.nl/flv/(.+?))"').findall(content, re.DOTALL)
    if len(vid) > 0:
      playlist = HTTP.Request(vid[0][0], errors='ignore')
      vid = re.compile('<location>(.+?)</location>').findall(playlist, re.DOTALL)
      if len(vid) > 0:
        return Redirect(vid[0])
      else:
        return None
    else:
      return None
