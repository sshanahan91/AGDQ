import os
import sys
from selenium import webdriver

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'AGDQ.settings'
django.setup()

from datetime import datetime
import re
from events.models import Event
from profiles.models import Profile
from runs.models import Run, Tag




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

		if run[0].text.encode('utf-8').strip() == "Total:":
			continue

		runObj = Run()
		runObj.run_id       = link[len(link)-1]
		runObj.event_id     = (event if event else "")
		runObj.name         = run[0].text.encode('utf-8').strip()
		runObj.game         = "--added later--"
		runObj.description  = run[2].text.encode('utf-8').strip()
		runObj.started_at   = run[3].text.encode('utf-8').strip()
		runObj.ended_at     = run[4].text.encode('utf-8').strip()
		runObj.youtube_link = "--added later--"
		#runObj.save()

		get_runners(run[1], link[len(link)-1])
		#get_tags(run[2], run[0], link[len(link)-1])


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

	for i in range(1, len(all_events)-2):
		event = Event()
		run_link = browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[7]/ul/li[%d]/a' % i)
		run = browser.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul/li[7]/ul/li[%d]/a' % i)
		link = run_link.get_attribute("href").split("/")
		
		event.event_id = link[len(link)-1]
		event.name = run.get_attribute("innerHTML").strip()
		
		browser.get('https://gamesdonequick.com/tracker/donations/%s' % event.event_id)

		event_range = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[1]/td[2]')
		ended_at = event_range.text.encode('utf-8').strip()
		event.ended_at = get_datetime(ended_at)
		
		all_events = browser.find_elements_by_xpath('/html/body/div[1]/p[1]/a[contains(@class, \'last\')]')
		rubbish, final = all_events[0].get_attribute("href").strip().split("=")

		browser.get('https://gamesdonequick.com/tracker/donations/%s?page=%s' % (event.event_id, final))
		all_runs = browser.find_elements_by_tag_name('tr')
		last = len(all_runs)-1
		event_range = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[2]' % last)
		started_at = event_range.text.encode('utf-8').strip()
		event.started_at = get_datetime(started_at)
		event.save()

def get_datetime(string):
	try:
		date_in = re.sub(r"(st|nd|rd|th),", ",", string)
		print date_in
		return datetime.strptime(date_in, '%B %d, %Y, %I:%M:%S %p')
	except:
		print "not abbreviated"

# maybe retry 1-372, just incase there was some unknown loss.
def get_all_users():
	browser.get('https://gamesdonequick.com/tracker/donors/')
	all_events = browser.find_elements_by_xpath('/html/body/div[1]/p[1]/a[contains(@class, \'last\')]')
	rubbish, final = all_events[0].get_attribute("href").strip().split("=")
	for i in range(1, int(final)):
		get_user_by_page(i+1)

def get_user_by_page(page):
	browser.get('https://gamesdonequick.com/tracker/donors/?page=' + str(page))

	try:
		all_runs = browser.find_elements_by_tag_name('tr')
		for i in range(0, len(all_runs)):
			run = browser.find_elements_by_xpath('//table/tbody/tr[%d]/td' % i)
			run_link = browser.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[%d]/td[1]/a' % i)
			link = run_link.get_attribute("href").split("/")
			user = Profile()
			user.user_id = link[len(link)-2]
			user.name   = (run[0].text.encode('utf-8').strip() if run[0].text.encode('utf-8').strip() else "")
			user.alias  = (run[1].text.encode('utf-8').strip() if run[1].text.encode('utf-8').strip() else "")
			user.save()
	except:
		print "Error %d" % page

def get_all_prizes():
	browser.get('https://gamesdonequick.com/tracker/prizes')
	all_prizes = browser.find_elements_by_tag_name('tr')

	for i in range(1, len(all_prizes)):
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
		elif (len(games_link) == 1):
			game_id_link = games_link[0].get_attribute("href").split("/")
			print "run_id/" + game_id_link[len(game_id_link)-1]		
		else:
			continue
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
	for i in range(1, len(all_donations)):
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


