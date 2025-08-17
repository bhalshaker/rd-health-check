import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# Get Environment type from environment variable
environment=os.getenv("ENVIRONMENT_TYPE",'')
options=Options()
# if environment type is container then run chrome in headless mode
if environment.lower()=='container':
    options.headless = True


def test_page_at_start_has_empty_regions():
    # Load Chrome webdriver
    driver= webdriver.Chrome(options)
    # Open Demo Dashboard Page
    driver.get("http://localhost:8000")
    # Get elements regions that they exists but they do not have childs
    regions_to_be_inspected=["databases-card-body","webservices-card-body","requirement-files-card-body","mount-points-card-body"]
    for region in regions_to_be_inspected:
        region_holder=driver.find_elements(By.ID,region)
        assert len(region_holder)>0
        assert len(region_holder[0].find_elements(By.XPATH,"./*"))==0
    driver.quit()

def test_page_select_all_healthcheck_results():
    # Load Chrome webdriver
    driver= webdriver.Chrome(options)
    # Open Demo Dashboard Page
    driver.get("http://localhost:8000")
    # Get elements regions that they exists but they do not have childs
    regions_to_be_inspected=["databases-card-body","webservices-card-body","requirement-files-card-body","mount-points-card-body"]
    for region in regions_to_be_inspected:
        region_holder=driver.find_elements(By.ID,region)
        assert len(region_holder)>0
        assert len(region_holder[0].find_elements(By.XPATH,"./*"))==0
    # Select drop down list and set selection value to All Healthchecks
    drop_down_list=driver.find_element(By.ID,'select-healthcheck')
    select=Select(drop_down_list)
    select.select_by_index(1)
    # Get Display Button and click on it
    display_button=driver.find_element(By.ID,'display-healthcheck-btn')
    display_button.click()
    # Wait until data is fetched and cards displayed with maximum timeout of five seconds
    wait= WebDriverWait(driver,5)
    wait.until(lambda drv: any (len(drv.find_element(By.ID, region).find_elements(By.XPATH,"./*"))>0
                                for region in regions_to_be_inspected
                                ))
    # Assert that all regions have cards
    for region in regions_to_be_inspected:
        region_holder=driver.find_elements(By.ID,region)
        assert len(region_holder)>0
        assert len(region_holder[0].find_elements(By.XPATH,"./*"))>0
    driver.quit()

def test_page_select_db_healthcheck_results():
    # Load Chrome webdriver
    driver= webdriver.Chrome(options)
    # Open Demo Dashboard Page
    driver.get("http://localhost:8000")
    # Get elements regions that they exists but they do not have childs
    regions_to_be_inspected=["databases-card-body","webservices-card-body","requirement-files-card-body","mount-points-card-body"]
    for region in regions_to_be_inspected:
        region_holder=driver.find_elements(By.ID,region)
        assert len(region_holder)>0
        assert len(region_holder[0].find_elements(By.XPATH,"./*"))==0
    # Select drop down list and set selection value to Databases
    drop_down_list=driver.find_element(By.ID,'select-healthcheck')
    select=Select(drop_down_list)
    select.select_by_index(2)
    # Get Display Button and click on it
    display_button=driver.find_element(By.ID,'display-healthcheck-btn')
    display_button.click()
    # Wait until data is fetched and cards displayed with maximum timeout of five seconds
    wait= WebDriverWait(driver,5)
    wait.until(lambda drv: len(drv.find_element(By.ID, 'databases-card-body').find_elements(By.XPATH,"./*"))>0)
    # Assert that regions other than databases have no cards
    for region in ["webservices-card-body","requirement-files-card-body","mount-points-card-body"]:
        len(driver.find_element(By.ID, region).find_elements(By.XPATH,"./*"))==0
    # Assert that database region has cards
    len(driver.find_element(By.ID, 'databases-card-body').find_elements(By.XPATH,"./*"))>0
    driver.quit()

def test_page_select_webservice_healthcheck_results():
    # Load Chrome webdriver
    driver= webdriver.Chrome(options)
    # Open Demo Dashboard Page
    driver.get("http://localhost:8000")
    # Get elements regions that they exists but they do not have childs
    regions_to_be_inspected=["databases-card-body","webservices-card-body","requirement-files-card-body","mount-points-card-body"]
    for region in regions_to_be_inspected:
        region_holder=driver.find_elements(By.ID,region)
        assert len(region_holder)>0
        assert len(region_holder[0].find_elements(By.XPATH,"./*"))==0
    # Select drop down list and set selection value to Webservices
    drop_down_list=driver.find_element(By.ID,'select-healthcheck')
    select=Select(drop_down_list)
    select.select_by_index(3)
    # Get Display Button and click on it
    display_button=driver.find_element(By.ID,'display-healthcheck-btn')
    display_button.click()
    # Wait until data is fetched and cards displayed with maximum timeout of five seconds
    wait= WebDriverWait(driver,5)
    wait.until(lambda drv: len(drv.find_element(By.ID, 'webservices-card-body').find_elements(By.XPATH,"./*"))>0)
    # Assert that regions other than webservices have no cards
    for region in ["databases-card-body","requirement-files-card-body","mount-points-card-body"]:
        len(driver.find_element(By.ID, region).find_elements(By.XPATH,"./*"))==0
    # Assert that webservices region has cards
    len(driver.find_element(By.ID, "webservices-card-body").find_elements(By.XPATH,"./*"))>0
    driver.quit()

