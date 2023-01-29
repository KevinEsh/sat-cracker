from pandas import DataFrame
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://cfdiau.sat.gob.mx/nidp/wsfed/ep?id=SATUPCFDiCon&sid=5&option=credential&sid=1")

login_form = driver.find_element(By.XPATH, "/html/body/main/div/div[1]/form")

print(login_form)

# assert "No results found." not in driver.page_source
driver.close()
