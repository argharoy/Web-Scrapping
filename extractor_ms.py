from bs4 import BeautifulSoup

import re
import json
import unicodedata
import urllib2 as fetch

print "Processing..."

#to_crawl = "http://www.mouthshut.com/product-reviews/Britannia-Little-Hearts-Biscuits-reviews-925036434-page-"
#to_crawl = "http://www.mouthshut.com/product-reviews/Parle-G-Biscuits-reviews-925036427-page-"
#to_crawl = "http://www.mouthshut.com/product-reviews/Britannia-Good-Day-Biscuits-reviews-925036420-page-"
to_crawl = "http://www.mouthshut.com/product-reviews/Goa-reviews-925752312-page-"

initial = 0
ending = 10

for k in range(initial, ending):
	file_flag = 1
	prev_data, new_data = ([] for lis in range(2))
	url = to_crawl + str(k+1)
	response = fetch.urlopen(url)

	data = response.read()

	soup = BeautifulSoup(data, "html.parser")

	p_data = soup.find_all('div',attrs= {'class':'more reviewdata'})

	urls = []
	for data in p_data:
		for url in data:
			try:
				match_url = re.search('http://www.mouthshut.com/review/',url['onclick'])
				if match_url:
					tokens = url['onclick'].split(',')
					urls.append(tokens[7].strip("'"))
			except:
				pass

	final_data = []
	final_user = []
	urls_len = len(urls)
	#eli_list = ['<p>','</p>','<p class="lnhgt">','<br/>','<ul>','</ul>','<li>','</li>']
	cleaner = re.compile('<.*?>')
	#eli_list = '|'.join(eli_list)

	for i in range(0,urls_len):
		response = fetch.urlopen(urls[i])
		data = response.read()
		soup = BeautifulSoup(data, "html.parser")

		revw_data = soup.find_all('div',attrs= {'class':'user-review'})
		user_data = soup.find_all('div', attrs= {'class':'col-2 profile'})
		'''
		print revw_data
		print len(user_data), " -- ",len(revw_data)
		print user_data
		'''

		for data in revw_data:
			texts = data.find_all("p", attrs = {'class':'lnhgt'})
			text = re.sub(cleaner, '', str(texts[0]))
			final_data.append(text.strip("\n"))
			user_data = user_data[0].find_all("label", attrs = {'id':'ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_linkrevname'})
			user_data = user_data[0].find_all("a")
			user_data = re.sub(cleaner, '', str(user_data[0]))
			final_user.append(user_data)

		#for data in user_data:
			#users_data = data.find_all("p", attrs = {'id':'ctl00_ctl00_ContentPlaceHolderFooter_ContentPlaceHolderBody_lnkRevName'})

			
			#print user_data
			
			#user = user_data[0].get_text().strip("\n")
			#user = unicodedata.normalize('NFKD', user).encode('ascii','ignore')


	print len(final_user)," -- ",len(final_data)
	print final_user

	dictionary = dict(zip(final_user,final_data))
	new_data.append(dictionary)
	try:
		with open('Goa1.json') as data_file:
			prev_data.append(json.load(data_file))
	except:
		file_flag = 0

	file = open('Goa1.json','w')

	if file_flag == 1:
		file.write(json.dumps(prev_data + new_data))
	elif file_flag == 0:
		file.write(json.dumps(new_data))

	file.close()

	for i in range(0,len(final_data)):
		print str(i+1),". ",final_user[i]," --> ",final_data[i],"\n"

	print "Processing Completed Web Page : ",str(k+1), " !"