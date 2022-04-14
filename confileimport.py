import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from config import Config

# def main():
class ConfigFileImport():    
    
    
    # def __init__(self):
    def __init__(self, confilename):
        # self.url = "http://221.140.31.130:8080/tlvedit.do?method=fetchUpload"
        self.url = Config.PACT_URL_FOR_CONFIGURATION_FILE_IMPORT
    
        # self.targetconfile = "bpi_sec_na_hslee4_310V4_current.cfg"
        self.targetconfile = confilename
        
        # self.phrase_upsuccess = "Uploaded successfully"
        self.phrase_upsuccess = Config.PACT_CONFIGURATION_FILE_IMPORT_SUCCESS_MSG
        
        options = webdriver.FirefoxOptions()
        options.headless = True
        
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(3)
    
        # pass
     
    def import_target_confile(self):
        
        self.browser.get(self.url)
        self.browser.set_window_size(1514, 893)
        # time.sleep(3)
        # self.browser.find_element_by_xpath("//input[@type='file']").send_keys("D:\\03.SW Test\\06.RG\\04.JCOM\\07.HGJ310_JP_V4\\bpi_sec_na_hslee4_310V4_current.cfg")
        self.browser.find_element_by_xpath("//input[@type='file']").send_keys(Config.CONFIGURATION_FILE_LOCAL_PATH)
        self.browser.find_element(By.NAME, "tlvfor").click()
        dropdown = self.browser.find_element(By.NAME, "tlvfor")
        dropdown.find_element(By.XPATH, "//option[. = 'CM']").click()
        self.browser.find_element(By.CSS_SELECTOR, "option:nth-child(2)").click()
        self.browser.find_element(By.NAME, "noedit").click()
        self.browser.find_element(By.CSS_SELECTOR, "input:nth-child(10)").click()
        
        url2 = self.browser.current_url
        
        print(f"First opended page's url is '{self.url}'.")
        print(f"Second opend page's url is '{url2}'.")
        
        if url2 == self.url:
            sys.exit('url and url2 should not be the same!')
        
        # df = pd.read_html(str(url2))    
        # print(df)
        
        soup = BeautifulSoup(self.browser.page_source, 'html.parser')
        
        tags_font = soup.find_all('font')
        
        print(f"Number of font tags in the current web page is '{len(tags_font)}'")
        
        for tag in tags_font:
            print(f"font tag is {str(tag)}")
            if self.phrase_upsuccess in str(tag):
                print("Target config file has uploaded successfully!")
        
        tags_table = soup.find_all('table')
        
        print(f"Number of table tags in the current web page is '{len(tags_table)}'")
        
        table = None
        i = 0
        for tag in tags_table:
            if i == 1:
                table = tag
            
            i = i + 1
        bFlag = False
        
        for tr in table.findAll("tr"):
            if bFlag == True:
                break
            tds = tr.findAll("td")
            for each in tds:
                try:
                    value = each.find('a')['href']
                    # print(f"td tag is : {value}")
                    
                    if self.targetconfile in value:
                        print("OK")
                        bFlag = True
                        break
                except:
                    pass
            
        self.browser.quit()
        
        return bFlag
        # pass

# def main():
#     config_import = ConfigFileImport("bpi_sec_na_hslee4_310V4_current.cfg")
#     config_import.import_target_confile()

# if __name__ == '__main__':    
#     main()
#     pass