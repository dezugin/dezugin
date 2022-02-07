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
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Firefox()
driver.get("https://www.amil.com.br/portal/web/servicos/saude/rede-credenciada/amil/busca-avancada")
driver.set_window_size(1000, 974)

# wait and accept cookies
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

while(True):
  for plano in range(2,942):
    if plano == 163:
      continue
    # click on "Plano ou rede", wait for options and click
    driver.find_element(By.CSS_SELECTOR, "#plano_saude_avancada_chosen b").click()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,  '/html/body/div[1]/section/form/div[1]/fieldset/dl[2]/dd/div/div/ul/li[2]')))
    try: 
      driver.find_element(By.XPATH, f'/html/body/div[1]/section/form/div[1]/fieldset/dl[2]/dd/div/div/ul/li[{plano}]').click()
    except NoSuchElementException:
      print(f'No plano{plano}')
      continue
    for estado in range(1,27):
      # click on "Estado", wait for options and click
      driver.find_element(By.CSS_SELECTOR, "#estado_saude_avancada_chosen b").click()
      element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,  '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[1]/div/div/ul/li[1]')))
      try:
        driver.find_element(By.XPATH, f'/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[1]/div/div/ul/li[{estado}]').click()
      except NoSuchElementException:
        print(f'No estado{estado}')
        continue
      for municipio in range(1,209):
        # click on "Municipio", wait for options and click
        driver.find_element(By.CSS_SELECTOR, "#municipio_saude_avancada_chosen b").click()
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,  '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[2]/div/div/ul/li[1]')))
        try:
          driver.find_element(By.XPATH,  f'/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[2]/div/div/ul/li[{municipio}]').click()
        except NoSuchElementException:
          print(f'No municipio{municipio}')
          continue
        # click on "Bairro", wait for options and click option todos os bairros
        driver.find_element(By.CSS_SELECTOR, "#bairro_saude_avancada_chosen b").click()
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[3]/div/div/ul/li[1]')))
        driver.find_element(By.XPATH, '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[3]/div/div/ul/li[1]').click()

        # click on "Tipo de servico", wait for options and click consultorio/clinicas
        driver.find_element(By.CSS_SELECTOR, "#tipo_servico_saude_avancada_chosen span").click()
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/form/div[3]/fieldset/div/dl[1]/dd[1]/div/div/ul/li[1]')))
        driver.find_element(By.XPATH, '/html/body/div[1]/section/form/div[3]/fieldset/div/dl[1]/dd[1]/div/div/ul/li[1]').click()

        for especialidade in range(1,77):
          # click on "Especialidade", wait for options and click
          driver.find_element(By.CSS_SELECTOR, "#especialidade_saude_avancada_tipo_chosen span").click()
          element = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/form/div[3]/fieldset/div/dl[1]/dd[2]/div/div/ul/li[1]')))
          try:
            driver.find_element(By.XPATH, f'/html/body/div[1]/section/form/div[3]/fieldset/div/dl[1]/dd[2]/div/div/ul/li[{especialidade}]').click()
          except NoSuchElementException:
            print(f'No especialidade{especialidade}')
            continue
          driver.find_element(By.ID, "selecionar-prestador").click()

          # download and save data into a csv file
          page_source = driver.page_source
          soup = BeautifulSoup(page_source, 'lxml')
          spam = soup.find_all('span')
          frame = []
          for unit in spam:
            title = re.search('<span class="(.*?)">',str(unit))
            if title is not None:
              title = title.group()
              title = title[13:-2]
            print('title: ',title)
            text = unit.get_text()
            print('text: ', text)
            
            row = {'title': title, 'text':text}
            frame.append(row)
          df = pd.DataFrame(frame)
          df.to_csv(f'dataamil/dados-plano{plano}-estado{estado}-municipio{municipio}-especialidade{especialidade}.csv')
          print(f'Salvo dataamil/dados-plano{plano}-estado{estado}-municipio{municipio}-especialidade{especialidade}.csv')