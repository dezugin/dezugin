#web scraper to search and download healthcare worker history based on CNS numbers from the CNES website

import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
  

count = 0
driver = webdriver.Firefox()
df = pd.read_csv("CentrosDeSaudeBHComCPFTraduzido.csv")
names = df['CNS_PROF'].astype(str).str[:-2].unique()
for name in names:
  count = count+1
  if count < 17798:
    continue
  driver.get("http://cnes.datasus.gov.br/pages/profissionais/consulta.jsp")
  driver.set_window_size(1000, 916)
  time.sleep(0.5)
  driver.find_element(By.ID, "pesquisaValue").click()
  driver.find_element(By.ID, "pesquisaValue").send_keys(name)
  driver.find_element(By.ID, "pesquisaValue").send_keys(Keys.ENTER)
  time.sleep(0.5)
  print("Profissional nr:",count)
  try:
    driver.find_element_by_xpath('//*[@class="glyphicon glyphicon-list"]').click()
    time.sleep(1.5)
    driver.find_element_by_xpath('//*[@class="btn btn-primary ng-isolate-scope"]').click()
    print(name)
  except NoSuchElementException:
    continue
  with open('out.txt', 'w') as f:
    print(count, file=f)
    