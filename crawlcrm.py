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
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import re
import pandas as pd

CLEANR = re.compile('<.*?>') 
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext
CLEANDATE = re.compile('[0-9]{2}/[0-9]{2}/[0-9]{4}')
def cleanhtmldate(raw_html):
  cleantext = re.findall(CLEANDATE, raw_html)
  return cleantext
CLEANINSCRICOES = re.compile('Inscriçõesemoutroestado:')
def cleanhtmlinscricoes(raw_html):
  cleantext = re.sub(CLEANINSCRICOES,'', raw_html)
  return cleantext
driver = webdriver.Firefox()
df = None

residencia = pd.read_csv('/home/dez/selenium/Base - MFC com Residência - Brasil - Sheet1.csv')
driver.get("https://portal.cfm.org.br/busca-medicos/")
driver.set_window_size(1000, 916)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[4]/div[2]/button")))
driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/button").click()
tamanho = len(residencia.index)
#print(tamanho)
#count = 0
with open('restartcrm.txt','r') as c:
  count = int(c.read())+1
print(count)
def downloadCrmInfoFromWebsite(index, row,driver):
  driver.refresh()
  element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/section[2]/div/div/div/article/div[2]/div/div/form/div/div[1]/div[1]/div/label")))
  #driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/button").click()
  estado = row['UF']
  crm = int(row['CRM'])
  print(f"Processando médico nr {index}, {index/tamanho}%, nome: {row['Médico']}, {crm}-{estado}")
  
  driver.find_element(By.NAME, "crm").clear()
  dropdown = driver.find_element(By.ID, "uf")
  Select(dropdown).select_by_value(estado)
  crmMenu = driver.find_element(By.NAME, "crm")
  driver.execute_script("arguments[0].click();", crmMenu)
  driver.find_element(By.NAME, "crm").send_keys(crm)
  driver.find_element(By.NAME, "crm").send_keys(Keys.ENTER)

  element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/section[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/div[1]")))
  str = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/div[2]').get_attribute("innerHTML")
  str = "".join(str.split())
  dataDeInscricao = cleanhtml(str)
  dataDeInscricao = cleanhtmldate(dataDeInscricao)[0]
  str = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/div[1]').get_attribute("innerHTML")
  str = "".join(str.split())
  crmMedico = cleanhtml(str)
  str = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[3]/div').get_attribute("innerHTML")
  str = "".join(str.split())
  outroEstado = cleanhtml(str)
  outroEstado = cleanhtmlinscricoes(outroEstado)
  str = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/section[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[5]/div').get_attribute("innerHTML")
  especialidade = cleanhtml(str)
  if 'Endereço:' in especialidade:
    especialidade = 'Médico sem especialidade registrada.'
  data = {'Data de Inscrição':dataDeInscricao,'CRM':crmMedico,'CRM Outro Estado':outroEstado,'Especialidade':especialidade}
  print(data)
  df = pd.DataFrame(data,index=[0])
  df.to_csv(f'/home/dez/selenium/crmdata/{index}-crm-{crm}.csv')
  with open('outcrm.txt', 'a') as f:
    print(f'{index} - {crm}', file=f)
  with open('restartcrm.txt', 'w') as f:
    print(index, file=f)
while count<6256:
  for index, row in residencia.iterrows():
      if index<count:
        continue
      try: 
        downloadCrmInfoFromWebsite(index, row,driver) 
        count = count + 1
      except Exception:
        flag = False
        while not flag:
          try:
            downloadCrmInfoFromWebsite(index, row,driver)
            flag = True
            count = count + 1
          except Exception:
            pass