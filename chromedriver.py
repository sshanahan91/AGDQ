import os
import sys
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

	for i in range(1, len(all_prizes)-1): #/html/body/div[1]/table/tbody/tr[129]/td[1]/a
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
		contrib_by = prize[1].text.encode('utf-8').strip()
		has_winner = len(winner_id_link)
		print "contrib_by: " + contrib_by
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

		if (len(games_link) > 1):
			browser.get('https://gamesdonequick.com/tracker/prize/' + prize_id_link[len(prize_id_link)-1])
			if (contrib_by and has_winner):
				all_games = browser.find_elements_by_xpath('/html/body/div[1]/table[3]/tbody/tr')
			elif (contrib_by or has_winner):
				all_games = browser.find_elements_by_xpath('/html/body/div[1]/table[2]/tbody/tr')
			else:
				all_games = browser.find_elements_by_xpath('/html/body/div[1]/table[1]/tbody/tr')

			for i in range(2, len(all_games)+1):
				if (contrib_by and has_winner):
					prize_link = browser.find_element_by_xpath('/html/body/div[1]/table[3]/tbody/tr[%d]/td/a' % i)
				elif (contrib_by or has_winner):
					prize_link = browser.find_element_by_xpath('/html/body/div[1]/table[2]/tbody/tr[%d]/td/a' % i)
				else:
					prize_link = browser.find_element_by_xpath('/html/body/div[1]/table[1]/tbody/tr[%d]/td/a' % i)

				prize_id_link = prize_link.get_attribute("href").split("/")
				print "run_id/" + prize_id_link[len(prize_id_link)-1]
			browser.get('https://gamesdonequick.com/tracker/prizes')
		else:
			game_id_link = games_link[0].get_attribute("href").split("/")
			print "run_id/" + game_id_link[len(game_id_link)-1]		
		print ""

def get_bids_by_event():
	# events = [5,3,2,1,7,8,9,10,12,16,17,18]
	event_name = [ 	'agdq2011', 'sgdq2011', 'agdq2012', \
					'sgdq2012', 'agdq2013', 'sgdq2013', \
					'agdq2014', 'sgdq2014', 'agdq2015', \
					'sgdq2015', 'agdq2016', 'sgdq2016' ]
	
	for event_id in event_name:
		browser.get('https://gamesdonequick.com/tracker/bids/' + event_id)
		last_id = 0
		all_bids = browser.find_elements_by_xpath('/html/body/div[1]/table/tbody/tr')

		for i in range(1, len(all_bids)+1):
			try:
				bid_link = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[1]/a' % i)
				bid_ids = bid_link.get_attribute("href").split("/")
				bid = browser.find_elements_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td' % i)
			except:
				if (last_id != 0):
					if (event_id == 'agdq2014' and last_id == '1077'): # save or kill the animals...

						browser.find_element_by_xpath('//*[@id="bidOptionToggle1077"]/td/button').click()
						browser.find_element_by_xpath('//*[@id="bidOptionToggle1078"]/td/button').click()
						for k in range(1, 3):
							kill_save_choice = browser.find_elements_by_xpath('//*[@id="bidOptionData1078"]/td/table/tbody/tr[%d]/td' % k)
							kill_save_choice_link = browser.find_element_by_xpath('//*[@id="bidOptionData1078"]/td/table/tbody/tr[%d]/td[1]/a' % k)
							choice_ids = kill_save_choice_link.get_attribute("href").split("/")
							print "----choice_id:    %s" % choice_ids[len(choice_ids)-1]
							print "----bid_id:       %s" % last_id
							print "----choice_name:  %s" % kill_save_choice[0].text.encode('utf-8').strip()
							print "----description:  %s" % kill_save_choice[1].text.encode('utf-8').strip()
							print "----"
						#"second" choice
						kill_save_choice = browser.find_elements_by_xpath('//*[@id="bidOptionData1077"]/td/table/tbody/tr[4]/td')
						kill_save_choice_link = browser.find_element_by_xpath('//*[@id="bidOptionData1077"]/td/table/tbody/tr[4]/td[1]/a')
						choice_ids = kill_save_choice_link.get_attribute("href").split("/")
						print "----choice_id:    %s" % choice_ids[len(choice_ids)-1]
						print "----bid_id:       %s" % last_id
						print "----choice_name:  %s" % kill_save_choice[0].text.encode('utf-8').strip()
						print "----description:  %s" % kill_save_choice[1].text.encode('utf-8').strip()
						print "----"
						last_id = 0
						continue
					browser.find_element_by_xpath('//*[@id="bidOptionToggle'+last_id+'"]/td/button').click()

					all_bid_choices = browser.find_elements_by_xpath('//*[@id="bidOptionData%s"]/td/table/tbody/tr' % last_id)

					for j in range(1, len(all_bid_choices)+1):
						bid_choices = browser.find_elements_by_xpath('//*[@id="bidOptionData%s"]/td/table/tbody/tr[%d]/td' % (last_id, j))
						bid_choices_link = browser.find_element_by_xpath('//*[@id="bidOptionData%s"]/td/table/tbody/tr[%d]/td[1]/a' % (last_id, j))
						choice_ids = bid_choices_link.get_attribute("href").split("/")
						print "----choice_id:    %s" % choice_ids[len(choice_ids)-1]
						print "----bid_id:       %s" % last_id
						print "----choice_name:  %s" % bid_choices[0].text.encode('utf-8').strip()
						print "----description:  %s" % bid_choices[1].text.encode('utf-8').strip()
						print "----"
					last_id = 0
				continue
			print "bid_id:       %s" % bid_ids[len(bid_ids)-1]
			#need to search database for event and run name.
			print "bid_name:     %s" % bid[0].text.encode('utf-8').strip()
			if (len(bid) == 4): # if there is no run name, the columns are offset by 1
				no_run_offset = -1
			else:
				no_run_offset = 0
				print "run_id:       %s" % bid[1].text.encode('utf-8').strip()

			print "description:  %s" % bid[2 + no_run_offset].text.encode('utf-8').strip()
			raised = float((bid[3 + no_run_offset].text.encode('utf-8').strip()).translate(None, '$,'))
			print "tot_donatns?: %.2f" % raised
			if (bid[4 + no_run_offset].text.encode('utf-8').strip() != "(None)"):
				goal = float((bid[4 + no_run_offset].text.encode('utf-8').strip()).translate(None, '$,'))
			else:
				goal = 0
			print "goal:         %.2f" % goal
			print "goal_met:     %s" % (True if (raised >= goal) else False)
			last_id = bid_ids[len(bid_ids)-1]
			print ""
			try:
				browser.find_element_by_xpath('//*[@id="bidOptionToggle'+last_id+'"]/td/button')
			except:
				print "----choice_id:    %s" % bid_ids[len(bid_ids)-1]
				print "----bid_id:       %s" % bid_ids[len(bid_ids)-1]
				print "----choice_name:  %s" % bid[0].text.encode('utf-8').strip()
				print "----description:  %s" % bid[2 + no_run_offset].text.encode('utf-8').strip()
				print "----"

