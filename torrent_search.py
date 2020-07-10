from site_parser import common_parser
from datetime import date
from datetime import datetime

from urllib.parse   import quote
from urllib.request import urlopen

# 숫자만 꺼낸다. 이때 소숫점까지 지원하기위해서 . 까지 포함한 숫자만꺼냄
def get_number_only_1(input_str):
	text = re.sub('[^0-9.]', '', input_str)
	return text


def torrent_search(search_keyword) :

	idx_cnt = 0
	main_url = 'https://www.torrentdownloads.me'
	base_url = 'https://www.torrentdownloads.me/search/?search=+'

	torrent_info_arr = []

	search_keyword = search_keyword.replace(' ','-')
	search_keyword = quote(search_keyword)

	content_ctx = common_parser.get_content_bs4ctx(base_url + search_keyword)

	div_ctx = content_ctx.find('div', attrs={'id': 'main_wrapper'})

	divs = div_ctx.find_all('div', attrs={'class':'grey_bar3'})

	for div_one in divs :
		links = div_one.find_all('a')
		for link_one in links :
			title_str = str(link_one.get('title'))

			if title_str is None or title_str.find('View torrent info') < 0:
				continue

			link_str = str(link_one['href'])
			if link_str.find('http') >= 0 :
				# external ads link..
				continue

			link_str = common_parser.url_join(main_url, link_str)

			seed_infos = div_one.find_all('span', attrs={'class': None})

			torrent_info = {}
			torrent_info['title'] = link_one.get('title').replace('View torrent info : ', '')
			torrent_info['link'] = link_str
			torrent_info['seed'] = seed_infos[0].text + '/' + seed_infos[1].text 
			torrent_info['size'] = seed_infos[2].text

			torrent_info_arr.append(torrent_info)
			print('----------')
			print(torrent_info)

	return torrent_info_arr

def get_magnet_addr(target_url) :
	content_ctx = common_parser.get_content_bs4ctx(target_url)
	links = content_ctx.find_all('a')
	for link_one in links :
		link_str = str(link_one['href'])
		if link_str.find('magnet:') >= 0:
			return link_str
	return None

def _run_server():
	os.chdir(str(Path(MAIN_WORK_DIR).joinpath('django_site')))
	saved_argv = sys.argv
	sys.argv = ['./manage.py', 'runserver', my_setting.SERVER_IP + ':' + my_setting.SERVER_PORT]
	manage.main()


if __name__ == '__main__':
	torrent_info = torrent_search('avengers endgame')
	get_magnet_addr(torrent_info[0]['link'])
