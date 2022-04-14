import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from config import Config

# def main():
# configfiledeploy
class ConfigFileDeploy(): 
    
    def __init__(self):
        
        # self.url = "http://221.140.31.130:8080/deploy.do?method=fetch&boatype=DHCP"
        self.url = Config.PACT_URL_FOR_CONFIGURATION_FILE_DEPLOY
    
        # self.phrase_depsuccess = "DHCP deployment successful"
        self.phrase_depsuccess = Config.PACT_CONFIGURATION_FILE_DEPLOY_SUCCESS_MSG
        
        options = webdriver.FirefoxOptions()
        options.headless = True
        
        self.browser = webdriver.Firefox(options=options)    
        # browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def deploy_confile(self):
        self.browser.get(self.url)
        self.browser.set_window_size(1514, 893)
        
        self.browser.find_element(By.NAME, "deploy_boa").click()
        
        time.sleep(10)
        
        # find_element(By.CSS_SELECTOR, "body").click()
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        
        tags_font = soup.find_all('font')
        
        print(f"Number of font tags in the current web page is '{len(tags_font)}'")
        
        bflag = False
        
        for tag in tags_font:
            print(f"font tag is {str(tag)}")
            if self.phrase_depsuccess in str(tag):
                bflag = True
                print("Target config file has uploaded successfully!")
            
        self.browser.quit()
        
        return bflag

# if __name__ == '__main__':    
#     main()
#     pass