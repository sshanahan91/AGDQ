import os
from selenium import webdriver

path_to_chromedriver = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'https://gamesdonequick.com/tracker/runs'
browser.get(url)

all_objects = browser.find_elements_by_tag_name('tr')

for i in range(1, len(all_objects)):
	run = browser.find_elements_by_xpath('//table/tbody/tr[%d]/td' % i)

	print "Title:       " + run[0].text.encode('utf-8').strip()
	print "Players:     " + run[1].text.encode('utf-8').strip()
	print "Description: " + run[2].text.encode('utf-8').strip()
	print "started_at:  " + run[3].text.encode('utf-8').strip()
	print "ended_at:    " + run[4].text.encode('utf-8').strip()
	print "bid_war:     " + run[5].text.encode('utf-8').strip()
	print "\n"
browser.close()