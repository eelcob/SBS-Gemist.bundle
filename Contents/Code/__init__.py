# -*- coding: utf-8 -*
PLUGIN_TITLE	= L('Title')

ART				= 'art-default.jpg'
ICON			= 'icon-default.png'
ICON_SEARCH		= 'icon-search.png'
ICON_MORE		= 'icon-more.png'

PROGRAMLINK		= '/ajax/programFilter/day/0/genre/all/block/programs/range/'
GENRELINK		= '/ajax/programFilter/range/popular/day/0/block/gemist/genre/'
DAYLINK			= '/ajax/programFilter/range/popular/genre/all/block/gemist/day/'
#RECENTURL		= '/gemist'
RECENTURL		= '/ajax/VideoNewPopular/nameprogram//page/'

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
		oc.add(DirectoryObject(key = Callback(OptionPicker, kanaal=kanaal), title=kanaal, thumb=R(CHANNELS[kanaal]['icon']), art=R(CHANNELS[kanaal]['art'])))
	
	return oc

####################################################################################################
def OptionPicker(kanaal):	
	oc = ObjectContainer(title2=kanaal)	
	
	oc.add(DirectoryObject(key = Callback(NameList, kanaal=kanaal), title=L('Programs via name'), thumb=R(CHANNELS[kanaal]['icon']), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(GenreList, kanaal=kanaal), title=L('Programs via genre'), thumb=R(CHANNELS[kanaal]['icon']), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Recent, kanaal=kanaal, url=CHANNELS[kanaal]['base'] + RECENTURL, pagenr=1), title=L('Recent'), thumb=R(CHANNELS[kanaal]['icon']), art=R(CHANNELS[kanaal]['art'])))
	
	return oc
	
####################################################################################################
def NameList(kanaal):
	oc = ObjectContainer(title2=kanaal)
	
	oc.add(DirectoryObject(key = Callback(Episode, title='popular', kanaal=kanaal, function='name'), title=L('Popular'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='0-9', kanaal=kanaal, function='name'), title=L('StartingWith') + " " + L('09'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='ABC', kanaal=kanaal, function='name'), title=L('StartingWith') + " " + L('ABC'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='DEF', kanaal=kanaal, function='name'), title=L('StartingWith') + " " + L('DEF'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='GHI', kanaal=kanaal, function='name'), title=L('StartingWith') + " " + L('GHI'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='JKL', kanaal=kanaal, function='name'), title=L('StartingWith') + " " + L('JKL'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='MNO', kanaal=kanaal, function='name'), title=L('StartingWith') + " " + L('MNO'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='PQR', kanaal=kanaal, function='name'), title=L('StartingWith') + " " + L('PQR'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='STUV', kanaal=kanaal, function='name'), title=L('StartingWith') + " " + L('STUV'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='WXYZ', kanaal=kanaal, function='name'), title=L('StartingWith') + " " + L('WXYZ'), art=R(CHANNELS[kanaal]['art'])))
	
	return oc

####################################################################################################
def GenreList(kanaal):
	oc = ObjectContainer(title2=kanaal)	

	oc.add(DirectoryObject(key = Callback(Episode, title='13', kanaal=kanaal, function='genre'), title=L('Amusement'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='12', kanaal=kanaal, function='genre'), title=L('Animation'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='4', kanaal=kanaal, function='genre'), title=L('Comedy'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='8', kanaal=kanaal, function='genre'), title=L('Consumer'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='10', kanaal=kanaal, function='genre'), title=L('Documentairy'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='17', kanaal=kanaal, function='genre'), title=L('Docusoap'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='5', kanaal=kanaal, function='genre'), title=L('Movie'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='1', kanaal=kanaal, function='genre'), title=L('Informative'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='11', kanaal=kanaal, function='genre'), title=L('Crime'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='9', kanaal=kanaal, function='genre'), title=L('Music'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='2', kanaal=kanaal, function='genre'), title=L('News'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='7', kanaal=kanaal, function='genre'), title=L('Other'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='16', kanaal=kanaal, function='genre'), title=L('Reality'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='3', kanaal=kanaal, function='genre'), title=L('Religion'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='14', kanaal=kanaal, function='genre'), title=L('Shows'), art=R(CHANNELS[kanaal]['art'])))
	oc.add(DirectoryObject(key = Callback(Episode, title='15', kanaal=kanaal, function='genre'), title=L('Sport'), art=R(CHANNELS[kanaal]['art'])))

	return oc

