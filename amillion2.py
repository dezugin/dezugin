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

driver = webdriver.Firefox()
driver.get("https://www.amil.com.br/portal/web/servicos/saude/rede-credenciada/amil/busca-avancada")
driver.set_window_size(1000, 974)

# wait and accept cookies
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="onetrust-accept-btn-handler"]')))
driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()

# click on "Plano ou rede", wait for options and click
driver.find_element(By.CSS_SELECTOR, "#plano_saude_avancada_chosen b").click()
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,  '/html/body/div[1]/section/form/div[1]/fieldset/dl[2]/dd/div/div/ul/li[2]')))
driver.find_element(By.XPATH, '/html/body/div[1]/section/form/div[1]/fieldset/dl[2]/dd/div/div/ul/li[2]').click()

# click on "Estado", wait for options and click
driver.find_element(By.CSS_SELECTOR, "#estado_saude_avancada_chosen b").click()
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,  '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[1]/div/div/ul/li[1]')))
driver.find_element(By.XPATH, '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[1]/div/div/ul/li[2]').click()

# click on "Municipio", wait for options and click
# '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[2]/div/div/ul/li'
# '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[2]/div/div/ul/li[1]'
# '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[2]/div/div/ul/li[2]'
driver.find_element(By.CSS_SELECTOR, "#municipio_saude_avancada_chosen b").click()
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,  '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[2]/div/div/ul/li[1]')))
driver.find_element(By.XPATH,  '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[2]/div/div/ul/li[2]').click()

# click on "Bairro", wait for options and click
driver.find_element(By.CSS_SELECTOR, "#bairro_saude_avancada_chosen b").click()
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[3]/div/div/ul/li[1]')))
driver.find_element(By.XPATH, '/html/body/div[1]/section/form/div[2]/fieldset/dl/dd[3]/div/div/ul/li[1]').click()

# click on "Tipo de servico", wait for options and click
driver.find_element(By.CSS_SELECTOR, "#tipo_servico_saude_avancada_chosen span").click()
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/form/div[3]/fieldset/div/dl[1]/dd[1]/div/div/ul/li[1]')))
driver.find_element(By.XPATH, '/html/body/div[1]/section/form/div[3]/fieldset/div/dl[1]/dd[1]/div/div/ul/li[1]').click()

# click on "Especialidade", wait for options and click
driver.find_element(By.CSS_SELECTOR, "#especialidade_saude_avancada_tipo_chosen span").click()
element = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/form/div[3]/fieldset/div/dl[1]/dd[2]/div/div/ul/li[1]')))
driver.find_element(By.XPATH, '/html/body/div[1]/section/form/div[3]/fieldset/div/dl[1]/dd[2]/div/div/ul/li[1]').click()
driver.find_element(By.ID, "selecionar-prestador").click()

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')
spam = soup.find_all('span')
#re.compile('<span class="(.*?)">')
#,re.compile('<span\b[^>]*>(.*?)</span>')
#print("spam: ",spam)
for unit in spam:
  #print("unit: ",unit)
  #if 'class' in str(unit):
  title = re.search('<span class="(.*?)">',str(unit))
  text = re.search('<span\b[^>]*>(.*?)</span>',str(unit))
  if title is not None:
    title = title.group()
    title = title[13:-2]
  if text is not None:
    text = text.group()
  print('title: ',title)
  #print('text: ',text)
  print('tex2t: ', unit.get_text())