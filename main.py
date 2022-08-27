from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import lxml
from bs4 import BeautifulSoup
import time
import requests
CHROME_DRIVER_PATH="/home/akshay/Desktop/hdoc/chromedriver_linux64/chromedriver"
FORM_LINK="https://forms.gle/Uyea5PfNfCj6KpWV7"
SHEET_LINK="https://docs.google.com/spreadsheets/d/1ifB10ZQzD5w5AD9R1dDtAjIEC3zJ9R3aZGx2hgLa9So/edit?resourcekey#gid=1806185620"
MAX_BUDGET=15000
CITY="Trivandrum"


class SearchSite:
    def __init__(self,path):
        self.driver=webdriver.Chrome(executable_path=path)
        self.driver.get("https://www.99acres.com/")
        self.driver.maximize_window()
        time.sleep(3)
        rent=self.driver.find_element(By.XPATH,'//*[@id="inPageSearchForm_1"]')
        rent.click()
        time.sleep(1)
        search_box=self.driver.find_element(By.XPATH,'//*[@id="keyword2"]')
        search_box.send_keys(CITY)
        time.sleep(1)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)
        set_budget=self.driver.find_element(By.XPATH,'//*[@id="undefined"]')
        set_budget.click()
        time.sleep(1)
        budgets=self.driver.find_elements(By.CSS_SELECTOR," #lf_budget_max_list li")
        time.sleep(2)
        for i in budgets:
            temp=i.get_attribute("textContent")
            if temp=="Max Budget":
                continue
            amt=int(temp.replace(",",""))
            if amt>=MAX_BUDGET or amt==95000:
                i.click()
                break;
        time.sleep(5)
        self.rents=[]
        self.addresses=[]
        self.links=[]
        x=self.driver.find_elements(By.ID,"srp_tuple_price")
        for i in x:
            temp=int(i.get_attribute("textContent").split(' ')[1].replace(",",""))
            self.rents.append(temp)
        x=self.driver.find_elements(By.CLASS_NAME,"srpTuple__tupleTitleOverflow")
        for i in x:
            self.addresses.append(i.get_attribute("textContent"))
        x=self.driver.find_elements(By.CSS_SELECTOR,".srpTuple__tdClassPremium a")
        for i in x:
            self.links.append(i.get_attribute("href"))

    def close_window(self):
        self.driver.close()

class EnterData:
    def __init__(self,rent_list,addr_list,link_list):
        self.driver=webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.driver.get(FORM_LINK)
        self.driver.maximize_window()
        time.sleep(2)
        for i,j,k in zip(rent_list,addr_list,link_list):
            q1=self.driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            q2=self.driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            q3=self.driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            q1.send_keys(j)
            time.sleep(1)
            q2.send_keys(i)
            time.sleep(1)
            q3.send_keys(k)
            time.sleep(1)
            submit=self.driver.find_element(By.XPATH,'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
            submit.click()
            time.sleep(2)
            goback=self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div/div[4]/a[2]')
            goback.click()
            time.sleep(2)
        self.driver.close()
        self.driver2=webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.driver2.get(SHEET_LINK)
        self.driver2.maximize_window()

x=SearchSite(CHROME_DRIVER_PATH)
x.close_window()
y=EnterData(x.rents,x.addresses,x.links)
