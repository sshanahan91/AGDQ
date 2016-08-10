import os
from selenium import webdriver

global browser 

path_to_chromedriver = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

# Runs
def get_all_runs(url):
	browser.get('https://gamesdonequick.com/tracker/' + url)
	all_runs = browser.find_elements_by_tag_name('tr')

	for i in range(1, len(all_runs)):
		run = browser.find_elements_by_xpath('//table/tbody/tr[%d]/td' % i)

		print "Title:       " + run[0].text.encode('utf-8').strip()
		print "Players:     " + run[1].text.encode('utf-8').strip()
		print "Description: " + run[2].text.encode('utf-8').strip()
		print "started_at:  " + run[3].text.encode('utf-8').strip()
		print "ended_at:    " + run[4].text.encode('utf-8').strip()
		print "bid_war:     " + run[5].text.encode('utf-8').strip()
		print ""


# Events
def get_all_events(url):
	browser.get('https://gamesdonequick.com/tracker/' + url)
	all_events = browser.find_elements_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[7]/ul/li')

	for i in range(1, len(all_events)-1):
		run_link = browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[7]/ul/li[%d]/a' % i)
		run = browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[7]/ul/li[%d]/a' % i)
		link = run_link.get_attribute("href").split("/")
		
		print "event_id:   " + link[len(link)-1]
		print "event_name: " + run.get_attribute("innerHTML").strip()
		print ""


get_all_events('runs')
browser.close()