from instapy import InstaPy
from time import sleep

username = "espanollie"
password = "6vzvmaHVQ9UWkV5ptE72N7LUpb7g5fMT"

session = InstaPy(username=username, password=password)
#session = InstaPy(username=username, password=password, headless_browser=True)
session.login()

def follow_user(username):
        session.browser.get('https://www.instagram.com/' + username + '/')
        sleep(2)
        buttons = session.browser.find_elements_by_css_selector('button')
        follow_button = buttons[1]
        follow_button.click()
        """
        if (follow_button.text != 'Following'):
            follow_button.click()
            sleep(5)
        else:
            print("You are already following this user")
        """
def unfollow_user(username):
        session.browser.get('https://www.instagram.com/' + username + '/')
        sleep(2)
        buttons = session.browser.find_elements_by_css_selector('button')
        unfollow_button = buttons[2]
        unfollow_button.click()
        confirm_button = session.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
        confirm_button.click()

#unfollow_user("newyorknico")
#follow_user("newyorknico")
sleep(5)

session.end()