def test_page_select_mountpoints_results():
    # Load Chrome webdriver
    driver= webdriver.Chrome(options)
    # Open Demo Dashboard Page
    driver.get("http://localhost:8000")
    # Get elements regions that they exists but they do not have childs
    regions_to_be_inspected=["databases-card-body","webservices-card-body","requirement-files-card-body","mount-points-card-body"]
    for region in regions_to_be_inspected:
        region_holder=driver.find_elements(By.ID,region)
        assert len(region_holder)>0
        assert len(region_holder[0].find_elements(By.XPATH,"./*"))==0
    # Select drop down list and set selection value to Mount Points
    drop_down_list=driver.find_element(By.ID,'select-healthcheck')
    select=Select(drop_down_list)
    select.select_by_index(4)
    # Get Display Button and click on it
    display_button=driver.find_element(By.ID,'display-healthcheck-btn')
    display_button.click()
    # Wait until data is fetched and cards displayed with maximum timeout of five seconds
    wait= WebDriverWait(driver,5)
    wait.until(lambda drv: len(drv.find_element(By.ID, "mount-points-card-body").find_elements(By.XPATH,"./*"))>0)
    # Assert that regions other than mount points have no cards
    for region in ["databases-card-body","requirement-files-card-body","webservices-card-body"]:
        len(driver.find_element(By.ID, region).find_elements(By.XPATH,"./*"))==0
    # Assert that mount points region has cards
    len(driver.find_element(By.ID, "mount-points-card-body").find_elements(By.XPATH,"./*"))>0
    driver.quit()

def test_page_select_requirements_results():
    # Load Chrome webdriver
    driver= webdriver.Chrome(options)
    # Open Demo Dashboard Page
    driver.get("http://localhost:8000")
    # Get elements regions that they exists but they do not have childs
    regions_to_be_inspected=["databases-card-body","webservices-card-body","requirement-files-card-body","mount-points-card-body"]
    for region in regions_to_be_inspected:
        region_holder=driver.find_elements(By.ID,region)
        assert len(region_holder)>0
        assert len(region_holder[0].find_elements(By.XPATH,"./*"))==0
    # Select drop down list and set selection value to Mount Points
    drop_down_list=driver.find_element(By.ID,'select-healthcheck')
    select=Select(drop_down_list)
    select.select_by_index(5)
    # Get Display Button and click on it
    display_button=driver.find_element(By.ID,'display-healthcheck-btn')
    display_button.click()
    # Wait until data is fetched and cards displayed with maximum timeout of five seconds
    wait= WebDriverWait(driver,5)
    wait.until(lambda drv: len(drv.find_element(By.ID, "requirement-files-card-body").find_elements(By.XPATH,"./*"))>0)
    # Assert that regions other than requirements have no cards
    for region in ["databases-card-body","webservices-card-body","mount-points-card-body"]:
        len(driver.find_element(By.ID, region).find_elements(By.XPATH,"./*"))==0
    # Assert that requirements region has cards
    len(driver.find_element(By.ID, "requirement-files-card-body").find_elements(By.XPATH,"./*"))>0
    driver.quit()

def test_clear_dashboard_button():
    # Load Chrome webdriver
    driver= webdriver.Chrome(options)
    # Open Demo Dashboard Page
    driver.get("http://localhost:8000")
    # Define regions to be inspected
    regions_to_be_inspected=["databases-card-body","webservices-card-body","requirement-files-card-body","mount-points-card-body"]
    # Select drop down list and set selection value to All Healthchecks
    drop_down_list=driver.find_element(By.ID,'select-healthcheck')
    select=Select(drop_down_list)
    select.select_by_index(1)
    # Get Display Button and click on it
    display_button=driver.find_element(By.ID,'display-healthcheck-btn')
    display_button.click()
    # Wait until data is fetched and cards displayed with maximum timeout of five seconds
    wait= WebDriverWait(driver,5)
    wait.until(lambda drv: any (len(drv.find_element(By.ID, region).find_elements(By.XPATH,"./*"))>0
                                for region in regions_to_be_inspected
                                ))
    # Assert that all regions have cards
    for region in regions_to_be_inspected:
        region_holder=driver.find_elements(By.ID,region)
        assert len(region_holder)>0
        assert len(region_holder[0].find_elements(By.XPATH,"./*"))>0
    # Get Reset Button and click on it
    reset_dashboard_button=driver.find_element(By.ID,'reset-selection-btn')
    reset_dashboard_button.click()
    # Wait until all main regions are cleared from cards
    wait.until(lambda drv: all (len(drv.find_element(By.ID, region).find_elements(By.XPATH,"./*"))==0
                                for region in regions_to_be_inspected
                                ))    
    # Get elements regions that they exists but they do not have childs
    for region in regions_to_be_inspected:
        region_holder=driver.find_elements(By.ID,region)
        assert len(region_holder)>0
        assert len(region_holder[0].find_elements(By.XPATH,"./*"))==0
    driver.quit()
