from instapy import InstaPy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
from time import sleep, time

from db import add_user
from random import shuffle, seed

seed(time())

username = "truman.human"
password = "6vzvmaHVQ9UWkV5ptE72N7LUpb7g5fMT"

session = InstaPy(username=username, password=password)
#session = instapy(username=username, password=password, headless_browser=true)
#session.login()
sleep(40)

def scroll(pause_time, wait_attempts):
    # Get scroll height
    page_height = session.browser.execute_script("return document.body.scrollHeight")
    # get height at 7/8ths of page
    scroll_to = int(page_height - page_height/8)

    last_height = scroll_to
    waited = 0
    last_state = None
    scrolls = 0
    while True:
        print(f"last height: {last_height} page_height: {page_height} scrolling height: {scroll_to}")
        #if page hasn't loaded after scrolling or we've reached bottom
        if last_height == page_height:
            page_height = session.browser.execute_script("return document.body.scrollHeight")
            print(f"[{str(waited)}] waiting...")
            waited += 1
            last_state = 'waiting'
            #if page taking too long to load, or nothing left to load return
            if (waited == wait_attempts):
                return scrolls

            #if we weren't waiting before, reset wait count
            if (last_state == 'scrolling'):
                waited = 0

        #if we can keep scrolling
        else:
            #scroll to scroll_to height
            scrolls += 1
            print("scrolling...")
            session.browser.execute_script(f"window.scrollTo(0, {scroll_to})")

            #get new height
            last_height = page_height
            page_height = session.browser.execute_script("return document.body.scrollHeight")

            #add to scroll_to by 1/8 of new height
            scroll_to += int(last_height/8)

            #don't pass window height if not much scroll height gained
            if scroll_to >= page_height:
                scroll_to = int(page_height - page_height/16)
            last_state = 'scrolling'

        #pause before restrolling
        sleep(pause_time)

    return scrolls

def get_follower_count():
    flw = WebDriverWait(session.browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#react-root > section > main')))
    sflw = b(flw.get_attribute('innerHTML'), 'html.parser')
    followers = sflw.findAll('span', {'class':'g47SY'})
    f = followers[1].getText().replace(',', '')
    if 'k' in f:
        f = float(f[:-1]) * 10**3
        return f
    elif 'm' in f:
        f = float(f[:-1]) * 10**6
        return f
    else:
        return float(f)

def get_usernames(followers):
    usernames = []
    index = 0
    last_index = 0
    index = followers.index('Follow', index+1)

    if (index - last_index) > 1:
        usernames.append(followers[last_index])
    else:
        usernames.append(followers[index-1])

    while 'Follow' in followers[index+1:]:
        last_index = index
        index = followers.index('Follow', index+1)
        if (index - last_index) > 1:
            usernames.append(followers[last_index+1])
        else:
            usernames.append(followers[index-1])

    return usernames


def get_followers(account):
    scrolls = 0
    for i in range(2):
        session.browser.get(f'https://www.instagram.com/{account}')
        try:
            follower_count = get_follower_count()
        except:
            print(f"{account} doesn't exist")
            return [], 5

        hrefs = []
        sleep(10)

        try:
            #click followers button
            followers_button_xpath = '/html/body/div[1]/section/main/div/ul/li[2]/a'
            followers_button = session.browser.find_element(By.XPATH, followers_button_xpath)
            session.browser.execute_script("arguments[0].click();", followers_button)
        except:
            print(f"{account} is private")
            return [], 5

        sleep(5)

        scrolls = scroll(pause_time=0.5, wait_attempts=50)
        if scrolls > 3:
            break

    #if nothing loaded, take a nice break before trying again
    if scrolls <= 3:
        print(f"taking long pause")
        pause = 600
        session.browser.get(f'https://www.google.com/') #take a break off instagram page
        return [], pause
    else:
        pause = 5



    #get followers
    try:
        div_xpath = '/html/body/div[1]/section/main/div/ul/div'
        div = session.browser.find_element(By.XPATH, div_xpath)
        followers = div.text.split('\n')

        #after done getting info, process it while on homepage
        session.browser.get(f'https://www.instagram.com/')
        usernames = get_usernames(followers)

        if int(follower_count) == len(usernames):
            #all follower for account gotten
            with open("done", 'a') as f:
                print(account, file=f)
    except:
        usernames = [], 5

    return usernames, pause

with open("accounts", 'r') as f:
    accounts = []
    for line in f:
        account = line.strip()
        accounts.append(account)

    for i in range(3):
        shuffle(accounts)
        for account in accounts:
            usernames, pause = get_followers(account)
            for username in usernames:
                try:
                    add_user(username, labels=['techno'])
                except Exception as e:
                    print(f"error adding {username} to db: {e}")
                    with open("errs", 'a') as f:
                        print(username, file=f)
            #sleep between accounts
            sleep(pause)

session.end()