###################################################################################################
def Recent(kanaal, url, pagenr):
	oc = ObjectContainer()

	urlpage = url + str(pagenr)
	
	page = HTML.ElementFromURL(urlpage)
	recentclips = page.xpath('//div[@class="sBody"]/div[@class="i iBorder"]')
	
	for clips in recentclips:
		clip_title 	= clips.xpath('./div/h2/a')[0].text
		clip_link 	= str(CHANNELS[kanaal]['base'] + clips.xpath('./div/h2/a')[0].get('href'))
		clip_thumb 	= str(CHANNELS[kanaal]['base'] + clips.xpath('./a/img')[0].get('src'))	
		try:
			clip_date	= clips.xpath('./div/p/a')[1].text
		except:
			clip_date 	= "00 / 00"
		
		clip_date, clip_length = clip_date.split('/')
		clip_length = clip_length.replace('min', '')
		clip_length = TimeToMilliseconds(time=clip_length)
		
		oc.add(VideoClipObject(
			url = clip_link,
			title = clip_title,
			duration = clip_length,
			thumb=Resource.ContentsOfURLWithFallback(url=clip_thumb, fallback=CHANNELS[kanaal]['icon'])
		))
		
	pagenr = int(pagenr)
	pagenr = pagenr + 1
	oc.add(DirectoryObject(key=Callback(Recent, kanaal=kanaal, url=url, pagenr=pagenr), title=L('More'), thumb=R(ICON_MORE), art=R(CHANNELS[kanaal]['art'])))
		
	return oc	
		
###################################################################################################
def Episode(title, kanaal, function):
	oc = ObjectContainer()
	
	if function == 'name':
		url = CHANNELS[kanaal]['base'] + PROGRAMLINK + title
	else:
		url = CHANNELS[kanaal]['base'] + GENRELINK + title
		
	try:
		page = HTML.ElementFromURL(url)
	except:
		page = ""
		pass

	div_main = page.xpath('//div[starts-with(@class, "i iGrid")]')
	
	for div in div_main:
		stream_name = div.xpath('./div/h2/a')[0].text
		stream_id   = CHANNELS[kanaal]['base'] + div.xpath('./div/h2/a')[0].get('href')
		
		if stream_id.find('/videos') == -1:
			url = stream_id + '/videos'	
		else:
			url = stream_id
		
		#test if the page is actually there a couple of pages have no video link
		try:
			data = HTTP.Request(url, cacheTime=0).headers
		except:
			continue

		oc.add(DirectoryObject(key = Callback(GetCatagory, kanaal=kanaal, url=url), title=stream_name, art=R(CHANNELS[kanaal]['art'])))
		
	if len(oc) == 0:
		oc = ObjectContainer(header = L('NoVideo'), message = L('NoClips'))
		
	return oc	

###################################################################################################
def GetCatagory(kanaal, url):
	oc = ObjectContainer()

	page = HTML.ElementFromURL(url)
	try:
		style = page.xpath('//section[@class="s ajax"]/header/h1')
		for num in range(len(style)):
			oc.add(DirectoryObject(key = Callback(GetShows, kanaal=kanaal, url=url, style=style[num].text), title=style[num].text, art=R(CHANNELS[kanaal]['art'])))
	except:
		oc = ObjectContainer(header = L('NoVideo'), message = L('NoClips'))
		
	return oc	
	
