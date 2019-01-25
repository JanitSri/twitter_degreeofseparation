''' 
NAME: Janit Sriganeshaelankovan 
CREATED: December 01, 2018 - 02:40 (EDT)
GOAL: Twitter degree of seperation 
ENVIRONMENT: Base 
LAST UPDATE: January 25, 2019 - 07:37 (EDT)
'''




import os 
import sys
from collections import OrderedDict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup as soup
import re


from driving_chrome import CHROME_DRIVER
import twitter_credentials



# WEBSCRAPING TWITTER USING SELENIUM
class TwitterLogin():
    ''' Set up the Twitter credentials ''' 
    
    def __init__(self, twitter_user_screen_name, twitter_username=twitter_credentials.USERNAME, twitter_pass=twitter_credentials.PASSWORD):
        self.username = twitter_username
        self.password = twitter_pass
        

    
    def start_twitter(self, login_website ='https://twitter.com/login'):
        ''' Start the chrome driver and login on to Twitter''' 
        
        try:
            # create a new Chrome session
            print('Starting...')
            
            
            # headless option
            options = Options()
#            options.add_argument('headless')
#            options.add_argument('--disable-gpu') 
#            options.add_argument('--incognito')
    
            # disable image loading    
            prefs = {"profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(CHROME_DRIVER, chrome_options=options)
            driver.implicitly_wait(60)
            driver.maximize_window()
    
            # navigate to the application home page
            driver.get('https://twitter.com/login')
            print('On Login Page')
    
            # get the username textbox
            login_field = driver.find_element_by_class_name("js-username-field")
            login_field.clear()
            
            # enter username
            login_field.send_keys(self.username)
            time.sleep(1)
            
            #get the password textbox
            password_field = driver.find_element_by_class_name("js-password-field")
            password_field.clear()
            
            #enter password
            password_field.send_keys(self.password)
            time.sleep(1)
            password_field.submit()
            
            return driver
        
        except Exception as e:
            print(e)
        
             
    def get_users(self, driver, user, follower_thres=750):
        ''' Get the followers '''
        
        try:
            # get follower page 
            start_page = 'https://twitter.com/{}/followers'.format(user)  
            driver.get(start_page)
            print("On {}'s Page".format(user))
            source = driver.page_source 
            page_soup = soup(source, 'lxml')
            
            # get total followers
            followers_count = [y.find_all('span', {"class":'ProfileNav-value'}) for y in page_soup.find_all('a', {"data-nav":'followers'})]
            total_followers = int(followers_count[0][0].attrs['data-count'])       
            print('-----{} has {} total followers-----'.format(user, total_followers))
            
            if total_followers > follower_thres:
                followers_list = 'Too Many Followers'
                return followers_list, total_followers

            if total_followers == 0:
                followers_list = 'Protected Account'
                return followers_list, total_followers

            
            # scroll time pause to allow for full loading 
            SCROLL_PAUSE_TIME = 0.5
            
            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")
            
            
            end_page = False
            repeat_load = 0
            while not end_page:
                html = driver.find_element_by_tag_name('html')
                html.send_keys(Keys.END)
                print('***SCROLL***')
                
                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                
                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    source2 = driver.page_source 
                    page_soup2 = soup(source2, 'lxml')    
                    followers_list = [link['href'] for link in page_soup2.find_all('a', {"class":'ProfileCard-screennameLink u-linkComplex js-nav'})]
#                    print(len(followers_list))
                    

                    if len(followers_list) == len(followers_list):
                        repeat_load += 1
                        if repeat_load == 3:
                            print('Tried 3x, could not reload further pages')
                            return followers_list, total_followers
                        
                    if len(followers_list) == total_followers:
                        end_page = True
                    else:
                        continue 
    
                last_height = new_height
            
            return followers_list, total_followers
            
        except Exception as e:
            print(e)
            
                
class DOS():
    ''' Apply the DOS system ''' 
    
    def __init__(self, start_node='janit27'):
        self.start_node = start_node
        self.q = [self.start_node]
        self.q_dict = OrderedDict()
        
    def node(self, max_nodes=100):
        twitter_login = TwitterLogin(twitter_user_screen_name=self.start_node)
        start_driver = twitter_login.start_twitter()         
        try:
            for n in self.q:
                print('>>>>>>>>' + str(len(self.q)))
#                print(n)
                try:
                    twitter_client = twitter_login.get_users(start_driver, n)
                    
                    if twitter_client[0] == 'Too Many Followers' or 'Protected Account':
                        self.q_dict[n] = twitter_client[0]
                        
                    
                    self.q_dict[n] = [x.strip('/') for x in twitter_client[0]]
                
                    for u in twitter_client[0]:
                        u = u.strip('/')
                        self.q.append(u)
                    
                        if len(self.q) == max_nodes:
                            start_driver.close()
                            return self.q, self.q_dict
                
                except Exception as e:
                    print("Failed to run the command on {}, Skipping...".format(n))
                    print(e)
                    continue 
    
        except:
            print('INTERRUPTED')
            start_driver.close()
            return self.q, self.q_dict
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
        


dos_test = DOS()
x_list, y_dict = dos_test.node(max_nodes=1500)
    
len(x_list)
len(y_dict.keys())

follower_len_check = dict()
for k in y_dict.keys():
    follower_len_check[k] = len(y_dict[k])


with open('dos_test.txt', 'w') as f:
    for k, v in y_dict.items():
       joined = re.match('Too Many Followers', ''.join(v))
       joined2 = re.match('Protected Account', ''.join(v))
       if joined:
           v = ''.join(v)  
       if joined2:
           v = ''.join(v)
       f.write(k + ' : ' +  str(v))
       f.write('\n'*2)










