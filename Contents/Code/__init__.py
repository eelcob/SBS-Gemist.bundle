# -*- coding: utf-8 -*
PLUGIN_TITLE	= L('Title')

ART				= 'art-default.jpg'
ICON			= 'icon-default.png'
ICON_SEARCH		= 'icon-search.png'
ICON_MORE		= 'icon-more.png'

PROGRAMLINK		= '/ajax/programFilter/day/0/genre/all/block/programs/range/'
VIDEOMATCH		= Regex("(.*?)videos(.*?)")

CHANNEL_ORDER      = ('NET 5', 'SBS 6', 'Veronica')
CHANNELS = {
	'NET 5': {
		'base': 'http://www.net5.nl',
		'art': 'art-net5.png',
		'icon': 'icon-net5.png',
	},
	'SBS 6': {
		'base': 'http://www.sbs6.nl',
		'art': 'art-sbs6.png',
		'icon': 'icon-sbs6.png'
	},
	'Veronica': {
		'base': 'http://www.veronicatv.nl',
		'art': 'art-veronica.png',
		'icon': 'icon-veronica.png'
	}
}

###################################################################################################
def Start():
	Plugin.AddPrefixHandler('/video/sbsgemist', MainMenu, PLUGIN_TITLE, ICON, ART)
	Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
	Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
	
	ObjectContainer.title1 = PLUGIN_TITLE
	ObjectContainer.view_group = 'List'
	ObjectContainer.art = R(ART)	

	VideoClipObject.thumb = R(ICON)
  
	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) Gecko/20100101 Firefox/13.0.1'

###################################################################################################
def MainMenu():

	oc = ObjectContainer()

	for kanaal in CHANNEL_ORDER:
		oc.add(DirectoryObject(key = Callback(CatagoryListing, kanaal=kanaal), title=kanaal, thumb=R(CHANNELS[kanaal]['icon']), art=R(CHANNELS[kanaal]['art'])))

	return oc

####################################################################################################
def CatagoryListing(kanaal):
	oc = ObjectContainer(title2=kanaal)
	
	oc.add(DirectoryObject(key = Callback(Episode, title='popular', kanaal=kanaal), title=L('Popular'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='0-9', kanaal=kanaal), title=L('StartingWith') + " " + L('09'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='ABC', kanaal=kanaal), title=L('StartingWith') + " " + L('ABC'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='DEF', kanaal=kanaal), title=L('StartingWith') + " " + L('DEF'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='GHI', kanaal=kanaal), title=L('StartingWith') + " " + L('GHI'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='JKL', kanaal=kanaal), title=L('StartingWith') + " " + L('JKL'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='MNO', kanaal=kanaal), title=L('StartingWith') + " " + L('MNO'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='PQR', kanaal=kanaal), title=L('StartingWith') + " " + L('PQR'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='STUV', kanaal=kanaal), title=L('StartingWith') + " " + L('STUV'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='WXYZ', kanaal=kanaal), title=L('StartingWith') + " " + L('WXYZ'), art=R(CHANNELS[kanaal]['art'])))
	
	return oc
	
###################################################################################################
def Episode(title, kanaal):
	oc = ObjectContainer()

	url  = CHANNELS[kanaal]['base'] + PROGRAMLINK + title
	try:
		page = HTML.ElementFromURL(url)
	except:
		page = ""
		pass

	div_main = page.xpath('//div[starts-with(@class, "i iGrid")]')
	
	for div in div_main:
		stream_name = div.xpath('./div/h2/a')[0].text
		stream_id   = CHANNELS[kanaal]['base'] + div.xpath('./div/h2/a')[0].get('href')
		url = stream_id + '/videos'	
		
		#test if the page is actually there 
		try:
			data = HTTP.Request(url, cacheTime=0).headers
		except:
			continue
			
		oc.add(DirectoryObject(key = Callback(GetShows, kanaal=kanaal, url=url), title=stream_name, art=R(CHANNELS[kanaal]['art'])))
		
	if len(oc) == 0:
		oc = ObjectContainer(header = L('NoVideo'), message = L('NoClips'))
		
	return oc	
	
###################################################################################################
def GetShows(kanaal, url):
	oc = ObjectContainer()

	page = HTML.ElementFromURL(url)
	try:
		style = page.xpath('//section[@class="s ajax"]/header/h1')[0].text
	except:
		oc = ObjectContainer(header = "Clip Error", message = "No clips found")
		style = ""
		div_main = []
		
	if style == 'Clips':
		div_main = page.xpath('//section[@class="s ajax"]/div/div/div[@class="i iBorder"]')
	elif style == 'Afleveringen':
		div_main = page.xpath('//div[@class="i iGuide iGuideSlider"]') 

	for episodes in div_main:
		if style == 'Clips':
			episode_name = str(episodes.xpath('./div/h2/a')[0].text)
			episode_id =  str(CHANNELS[kanaal]['base'] + episodes.xpath('./a')[0].get('href'))
			episode_thumb = str(CHANNELS[kanaal]['base'] + episodes.xpath('./a/img')[0].get('src'))
		elif style == 'Afleveringen':
			episode_name = str(episodes.xpath('./div/h2')[0].text)
			episode_id =  str(CHANNELS[kanaal]['base'] + episodes.xpath('./a')[0].get('href'))
			episode_thumb = str(CHANNELS[kanaal]['base'] + episodes.xpath('./a/img')[0].get('src'))
		else:
			continue

		video = VIDEOMATCH.match(episode_id)
		
		if video:
			Log('video found')
		else:
			continue
		
		oc.add(VideoClipObject(
			url = episode_id,
			title = episode_name,
			thumb=Resource.ContentsOfURLWithFallback(url=episode_thumb, fallback=CHANNELS[kanaal]['icon'])
			#thumb=Resource.ContentsOfURLWithFallback(url=episode_thumb, fallback=R(CHANNELS[kanaal]['icon']))	
		))
	
	if len(page.xpath('//div[@class="pager"]')) > 0:
		count = len(page.xpath('//div[@class="pager"]/ul/li[@class]'))
		currentpage = page.xpath('//div[@class="pager"]/ul/li[@class="active"]/a')[0].get('href')
		link, pagenr = currentpage.split('page/')
		pagenr = int(pagenr)

		if pagenr == count:
			Log('end of pages reached')
		else:	
			pagenr = pagenr + 1
			pagenr = str(pagenr)
			url = 	CHANNELS[kanaal]['base'] + 	link + "page/" + pagenr
			oc.add(DirectoryObject(key=Callback(GetShows, kanaal=kanaal, url=url), title=L('More'), thumb=R(ICON_MORE), art=R(CHANNELS[kanaal]['art'])))
	
	return oc