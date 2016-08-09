from selenium import webdriver

path_to_chromedriver = '/home/sshanahan91/Downloads/AGDQ/chromedriver' # change path as needed
browser = webdriver.Chrome(executable_path = path_to_chromedriver)

url = 'https://gamesdonequick.com/tracker/'
browser.get(url)
