import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from config import Config

# def main():
class SWVersionCheckinginPACT(): #SWVersionCheckinginPACT()
    
    # # cm list devices page url (PACT 2.1)
    # pact_base_url = "http://221.140.31.130:8080"
    # pact_url_listdevices = pact_base_url + "/config/dhcp/deviceConfig.do?method=fetchLst"
    # # variable for target config file URL
    # target_tlvedit_url = ""
    # # Target device CM MAC information
    # orig_cmmac = "ec:c3:02:6f:27:08"
    # tar_cmmac = orig_cmmac.replace(":", "")
    # final_cmmac = tar_cmmac.upper()
    # # Target device SW F/W file name
    # swupgdfilename = "hgj310v4_v0.3.7.img"
    
    def __init__(self, cmmac, swfilename):
        # cm list devices page url (PACT 2.1)
        # self.pact_base_url = "http://221.140.31.130:8080"
        self.pact_base_url = Config.PACT_URL_BASE
        # self.pact_url_listdevices = self.pact_base_url + "/config/dhcp/deviceConfig.do?method=fetchLst"
        self.pact_url_listdevices = Config.PACT_URL_FOR_LISTDEVICES
        # variable for target config file URL
        self.target_tlvedit_url = ""
        # Target device CM MAC information
        # orig_cmmac = "ec:c3:02:6f:27:08" #@초기화 시 인자로 받을 후보
        orig_cmmac = cmmac
        tar_cmmac = orig_cmmac.replace(":", "")
        self.final_cmmac = tar_cmmac.upper()
        # Target device SW F/W file name
        self.swupgdfilename = swfilename #@초기화 시 인자로 받을 후보
        
    
    # 1. To find a config file matched with a target CM MAC.
    # This is a part to know the link of the config file's path(URL) using Beautiful Soup
    # If you want to use pandas package, the html tags including what we want to handle must be a kind of static things. If not, we should be better to use the webdriver package.
    
    def get_filename_frm_conf(self):
        
        swfilename = ""
        
        print("=================================")
        print(f"The list devices page's url is \n{self.pact_url_listdevices}")
        print("=================================")
        response = requests.get(self.pact_url_listdevices)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        items = soup.select('table')
        
        # 1-1. There are multi tables in the page so we have to find a target table including CM MAC and config file list.
        i = 0
        table = None
        for item in items:
            # There are two table tags in the list devices page. And the target table tag is the second one.
            if i == 1:
                table = item  
                print("=================================")
                print(f'The type of table which including the list devices is {type(table)}')
                print("=================================")
                print(f'The tags of table which including the list devices is \n {str(table)}')
                print("=================================")
                break
            i = i + 1
        
        
        # 1-2. The table tags found through 1-1., a target config file link should be seperated.
        links = []
        bFlag = False
        for tr in table.findAll("tr"):
            tds = tr.findAll("td")
            for each in tds:
                try:
                    link = each.find('a')['href']
                    
                    # If the cm mac info has found in the tags, that low has the link info of the target config file.
                    if (self.final_cmmac in link) and bFlag == False:
                        bFlag = True
                    # And if bFlag is True, we have to find the link including the file extenstion '.cfg'.
                    elif (self.final_cmmac not in link) and bFlag == True:
                        if '.cfg' in link:
                            links.append(link)
                    # And then if we have already found the link including the target file extenstion, we don't need to consider saving another links. So bFlag will be set as False and quit a for loop.
                    elif (self.final_cmmac in link) and bFlag == True:
                        bFlag = False
                        break
                except:
                    pass
        print("=================================")
        print(f'The length of the links is {len(links)}')
        print("=================================")
        print(f'The links have items like this: \n {links}')
        print("=================================")
        
        
        # 2. To find a target sw f/w name is what we are purposed.
        # The item of the links which has found through 1-2.
        # And the webdriver is going to be used to get the tag data which will be created dynamically.
        # And plus, the real web browser will be opened in the background state. (option:headless)
        self.target_tlvedit_url = self.pact_base_url + links[0]
        print(f"The target config file page's url is \n{self.target_tlvedit_url}")
        
        options = webdriver.FirefoxOptions()
        options.headless = True
        
        browser = webdriver.Firefox(options=options)
        browser.implicitly_wait(3)
        browser.get(self.target_tlvedit_url)
        soup2 = BeautifulSoup(browser.page_source, 'html.parser')
        
        items2 = soup2.find_all('table')
        
        print("=================================")
        print(f'The number of the tables is {len(items2)}')
        print("=================================")
        
        # print(len(items2))
        
        # print(items2)
        
        # 2-1. To find the target table from the multi table tags
        i = 0
        table2 = None
        for item in items2:
            if i == 6:
                # print(type(item))
                print("=================================")
                print(f'The target table including the sw file name is \n {str(item)}')
                print("=================================")
                table2 = item
                
            i = i + 1
        
        # 2-2. To find the target sw file name in the config file from the table filtered on 2-1.
        # links = []
        bFlag2 = False
        # swupgdfilename = "hgj310v4_v0.4.0.img"
        
        for tr in table2.findAll("tr"):
            tds = tr.findAll("td")
            
            if bFlag2 == True:
                break
            
            for each in tds:
                try:
                    value = each.find('input')['value']            

                    print(str(each))
                    # print(type(link))
                    # print(str(link))
                    
                    if self.swupgdfilename in value:
                        print("=================================")
                        print(str(each))
                        print("=================================")
                        # print(type(link))
                        print(f'The name of the target sw upgrade file is {str(value)}. \nIt is what we want!!!')
                        print("=================================")
                        # print("Good")
                        bFlag2 = True
                        swfilename = str(value)
                        break
                    # elif bFlag2 == True:
                    #     print(f"{self.swupgdfilename} was already checked. So the execution process will be moved to the next step.")
                    #     break

                except:
                    pass
        # print(links)
        # print(len(links))
        
        
        browser.quit()
        
        return swfilename
    
    
# if __name__ == '__main__':
#     main()
#     pass