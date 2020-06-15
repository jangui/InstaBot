from instapy import InstaPy
from time import sleep

def follow(username):
    try:
        session.browser.get('https://www.instagram.com/' + username + '/')
        sleep(2)
        buttons = session.browser.find_elements_by_css_selector('button')
        follow_button = buttons[1]
        follow_button.click()
    except:
        print(f"failed to follow {username}")

def unfollow(username):
    try:
        session.browser.get('https://www.instagram.com/' + username + '/')
        sleep(2)
        buttons = session.browser.find_elements_by_css_selector('button')
        unfollow_button = buttons[2]
        unfollow_button.click()
        sleep(1)
        confirm_button = session.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
        confirm_button.click()
    except:
        print(f"failed to unfollow {username}")


username = "espanollie"
password = "6vzvmaHVQ9UWkV5ptE72N7LUpb7g5fMT"

session = InstaPy(username=username, password=password)
#session = InstaPy(username=username, password=password, headless_browser=True)
session.login()

users = ["el.jorgeto.por.ejemplo", "drake", "jaim__d", "djkhaled"]

for user in users:
    follow(user)
    sleep(2)

for user in users:
    unfollow(user)
    sleep(2)

for user in users:
    follow(user)
    sleep(2)

for user in users:
    unfollow(user)
    sleep(2)

session.end()
