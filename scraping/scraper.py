from instapy import InstaPy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as b
from time import sleep

username = "truman.human"
password = "6vzvmaHVQ9UWkV5ptE72N7LUpb7g5fMT"

session = InstaPy(username=username, password=password)
#session = instapy(username=username, password=password, headless_browser=true)
session.login()

def scroll(pause_time):
    # Get scroll height
    page_height = session.browser.execute_script("return document.body.scrollHeight")
    # get height at 7/8ths of page
    scroll_to = int(page_height - page_height/8)

    last_height = scroll_to
    while True:
        print(f"last height: {last_height} page_height: {page_height} scrolling height: {scroll_to}")
        #if page hasn't loaded after scrolling or we've reached bottom
        if last_height == page_height:
            page_height = session.browser.execute_script("return document.body.scrollHeight")
            print("waiting...")
            pass
            #break out func

        #if we can keep scrolling
        else:
            #scroll to scroll_to height
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

        #pause before restrolling
        sleep(pause_time)

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

def get_followers(account):
    session.browser.get(f'https://www.instagram.com/{account}')
    #follower_count = get_follower_count()
    hrefs = []
    sleep(2)

    #click follow button
    follow_button_xpath = '/html/body/div[1]/section/main/div/ul/li[2]/a'
    follow_button = session.browser.find_element(By.XPATH, follow_button_xpath)
    session.browser.execute_script("arguments[0].click();", follow_button)

    sleep(5)

    #scroll with a pause of 2 secconds
    scroll(1)

    """
    #find followers
    div_xpath = '/html/body/div[1]/section/main/div/ul/div'
    div = session.browser.find_element(By.XPATH, div_xpath)
    print(div.text)
    """

#account = "el.jorgeto.por.ejemplo"
#account = 'alexandra_melliflow'
account = 'veragoesdeep'
print(get_followers(account))

session.end()
