from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib3.packages.six import b


class LoginPage: 
    def __init__(self, browser):
        self.browser = browser

    def login(self, username, password):
        username_input = self.browser.find_element_by_css_selector("input[name='username']")
        password_input = self.browser.find_element_by_css_selector("input[name='password']")
        #find the username and passowrd input fields by cs
        username_input.send_keys(username)
        password_input.send_keys(password)
        #TFA must be off on target account
        login_button = browser.find_element_by_xpath("//button[@type='submit']")
        login_button.click()
        sleep(5)

class HomePage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://www.instagram.com/')

    def go_to_login_page(self):
      #  self.browser.find_element_by_xpath("//a[text()='Log in']").click() 
      #above line isn't needed with current website since login fields are visbile on homepage but has been needed on older versions of the site so I'll leave it
        sleep(2)
        return LoginPage(self.browser)

class Search:
    def __init__(self, browser):
        self.browser = browser   

    def search_for(self, searchterm):
        search_bar = browser.find_element_by_css_selector("input[placeholder='Search']")
        search_bar.send_keys(searchterm)
        search_bar.send_keys(Keys.ENTER)
        sleep(1)
        search_bar.send_keys(Keys.ENTER)
        sleep(1)
        search_bar.send_keys(Keys.ENTER)
        #it takes hitting enter three times apparently
    
class Interact:
    def __init__(self, browser):
        self.browser = browser   

    def next_button(self): #this works for either liking or commenting on posts. Whenever you're in the post carousel, it will go to the next post
        next_button = browser.find_element_by_css_selector('._65Bje')
        next_button.click()

    def find_first_photo(self): #need to call search for before calling this
        user_photo = browser.find_element_by_css_selector('.EZdmt > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2)')
        user_photo.click()

    def like_posts(self): #need to call search and find first photo before calling this. I could seperate them and create a dependency but I don't want to
        like_button = browser.find_element_by_css_selector('.fr66n > button:nth-child(1) > div:nth-child(1) > span:nth-child(1) > svg:nth-child(1)')
        like_button.click()
        #this worked on all the hashtags I tried it on but idk if it works on all searches
        #repreating this on the same hashtag can "un-like" posts that have previously been "liked"

    def comment_on_posts(self,comment):
        comment_box = browser.find_element_by_css_selector('.RxpZH')
        comment_box.click()
        comment_text_field = browser.find_element_by_css_selector('.Ypffh')
        comment_text_field.send_keys(comment)
        post_button = browser.find_element_by_css_selector('button.sqdOP:nth-child(4)')
        post_button.click()


#######################################################################################################################################################################

browser = webdriver.Firefox()
browser.implicitly_wait(5) #waits for 5 seconds to allow elements to load if not found the first time

home_page = HomePage(browser)
login_page = home_page.go_to_login_page()
login_page.login("USERNAME", "PASSWORD") #INSERT TARGET ACCOUNT CREDENTIALS HERE


hashtag_search = Search(browser)
hashtag_search.search_for("SEARCH TERM") #ENTER A SEARCH TERM HERE
#needs the '#' symbol if searching for a hashtag other wise you will get a user account


do_stuff = Interact(browser)

#Lets do stuff
do_stuff.find_first_photo()
x = 1
while x<= 100: #CHANGE X TO ANY NUMBER OF POSTS YOU WANT TO INTERACT WITH
        do_stuff.like_posts()
        do_stuff.comment_on_posts("COMMENT") #ENTER YOUR COMMENT HERE
        do_stuff.next_button()
        x+=1
#the above technically works however instagram will probably flag it as a bot and limit post commenting after 5-10 posts
#You could probably let the program sleep for a set amount of time inbetween comments and/or loop through a bunch of different comments in order to not be flagged but idk how Instagram's code works

browser.close()

