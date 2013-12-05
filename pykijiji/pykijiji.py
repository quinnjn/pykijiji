import requests
import re
from bs4 import BeautifulSoup

class KijijiItem: 
	def __init__(self, id):
		self.link = "http://m.kijiji.ca/v?adId="+id
		self.meta = {
			'id':id
		}
		headers = {
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'
		}
		soup = BeautifulSoup(requests.get(self.link, headers=headers).text)

		for item in soup.find_all('span', {'class':'fieldLabel'}):
			if 'id' in item.attrs:
				self.meta[item['id']] = item.parent.contents[3].string

	def __str__(self):
		return str(self.meta)

class KijijiList: 
	def __init__(self, homesite, category):
		site = 'http://%s.kijiji.ca/f-SearchAdRss?CatId=%d'%(
			homesite,
			category
		)
		self.items = []

		soup = BeautifulSoup(requests.get(site).text)
		for item in soup.find_all('item'):
			link = item.link.text
			group = re.search('AdIdZ(\d+)', link)
			kijiji_id = group.group(1)
			self.items.append(KijijiItem(kijiji_id))

	def list(self):
		return self.items

class PyKijiji: 
	master_categories = {
		'snowmobiles':171
	}
	def site(self, site=""):
		if(site):
			self.site = site 
		return self.site

	def category(self, category=""):
		category = self.master_categories[category]
		if(category):
			self.category = category
		return category

	def list(self):
		klist = KijijiList(
			self.site, 
			self.category
		)
		return klist.list()


k = PyKijiji()

k.site('regina')
k.category('snowmobiles')

for item in k.list():
	print item
