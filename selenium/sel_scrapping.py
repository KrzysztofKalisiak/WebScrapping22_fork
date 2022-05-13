from multiprocessing.sharedctypes import Value
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import getpass
import datetime
import pandas as pd
import sqlite3

gecko_path = 'geckodriver'
ser = Service(gecko_path)
options = webdriver.firefox.options.Options()
options.headless = False
driver = webdriver.Firefox(options = options, service=ser)

# Url used
url = 'https://www.plusliga.pl/statsTeams/tournament_1/all.html'
driver.get(url)

# Database in which scraped data is stored
conn = sqlite3.connect('database.db')

# If True, scraper stops after visiting 100 pages
limit = True

# Do not change this value
breaker = False

# Set up the counter
i = 0

# Cookies
button = driver.find_element(By.XPATH, '//button[@class="btn btn-default cookie-manager-button button-allow-all"]')
button.click()

# Which team
buttons_teams = driver.find_elements(By.XPATH, '//img[@class="img-responsive isphoto"]')
for team in range(len(buttons_teams)):
    if breaker:
        break

    button2 = driver.find_elements(By.XPATH, '//img[@class="img-responsive isphoto"]')
    team_name = button2[team].get_attribute('alt')
    button2[team].click()

    # Which season
    button3 = driver.find_elements(By.XPATH, '//button[@class="btn btn-default dropdown-toggle form-control"]')
    button3[1].click()
    buttons = driver.find_elements(By.XPATH, '//a[contains(string(), "Sezon")]')

    for season in range(len(buttons)):
        if limit and i >= 100:
            breaker = True
            break

        button4 = driver.find_elements(By.XPATH, '//a[contains(string(), "Sezon")]')
        season_nr = button4[season].text
        button4[season].click()

        # Extract the table with data
        table = pd.read_html(driver.find_element(By.XPATH, '/html/body/div[3]/div[8]/div[2]/div/div/div').get_attribute('innerHTML'))[0]

        # Save data to sql database
        table['Season'] = season_nr
        table.to_sql(team_name, conn, if_exists='append', index=False)
        button3 = driver.find_elements(By.XPATH, '//button[@class="btn btn-default dropdown-toggle form-control"]')
        button3[1].click()

        # Increase the counter
        i += 1
    # After looping over all available seasons, scraper goes back to the main page to select the next team
    driver.get(url)
