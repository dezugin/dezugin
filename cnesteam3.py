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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException
import time
import pandas as pd

continueCount = 1
continueMonth = 12
continueYear = 2010
driver = webdriver.Firefox()
key = int("2695472")
centrosDeSaude = pd.read_csv('CentrosDeSaudeBHComCPFTraduzido.csv')
keys = centrosDeSaude['CNES'].unique().astype(int)
count = 0
for key in keys:
  if count<continueCount:
    count = count +1
    continue
  cnes = f'{key:07d}'
  driver.get("http://cnes.datasus.gov.br/pages/estabelecimentos/consulta.jsp")
  driver.set_window_size(1000, 916)
  time.sleep(0.8)
  driver.find_element(By.ID, "pesquisaValue").click()
  out = " Inicio: "+cnes+" Count: "+str(count)
  with open('out.txt', 'w') as f:
    print(out, file=f)
  print(out)
  driver.find_element(By.ID, "pesquisaValue").send_keys(cnes)
  driver.find_element(By.ID, "pesquisaValue").send_keys(Keys.ENTER)
  time.sleep(0.5)
  driver.find_element(By.CSS_SELECTOR, ".glyphicon-list").click()
  driver.find_element(By.CSS_SELECTOR, "li:nth-child(11) span").click()
  time.sleep(0.8)
  out = " Atual: "+cnes+" Count: "+str(count)
  with open('out.txt', 'w') as f:
    print(out, file=f)
  print(out)
  for i in range(1,11):
    if count<continueCount+1:
      continue
    try:
      driver.find_element(By.CSS_SELECTOR, f'.ng-scope:nth-child({i}) > .text-center .glyphicon').click()
      rows = len (driver.find_elements_by_xpath("//*[@id='listaProfEquipes']/tbody/tr"))
      columns = len (driver.find_elements_by_xpath("//*[@id='listaProfEquipes']/tbody/tr[2]/td"))
      before_XPath = "//*[@id='listaProfEquipes']/tbody/tr["
      aftertd_XPath = "]/td["
      aftertr_XPath = "]"
      time.sleep(0.3)
      text = driver.find_element_by_xpath("//*[@id='listaProfEquipes']/thead/tr[1]/th").text
      if len(text)>0:
        #title = text.splitlines()[1]
        title = text
        dataframelist = []
        for t_row in range(2, (rows + 1)):
          dataframerow = []
          dataframerow.append(title)
          for t_column in range(1, (columns + 1)):
            FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
            cell_text = driver.find_element_by_xpath(FinalXPath).text
            dataframerow.append(cell_text)
          dataframerow.append("10/21")
          dataframerow.append(cnes)  
          dataframelist.append(dataframerow)
        df = pd.DataFrame(dataframelist, columns=['Equipe','Nome','CNS','CBO','Atividade','Equipe Minima','Hospitalar','Ambulatorial','Outras','Diferenciada','Complementar','Data Entrada','Data do arquivo','CNES'])
        title = title.replace("/", "-")
        df.to_csv(f'/home/dez/selenium/data/{cnes}-{title}10-21.csv')
      time.sleep(0.3)
      ActionChains(driver).send_keys(Keys.ESCAPE).perform()
      time.sleep(0.5)
    except (NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException):
      outatual = cnes+'\n'
      with open('outcnes.txt', 'a') as f:
        f.write(outatual)
      continue
  for i in range(1,11):
    if count<continueCount+1:
      continue
    try:  
      driver.find_element(By.LINK_TEXT, "2").click()
      driver.find_element(By.CSS_SELECTOR, f'.ng-scope:nth-child({i}) > .text-center .glyphicon').click()
      rows = len (driver.find_elements_by_xpath("//*[@id='listaProfEquipes']/tbody/tr"))
      columns = len (driver.find_elements_by_xpath("//*[@id='listaProfEquipes']/tbody/tr[2]/td"))
      before_XPath = "//*[@id='listaProfEquipes']/tbody/tr["
      aftertd_XPath = "]/td["
      aftertr_XPath = "]"
      time.sleep(0.3)
      text = driver.find_element_by_xpath("//*[@id='listaProfEquipes']/thead/tr[1]/th").text
      if len(text)>0:
        #title = text.splitlines()[1]
        title = text
        dataframelist = []
        for t_row in range(2, (rows + 1)):
          dataframerow = []
          dataframerow.append(title)
          for t_column in range(1, (columns + 1)):
            FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
            cell_text = driver.find_element_by_xpath(FinalXPath).text
            dataframerow.append(cell_text)
          dataframerow.append("10/21")
          dataframerow.append(cnes)  
          dataframelist.append(dataframerow)
        df = pd.DataFrame(dataframelist, columns=['Equipe','Nome','CNS','CBO','Atividade','Equipe Minima','Hospitalar','Ambulatorial','Outras','Diferenciada','Complementar','Data Entrada','Data do arquivo','CNES'])
        title = title.replace("/", "-")
        df.to_csv(f'/home/dez/selenium/data/{cnes}-{title}10-21.csv')
      time.sleep(0.3)
      ActionChains(driver).send_keys(Keys.ESCAPE).perform()
      time.sleep(0.5)
    except (NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException):
      outatual = cnes+'(2)\n'
      with open('outcnes.txt', 'a') as f:
        f.write(outatual)
      continue
  for ano in range(2021,2006,-1):
    for mes in range(12,0,-1):

      data = f'{mes:02d}/{ano}'
      data2 = f'{mes:02d}-{ano}'
      if (count==continueCount and ano>continueYear) or (count ==continueCount and (ano >= continueYear and mes >continueMonth)):
        continue
      try:
        time.sleep(0.5)
        driver.find_element_by_xpath("//*[@id='estabContent']/header/nav/form/div/select").click()
        driver.find_element(By.XPATH, f"//option[. = '{data}']").click()
        out = data+" Inicio: "+cnes+" Count: "+str(count)
        with open('out.txt', 'w') as f:
          print(out, file=f)
        print(out)
        for i in range(1,11):
          try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            driver.find_element(By.CSS_SELECTOR, f'.ng-scope:nth-child({i}) > .text-center .glyphicon').click()
            rows = len (driver.find_elements_by_xpath("//*[@id='listaProfEquipes']/tbody/tr"))
            columns = len (driver.find_elements_by_xpath("//*[@id='listaProfEquipes']/tbody/tr[2]/td"))
            before_XPath = "//*[@id='listaProfEquipes']/tbody/tr["
            aftertd_XPath = "]/td["
            aftertr_XPath = "]"
            time.sleep(0.3)
            text = driver.find_element_by_xpath("//*[@id='listaProfEquipes']/thead/tr[1]/th").text
            if len(text)>0:
              #title = text.splitlines()[1]
              title = text
              dataframelist = []
              for t_row in range(2, (rows + 1)):
                dataframerow = []
                dataframerow.append(title)
                for t_column in range(1, (columns + 1)):
                  FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
                  cell_text = driver.find_element_by_xpath(FinalXPath).text
                  dataframerow.append(cell_text)
                dataframerow.append(data)
                dataframerow.append(cnes)  
                dataframelist.append(dataframerow)
              df = pd.DataFrame(dataframelist, columns=['Equipe','Nome','CNS','CBO','Atividade','Equipe Minima','Hospitalar','Ambulatorial','Outras','Diferenciada','Complementar','Data Entrada','Data do arquivo','CNES'])
              title = title.replace("/", "-")
              df.to_csv(f'/home/dez/selenium/data/{cnes}-{title}{data2}.csv')
            time.sleep(0.3)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.5)
          except NoSuchElementException:
            continue
          except ElementClickInterceptedException:
            continue
          except StaleElementReferenceException:
            continue
        for i in range(1,11):
          try:
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()  
            driver.find_element(By.LINK_TEXT, "2").click()
            driver.find_element(By.CSS_SELECTOR, f'.ng-scope:nth-child({i}) > .text-center .glyphicon').click()
            rows = len (driver.find_elements_by_xpath("//*[@id='listaProfEquipes']/tbody/tr"))
            columns = len (driver.find_elements_by_xpath("//*[@id='listaProfEquipes']/tbody/tr[2]/td"))
            before_XPath = "//*[@id='listaProfEquipes']/tbody/tr["
            aftertd_XPath = "]/td["
            aftertr_XPath = "]"
            time.sleep(0.3)
            text = driver.find_element_by_xpath("//*[@id='listaProfEquipes']/thead/tr[1]/th").text
            if len(text)>0:
              #title = text.splitlines()[1]
              title = text
              dataframelist = []
              for t_row in range(2, (rows + 1)):
                dataframerow = []
                dataframerow.append(title)
                for t_column in range(1, (columns + 1)):
                  FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
                  cell_text = driver.find_element_by_xpath(FinalXPath).text
                  dataframerow.append(cell_text)
                dataframerow.append(data)
                dataframerow.append(cnes)  
                dataframelist.append(dataframerow)
              df = pd.DataFrame(dataframelist, columns=['Equipe','Nome','CNS','CBO','Atividade','Equipe Minima','Hospitalar','Ambulatorial','Outras','Diferenciada','Complementar','Data Entrada','Data do arquivo','CNES'])
              title = title.replace("/", "-")
              df.to_csv(f'/home/dez/selenium/data/{cnes}-{title}{data2}.csv')
            time.sleep(0.3)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(0.5)
          except NoSuchElementException:
            continue
          except StaleElementReferenceException:
            continue
          except ElementClickInterceptedException:
            continue
      except ElementClickInterceptedException:
        continue
      except NoSuchElementException:
        continue
    out = data+" Fim:"+cnes+" Count: "+str(count)
    with open('out.txt', 'w') as f:
      print(out, file=f)
    print(out)
  out = "Terminando: "+cnes+" Count: "+str(count)
  with open('out.txt', 'w') as f:
    print(out, file=f)
  print(out)
  count = count + 1