def get_runners(runners_webelem, run_id):

	runner_names = [final.strip() for final in runners_webelem.text.encode('utf-8').split(',')]

	for each_runner in runner_names:
		if ' or ' in each_runner.lower():
			first, second = each_runner.split(' or ')
			runner_names.remove(each_runner)
			runner_names.append(first)
			runner_names.append(second)

	for each_runner in runner_names:
		if ' vs ' in each_runner.lower():
			first, second = each_runner.split(' vs ')
			runner_names.remove(each_runner)
			runner_names.append(first)
			runner_names.append(second)

	for each_runner in runner_names:
		if ' vs. ' in each_runner.lower():
			if each_runner.count(' vs. ') == 1:
				first, second = each_runner.split(' vs. ')
			if each_runner.count(' vs. ') == 2:
				first, second, third = each_runner.split(' vs. ')
			runner_names.remove(each_runner)
			runner_names.append(first)
			runner_names.append(second)
			try:
				if third:
					runner_names.append(third)
			except:
				third = 0 #doesnt exist

	for each_runner in runner_names:
		if ' and ' in each_runner.lower():
			first, second = each_runner.split(' and ')
			runner_names.remove(each_runner)
			runner_names.append(first)
			runner_names.append(second)

	for each_runner in runner_names:
		if ' & ' in each_runner.lower():
			first, second = each_runner.split(' & ')
			runner_names.remove(each_runner)
			runner_names.append(first)
			runner_names.append(second)

	for each_runner in runner_names:
		if ' vs. ' in each_runner.lower():
			if each_runner.count(' vs. ') == 1:
				first, second = each_runner.split(' vs. ')
			if each_runner.count(' vs. ') == 2:
				first, second, third = each_runner.split(' vs. ')
			runner_names.remove(each_runner)
			runner_names.append(first)
			runner_names.append(second)
			try:
				if third:
					runner_names.append(third)
			except:
				third = 0 #doesnt exist

	if 'None' in runner_names:
		runner_names.remove('None')
	if '' in runner_names:
		runner_names.remove('')

	for each_runner in runner_names:
		intital_ref = each_runner
		if each_runner.startswith('and '):
			each_runner = each_runner[4:]
		if each_runner.startswith('maybe '):
			each_runner = each_runner[6:]
		if each_runner.startswith('any% by '):
			each_runner = each_runner[8:]
		if each_runner.startswith('everyone'):
			runner_names.remove(each_runner)
		if each_runner.startswith('or '):
			each_runner = each_runner[3:]
		if each_runner.endswith('.'):
			each_runner = each_runner[:-1]
		if intital_ref != each_runner:
			runner_names.append(each_runner)
			runner_names.remove(intital_ref)

	for each_runner in runner_names:
		if ' and ' in each_runner.lower():
			first, second = each_runner.split(' and ')
			runner_names.remove(each_runner)
			runner_names.append(first)
			runner_names.append(second)
	for each_runner in runner_names:
		print run_id + ": " + each_runner
	print "------"

def make_tags():
	tags = ['Boss Mode','Any%','Low%','100%','Race', \
			'2p','4p','8p','New Game+','Blindfolded','TAS',  \
			'Good Ending','Bad Ending','Glitched', \
			'Co-Op','1p2c', 'Hard Mode','Best Ending','Warpless']

	for tag in tags:
		print "Made tag %s" % tag
		new_tag = Tag(name=tag)
		new_tag.save()


def get_tags(description, title, run_id):
	text = description.text.encode('utf-8').strip().lower() + title.text.encode('utf-8').strip().lower()
	run = Run.objects.get(run_id=run_id)

	if 'boss' in text:
		tag = Tag.objects.get(name='Boss Mode')
		run.tags.add(tag)

	if ('any%' in text) or ('any %' in text):
		tag = Tag.objects.get(name='Any%')
		run.tags.add(tag)

	if ('low%' in text) or ('low %' in text):
		tag = Tag.objects.get(name='Low%')
		run.tags.add(tag)

	if ('100%' in text) or ('100 %' in text):
		tag = Tag.objects.get(name='100%')
		run.tags.add(tag)

	if 'race' in text:
		tag = Tag.objects.get(name='Race')
		run.tags.add(tag)

	if ('2p' in text) or ('2 player' in text) or ('2 way' in text):
		tag = Tag.objects.get(name='2p')
		run.tags.add(tag)

	if ('4p' in text) or ('4 player' in text) or ('4 way' in text):
		tag = Tag.objects.get(name='4p')
		run.tags.add(tag)

	if ('8p' in text) or ('8 player' in text) or ('8 way' in text):
		tag = Tag.objects.get(name='8p')
		run.tags.add(tag)

	if ('ng+' in text) or ('new game+' in text) or ('new game +' in text):
		tag = Tag.objects.get(name='New Game+')
		run.tags.add(tag)

	if ('blindfold' in text):
		tag = Tag.objects.get(name='Blindfolded')
		run.tags.add(tag)

	if ('tasbot' in text) or (' tas ' in text):
		tag = Tag.objects.get(name='TAS')
		run.tags.add(tag)

	if 'good end' in text:
		tag = Tag.objects.get(name='Good Ending')
		run.tags.add(tag)

	if 'bad end' in text:
		tag = Tag.objects.get(name='Bad Ending')
		run.tags.add(tag)

	if 'glitch' in text:
		tag = Tag.objects.get(name='Glitched')
		run.tags.add(tag)

	if ('coop' in text) or ('co-op' in text):
		tag = Tag.objects.get(name='Co-Operative')
		run.tags.add(tag)

	if ('1p2c' in text) or ('1 player, 2 controllers' in text):
		tag = Tag.objects.get(name='1 player, 2 controllers')
		run.tags.add(tag)

	if 'hard mode' in text:
		tag = Tag.objects.get(name='Hard Mode')
		run.tags.add(tag)

	if ('best end' in text) or ('true end' in text):
		tag = Tag.objects.get(name='Best Ending')
		run.tags.add(tag)

	if ('no warp' in text) or ('warpless' in text):
		tag = Tag.objects.get(name='Warpless')
		run.tags.add(tag)

#get_all_events()
# get_all_users()

# without event_ids as an array, event_id not saved with data
# without users first, cant search for players based on name
#make_tags()

# for event in Event.objects.all():
# 	get_runs_by_event(event.event_id)
get_runs_by_event('sgdq2013')
#
#get_all_prizes()

#get_bids_by_event()

## must come after users
#get_all_donations()

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