###################################################################################################
def GetShows(kanaal, url, style):
	oc = ObjectContainer()

	page = HTML.ElementFromURL(url)	
	seasons	 	= ""
	
	### Set the xpath per call, clips and parsed return videos, afleveringen hits the season list
	if style == 'Clips':
		div_main 	= page.xpath('//section[@class="s ajax"]/div/div/div[@class="i iBorder"]')	
	elif style == 'Parsed':
		div_main 	= page.xpath('//div[@class="i iGuide iGuideSlider"]') 		
	elif style == 'Afleveringen':
		seasons  	= page.xpath('//div[@class="subMenu"]/ul/li') 
		div_main 	= page.xpath('//div[@class="i iGuide iGuideSlider"]') 		
	else:
		oc = ObjectContainer(header = L('NoVideo'), message = L('NoClips'))
		return oc
		
	### Test for full season links and display a container per season	
	if seasons:
		try:
			for season in seasons:
				slink = season.xpath('./a')[0].get('href')
				stext = season.xpath('./a')[0].text
				oc.add(DirectoryObject(key = Callback(GetShows, kanaal=kanaal, url=str(CHANNELS[kanaal]['base'] + slink), style='Parsed'), title=stext, art=R(CHANNELS[kanaal]['art'])))
			return oc
		except:
			pass
	else:	
		for episodes in div_main:
			if style == 'Clips':
				episode_name = str(episodes.xpath('./div/h2/a')[0].text)
				episode_id =  str(CHANNELS[kanaal]['base'] + episodes.xpath('./a')[0].get('href'))
				episode_thumb = str(CHANNELS[kanaal]['base'] + episodes.xpath('./a/img')[0].get('src'))
				try:
					clip_date	= episodes.xpath('./div/p/a')[1].text
				except:
					clip_date 	= "00 / 00:00"			
			elif style == 'Parsed':
				episode_name = str(episodes.xpath('./div/h2')[0].text)
				episode_id =  str(CHANNELS[kanaal]['base'] + episodes.xpath('./a')[0].get('href'))
				episode_thumb = str(CHANNELS[kanaal]['base'] + episodes.xpath('./a/img')[0].get('src'))
				try:
					clip_date	= episodes.xpath('./div/p')[0].text
				except:
					clip_date 	= "00 / 00:00"
			elif style == 'Afleveringen':
				episode_name = str(episodes.xpath('./div/h2')[0].text)
				episode_id =  str(CHANNELS[kanaal]['base'] + episodes.xpath('./a')[0].get('href'))
				episode_thumb = str(CHANNELS[kanaal]['base'] + episodes.xpath('./a/img')[0].get('src'))
				try:
					clip_date	= episodes.xpath('./div/p')[0].text
				except:
					clip_date 	= "00 / 00:00"
			else:
				continue

			clip_date, clip_length = clip_date.split('/')
			clip_length = clip_length.replace('min', '')
			clip_length = TimeToMilliseconds(time=clip_length)
			
			video = VIDEOMATCH.match(episode_id)
		
			if not video:
				continue
		
			oc.add(VideoClipObject(
				url = episode_id,
				title = episode_name,
				duration = clip_length,
				thumb=Resource.ContentsOfURLWithFallback(url=episode_thumb, fallback=CHANNELS[kanaal]['icon'])
			))
	
		### Test for multiple pages on the clips screen and display a more button if there a more clips
		if style == 'Clips':
			if len(page.xpath('//div[@class="pager"]')) > 0:
				count = len(page.xpath('//div[@class="pager"]/ul/li[@class]'))
				currentpage = page.xpath('//div[@class="pager"]/ul/li[@class="active"]/a')[0].get('href')
				link, pagenr = currentpage.split('page/')
				pagenr = int(pagenr)
				if not pagenr == count:
					pagenr = pagenr + 1
					pagenr = str(pagenr)
					url = 	CHANNELS[kanaal]['base'] + 	link + "page/" + pagenr
					oc.add(DirectoryObject(key=Callback(GetShows, kanaal=kanaal, url=url, style='Clips'), title=L('More'), thumb=R(ICON_MORE), art=R(CHANNELS[kanaal]['art'])))
	
	return oc
	
###################################################################################################	
def TimeToMilliseconds(time):

	milliseconds  = 0
	duration = time.split(':')
	duration.reverse()

	for i in range(0, len(duration)):
		milliseconds += int(duration[i]) * (60**i) * 1000

	return milliseconds