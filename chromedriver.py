import os
from selenium import webdriver

path_to_chromedriver = os.path.dirname(os.path.abspath(__file__)) + '/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'https://gamesdonequick.com/tracker/'
browser.get(url)
