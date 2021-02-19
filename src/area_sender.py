from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select

options = Options()
options.binary_location = '/usr/bin/firefox'
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)

driver.get('https://radiko.jp/contact3')
element = driver.find_element_by_id("area_name")

if element.text != '東京都':
  print('ずれている')
  element = driver.find_element_by_name("prefecture")
  text_for_select = "東京都"
  select = Select(element)
  select.select_by_visible_text(text_for_select)
  
  confirm_element = driver.find_element_by_id("confirmbtn")
  confirm_button_element = confirm_element.find_element_by_class_name("confirm")
  confirm_button_element.click()

  driver.set_page_load_timeout(5)
  confirm_element = driver.find_element_by_id("confirmbtn2")
  confirm_button_element = confirm_element.find_element_by_class_name("send")
  confirm_button_element.click()

driver.quit()
