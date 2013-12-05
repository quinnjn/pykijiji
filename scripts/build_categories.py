from bs4 import BeautifulSoup, SoupStrainer
import re
import requests 
import json

strained = SoupStrainer('a', href=re.compile('saskatchewan.kijiji.ca/f.*QQ'))
soup = BeautifulSoup(requests.get('http://saskatchewan.kijiji.ca').text)

category_dict = {}

for a in soup.findAll(strained):
	category_id = None
	category = []

	for key in str(a.string).split(", "):
		category.append(key)

	category_id_matches = re.search('CatIdZ(\d+)', a['href'])
	if(category_id_matches):
		category_id = category_id_matches.group(1)

	if(category_id and category):
		for key in category:
			category_dict[key] = int(category_id)

if(category_dict):
	with open('../pykijiji/categories.json', 'w') as f:
		json.dump(
			category_dict, 
			f, 
			sort_keys=True, 
			indent=2
		)

