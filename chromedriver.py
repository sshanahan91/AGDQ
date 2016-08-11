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
		print "started_at:   " + run[3].text.encode('utf-8').strip()
		print "ended_at:     " + run[4].text.encode('utf-8').strip()
		print "bid_war:      " + run[5].text.encode('utf-8').strip()
		print "game:         " + "--added later--"
		print "youtube_link: " + "--added later--"

		# split full runner text by comma, remove all white space
		runners = get_runners(run[1])
		if runners:
		# show list as a string seperated by slashes.
			print "runners:      " + "/".join(runners)
		print "description:  " + run[2].text.encode('utf-8').strip()
		tags = get_tags(run[2], run[0])
		if tags:
			print "tags:         " + "/".join(tags)
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
		get_event_range(link[len(link)-1])
		print ""

def get_event_range(event_id):
	browser.get('https://gamesdonequick.com/tracker/donations/' + event_id)

	event_range = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[1]/td[2]')
	print "ended_at:   " + event_range.text.encode('utf-8').strip()
	all_events = browser.find_elements_by_xpath('/html/body/div[1]/p[1]/a[contains(@class, \'last\')]')
	rubbish, final = all_events[0].get_attribute("href").strip().split("=")

	browser.get('https://gamesdonequick.com/tracker/donations/%s?page=%s' % (event_id, final))
	all_runs = browser.find_elements_by_tag_name('tr')
	last = len(all_runs)-1
	event_range = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[2]' % last)
	print "started_at: " + event_range.text.encode('utf-8').strip()

def get_all_users():
	browser.get('https://gamesdonequick.com/tracker/donors/')
	all_events = browser.find_elements_by_xpath('/html/body/div[1]/p[1]/a[contains(@class, \'last\')]')
	rubbish, final = all_events[0].get_attribute("href").strip().split("=")
	for i in range(0, int(final)):
		get_user_by_page(i+1)

def get_user_by_page(page):
	browser.get('https://gamesdonequick.com/tracker/donors/?page=' + str(page))

	all_runs = browser.find_elements_by_tag_name('tr')
	for i in range(1, len(all_runs)):
		run = browser.find_elements_by_xpath('//table/tbody/tr[%d]/td' % i)
		run_link = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[1]/a' % i)
		link = run_link.get_attribute("href").split("/")
		print "user_id: " + link[len(link)-2]
		print "name:    " + run[0].text.encode('utf-8').strip()
		print "alias:   " + run[1].text.encode('utf-8').strip()

def get_all_prizes():
	browser.get('https://gamesdonequick.com/tracker/prizes')
	all_prizes = browser.find_elements_by_tag_name('tr')

	for i in range(1, len(all_prizes)-1):
		prize_link = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[1]/a' % i)
		games_link = browser.find_elements_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[4]/a' % i)		
		prize = browser.find_elements_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td' % i)
		prize_id_link = prize_link.get_attribute("href").split("/")
		image_link = prize[5].get_attribute("href")
		winner_id_link = browser.find_elements_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[7]/a' % i)		
		###winner_id_link = browser.find_elements_by_xpath('/html/body/div[1]/table/tbody/tr[659]/td[7]/a')		
		print "prize_id:   " + prize_id_link[len(prize_id_link)-1]
		print "prize_name: " + prize[0].text.encode('utf-8').strip()
		# need to try to link this to a user ID before putting in DB
		print "contrib_by: " + prize[1].text.encode('utf-8').strip()
		print "min_bid:    " + prize[2].text.encode('utf-8').strip()
		print "category:   " + prize[4].text.encode('utf-8').strip()
		print "image_link: " + (image_link if image_link else "")

		if (len(winner_id_link) == 1):
			winner_id_links = [(winner_id.get_attribute("href").split("/"))[len(winner_id_link)-3] for winner_id in winner_id_link]
			print "winner_id/" + winner_id_links[0]
		if (len(winner_id_link) > 1):
			winner_id_links = [(winner_id.get_attribute("href").split("/")) for winner_id in winner_id_link]
			for each_id in winner_id_links:
				print "winner_id/" + each_id[len(each_id)-2]
		# if (len(games_link) > 1):
		# 	print "multiple games"
		# elif (len(games_link) == 0):
		# 	print "grand prize"
		# else:
		# 	game = games_link[0].get_attribute("href").split("/")
		# 	print "run_id/" + game[len(link)-1] + "\tprize_id/" + link[len(link)-1]
		
		print ""


def get_runners(runners_webelem):
	# "None" still considered a runner. " and " still gives runner
	#  information concatenated.
	return [final.strip() for final in runners_webelem.text.encode('utf-8').split(',')]

def get_tags(description, title):
	text = description.text.encode('utf-8').strip().lower() + title.text.encode('utf-8').strip().lower()
	tag_list = []

	if 'boss' in text:
		tag_list.append('Boss Mode')

	if ('any%' in text) or ('any %' in text):
		tag_list.append('Any%')

	if ('low%' in text) or ('low %' in text):
		tag_list.append('Low%')

	if ('100%' in text) or ('100 %' in text):
		tag_list.append('100%')

	if 'race' in text:
		tag_list.append('Race')

	if ('2p' in text) or ('2 player' in text) or ('2 way' in text):
		tag_list.append('2p')

	if ('4p' in text) or ('4 player' in text) or ('4 way' in text):
		tag_list.append('4p')

	if ('8p' in text) or ('8 player' in text) or ('8 way' in text):
		tag_list.append('8p')

	if ('ng+' in text) or ('new game+' in text) or ('new game +' in text):
		tag_list.append('New Game+')

	if ('blindfold' in text):
		tag_list.append('Blindfolded')

	if 'good end' in text:
		tag_list.append('Good Ending')

	if 'bad end' in text:
		tag_list.append('Bad Ending')

	if 'glitch' in text:
		tag_list.append('Glitched')

	if ('coop' in text) or ('co-op' in text):
		tag_list.append('4p')

	if 'hard mode' in text:
		tag_list.append('Hard Mode')

	if 'best end' in text:
		tag_list.append('Best Ending')

	return tag_list

# get_all_events()
# get_runs_by_event()
# get_all_users()
get_all_prizes()
browser.close()

# all donors
# all events
# 
# all runs
#  --when runners, connect to donors or create "donor"
#    --connect runners_to_runs
#  --when tags, create "tag"
#    --connect tags_to_runs
# 
# 
# 
# 
# 
# 
# 
# 
# 