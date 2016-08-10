import os
from selenium import webdriver

global browser 

path_to_chromedriver = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver'
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

# Runs
#
# Set up to either use event specific runs. defaults to all events.
#
def get_runs_by_event(event = None):
	if event:
		browser.get('https://gamesdonequick.com/tracker/runs/' + event)
	else:
		browser.get('https://gamesdonequick.com/tracker/runs')
		event = None

	all_runs = browser.find_elements_by_tag_name('tr')

	for i in range(1, len(all_runs)):
		run = browser.find_elements_by_xpath('//table/tbody/tr[%d]/td' % i)
		run_link = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[1]/a' % i)
		link = run_link.get_attribute("href").split("/")
		print "run_id:       " + link[len(link)-1]
		print "event_id:     " + (event if event else "")
		print "name:         " + run[0].text.encode('utf-8').strip()
		print "game:         " + "--added later--"
		print "youtube_link: " + "--added later--"
		print "runners txt:  " + run[1].text.encode('utf-8').strip()
		print "description:  " + run[2].text.encode('utf-8').strip()
		print "started_at:   " + run[3].text.encode('utf-8').strip()
		print "ended_at:     " + run[4].text.encode('utf-8').strip()
		print "bid_war:      " + run[5].text.encode('utf-8').strip()
		print ""


# Events
#
# Note, this function only gets the name and ID. start and end time
#   should be calculated after runs are connected. MIN(start time)
#   and MAX(end time) are the start and end. or use those times +/-
#   a week to account for rogue donations.
#
def get_all_events():
	browser.get('https://gamesdonequick.com/tracker/')
	all_events = browser.find_elements_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[7]/ul/li')

	for i in range(1, len(all_events)-1):
		run_link = browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[7]/ul/li[%d]/a' % i)
		run = browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[7]/ul/li[%d]/a' % i)
		link = run_link.get_attribute("href").split("/")
		
		print "event_id:   " + link[len(link)-1]
		print "event_name: " + run.get_attribute("innerHTML").strip()
		print ""


get_runs_by_event('agdq2016')
browser.close()