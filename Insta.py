from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from xlsxwriter import Workbook
import os
import requests
import shutil


class App:
    def __init__(self, username='username', password='password', target_username='username', #enter details here
                 path='/Users/Hp/Desktop/data science/Web scraping/Images'):
        self.username = username
        self.password = password
        self.target_username = target_username
        self.path = path
        self.driver = webdriver.Chrome('C:/Users/hp/Downloads/chromedriver')
        self.error = False
        self.main_url = 'https://www.instagram.com'
        self.all_images = []
        self.driver.get(self.main_url)
        sleep(3)
        self.log_in()
        if self.error is False:
            self.close_dialog_box()
            self.open_target_profile()
        if self.error is False:
            self.scroll_down()
        if self.error is False:
            if not os.path.exists(path):
                os.mkdir(path)
            self.downloading_images()
        sleep(3)
        #self.driver.close()



    def downloading_images(self):
        self.all_images = list(set(self.all_images))
        #self.download_captions(self.all_images)
        print('Length of all images', len(self.all_images))
        for index, image in enumerate(self.all_images):
            filename = 'image_' + str(index) + '.jpg'
            image_path = os.path.join(self.path, filename)
            link = image['src']
            print('Downloading image', index)
            response = requests.get(link, stream=True)
            try:
                with open(image_path, 'wb') as file:
                    shutil.copyfileobj(response.raw, file)  # source -  destination
            except Exception as e:
                print(e)
                print('Could not download image number ', index)
                print('Image link -->', link)

    def scroll_down(self):
        try:
            no_of_posts = self.driver.find_element_by_xpath('//span[text()=" posts"]').text
            no_of_posts = no_of_posts.replace(' posts', '')
            no_of_posts = str(no_of_posts).replace(',', '')  # 15,483 --> 15483
            self.no_of_posts = int(no_of_posts)
            if self.no_of_posts > 24:
                no_of_scrolls = int(self.no_of_posts/12) + 3
                try:
                    for value in range(no_of_scrolls):
                        soup = BeautifulSoup(self.driver.page_source, 'lxml')
                        for image in soup.find_all('img'):
                            self.all_images.append(image)

                        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                        sleep(2)
                except Exception as e:
                    self.error = True
                    print(e)
                    print('Some error occurred while trying to scroll down')
            sleep(10)
        except Exception:
            print('Could not find no of posts while trying to scroll down')
            self.error = True

    def open_target_profile(self):
        try:
            search_bar = self.driver.find_element_by_xpath('//input[@placeholder="Search"]')
            search_bar.send_keys(self.target_username)
            target_profile_url = self.main_url + '/' + self.target_username + '/'
            self.driver.get(target_profile_url)
            sleep(3)

        except Exception:
            self.error = True
            print('Could not find search bar')

    def close_dialog_box(self):
        # reload page
        sleep(2)
        self.driver.get(self.driver.current_url)
        sleep(3)

        try:
            sleep(3)
            not_now_btn = self.driver.find_element_by_xpath('//*[text()="Not Now"]')
            sleep(3)

            not_now_btn.click()
            sleep(1)
        except Exception:
            pass

    def log_in(self, ):
        #try:
            #log_in_button = self.driver.find_element_by_link_text('Log in')
            #log_in_button.click()
            #sleep(3)
        #except Exception:
            #self.error = True
            #print('Unable to find login button')
        #else:
            try:
                user_name_input = self.driver.find_element_by_xpath('//input[@aria-label="Phone number, username, or email"]')
                user_name_input.send_keys(self.username)
                sleep(3)

                password_input = self.driver.find_element_by_xpath('//input[@aria-label="Password"]')
                password_input.send_keys(self.password)
                sleep(3)

                user_name_input.submit()
                sleep(3)

                #self.close_settings_window_if_there()
            except Exception:
                print('Some exception occurred while trying to find username or password field')
                self.error = True

if __name__ == '__main__':
    app = App()