def get_all_donations():
	browser.get('https://gamesdonequick.com/tracker/donations/')
	all_events = browser.find_elements_by_xpath('/html/body/div[1]/p[1]/a[contains(@class, \'last\')]')
	rubbish, final = all_events[0].get_attribute("href").strip().split("=")
	for i in range(0, int(final)):
		get_donation_by_page(i+1)

def get_donation_by_page(page):
	browser.get('https://gamesdonequick.com/tracker/donations/?page=' + str(page))

	all_donations = browser.find_elements_by_tag_name('tr')
	for i in range(1, len(all_donations)+1):
		donation = browser.find_elements_by_xpath('//table/tbody/tr[%d]/td' % i)
		donation_user_link = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[1]/a' % i)
		user_link = donation_user_link.get_attribute("href").split("/")
		donation_link = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[3]/a' % i)
		link = donation_link.get_attribute("href").split("/")
		print "user_id:       " + user_link[len(user_link)-2]
		print "event_id:      " + user_link[len(user_link)-1]
		print "time_recieved: " + donation[1].text.encode('utf-8').strip()
		print "amount:        %.2f" % float((donation[2].text.encode('utf-8').strip()).translate(None, '$,'))
		print "donation_id:   " + link[len(link)-1]
		print "has_comment:   " + str(True if (donation[3].text.encode('utf-8').strip() == 'Yes') else False)
		print ""

def get_donation_bids_by_choice(choice_ids = []):
	#requires each individual choice id on the /bid/{num} page.
	for choice_id in choice_ids:
		browser.get('https://gamesdonequick.com/tracker/bid/' + str(choice_id))

		all_choices = browser.find_elements_by_tag_name('tr')
		for i in range(1, len(all_choices)):
			choice = browser.find_elements_by_xpath('//table/tbody/tr[%d]/td' % i)
			choice_user_link = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[1]/a' % i)
			user_link = choice_user_link.get_attribute("href").split("/")
			choice_link = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[3]/a' % i)
			link = choice_link.get_attribute("href").split("/")
			print "choice_id:     " + str(choice_id)
			print "user_id:       " + user_link[len(user_link)-2]
			print "time_recieved: " + choice[1].text.encode('utf-8').strip()
			print "amount:        %.2f" % float((choice[2].text.encode('utf-8').strip()).translate(None, '$,'))
			print "donation_id:   " + link[len(link)-1]
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

	if ('tasbot' in text) or (' tas ' in text):
		tag_list.append('TAS')

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

get_all_events()
get_runs_by_event()
get_all_users()
get_all_prizes()

get_bids_by_event()

## must come after users
get_all_donations()

## need each bid_choice
#get_donation_bids_by_choice()
browser.close()

# all donors
#  --donations?
# all events
# 
# all runs
#  --when runners, connect to donors or create "donor"
#    --connect runners_to_runs
#  --when tags, create "tag"
#    --connect tags_to_runs
# 
# all prizes
#   --when contributors, search and connect to donors, or create donor
#   --when winners, connect prize_to_winner
#   --when runs, connect prize_to_runs
# 
# all bids
#  --when choices add choice
#    --when bid choices, connect bid_to_choice
#      --connect to donation_id