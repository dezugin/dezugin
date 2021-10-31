import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, WebDriverException, TimeoutException
import time
import pandas as pd
import traceback

#load CNES file, webdriver and current count of CNES number
with open('restart.txt','r') as c:
  count = int(c.read())-1
centrosDeSaude = pd.read_csv('CentrosDeSaudeBHComCPFTraduzido.csv')
keys = centrosDeSaude['CNES'].unique().astype(int)
conditionalKey = 0
driver = webdriver.Firefox()

#loop to iterate through entire CNES list
while count<len(keys):

  try:

    #values of consecutive CNES number to begin from, month and year
    continueCount = count
    continueMonth = 13
    continueYear = 2022

    #main loop, iterate through keys
    for key in keys:
      if count<=continueCount:
        print(count," + ",keys[count]," + ",continueCount)
        count = count +1
      key = keys[count]
      cnes = f'{key:07d}'
      conditionForReloading = True

      #repeatedly access website until it loads
      while(conditionForReloading == True):
        try:
          driver.get(f'http://cnes.datasus.gov.br/pages/estabelecimentos/ficha/index.jsp?coUnidade=310620{cnes}')
          driver.set_window_size(1000, 916)
          element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cnes")))
          conditionForReloading = False
        except TimeoutException:
          print("Website loading not successful")

      out = " Inicio: "+cnes+" Count: "+str(count)
      with open('out.txt', 'a') as f:
        print(out, file=f)
      print(out)
      driver.find_element(By.CSS_SELECTOR, "li:nth-child(11) span").click()
      out = " Atual: "+cnes+" Count: "+str(count)
      with open('out.txt', 'a') as f:
        print(out, file=f)
      print(out)

      # downloading current year's data
      for i in range(1,11):

        if count<=continueCount:
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
            title = text
            dataframelist = []

            for t_row in range(2, (rows + 1)):
              dataframerow = []
              dataframerow.append(title)
              for t_column in range(1, (columns + 1)):
                FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
                cell_text = driver.find_element_by_xpath(FinalXPath).get_attribute("innerHTML")
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

        except (NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException,ElementNotInteractableException) as e:
          error = str(e)
          with open('except.txt', 'w') as f:
            f.write(error)
          outatual = cnes+'\n'+error
          with open('outcnes.txt', 'a') as f:
            f.write(outatual)
          continue

      #downloading current year's data, second tab

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
            title = text
            dataframelist = []

            for t_row in range(2, (rows + 1)):
              dataframerow = []
              dataframerow.append(title)
              for t_column in range(1, (columns + 1)):
                FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
                cell_text = driver.find_element_by_xpath(FinalXPath).get_attribute("innerHTML")
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

        except (NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException,ElementNotInteractableException)as e:
          error = str(e)
          with open('except.txt', 'w') as f:
            f.write(error)
          outatual = cnes+'(2)\n'+error
          with open('outcnes.txt', 'a') as f:
            f.write(outatual)
          continue

      #download data from years 2021 to 2007
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
            with open('out.txt', 'a') as f:
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
                  title = text
                  dataframelist = []

                  for t_row in range(2, (rows + 1)):
                    dataframerow = []
                    dataframerow.append(title)
                    for t_column in range(1, (columns + 1)):
                      FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
                      cell_text = driver.find_element_by_xpath(FinalXPath).get_attribute("innerHTML")
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
              except (NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException)as e:
                error = str(e)
                with open('except.txt', 'w') as f:
                  f.write(error)
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
                  title = text
                  dataframelist = []

                  for t_row in range(2, (rows + 1)):
                    dataframerow = []
                    dataframerow.append(title)
                    for t_column in range(1, (columns + 1)):
                      FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
                      cell_text = driver.find_element_by_xpath(FinalXPath).get_attribute("innerHTML")
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
              except (NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException)as e:
                error = str(e)
                with open('except.txt', 'w') as f:
                  f.write(error)
                continue

          except (NoSuchElementException,ElementClickInterceptedException,StaleElementReferenceException)as e:
            error = str(e)
            with open('except.txt', 'w') as f:
              f.write(str(count)+error)
            continue
          except (ElementNotInteractableException) as e:
            error = str(e)
            with open('except.txt', 'w') as f:
              f.write(str(count)+error)
            outatual = cnes+'(3)\n'+str(data)+error
            with open('outcnes.txt', 'a') as f:
              f.write(str(count)+outatual)
            continue

        out = str(count)+data+" Fim:"+cnes+" Count: "+str(count)
        with open('out.txt', 'a') as f:
          print(out, file=f)
        print(out)

      out = str(count)+"Terminando: "+cnes+" Count: "+str(count)
      with open('out.txt', 'a') as f:
        print(out, file=f)
      print(out)
      count = count + 1
      with open('restart.txt','w') as cou:
        print(count,file=cou)
    with open('restart.txt', 'w') as f:
      countln = str(count)
      print(countln, file=f)
  except Exception:
    with open('restart.txt','r') as c:
      count = int(c.read())
    with open('restart2.txt','a') as f2:
      countln = str(count)
      print(countln,file=f2)
    with open('restarterror.txt', 'a') as f:
      traceback.print_exc(file=f)
    continue
