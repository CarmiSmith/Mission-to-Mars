# import dendencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import requests
import pymongo
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#executable_path = {'executable_path': ChromeDriverManager().install()}
#browser = Browser('chrome', **executable_path, headless=False)

# Initialize Browser
def init_Browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


# Create scraping function
def scrape():
    mars_dict = {}
    browser = init_Browser()

    # Nasa News
    # url to scrape
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    html = requests.get(url)

    # Create BeautifulSoup object; parse with ‘html.parser’
    soup = bs(html.text, 'html.parser')

    # Store first head line as news_title
    news_title = soup.find_all('div', class_='content_title')
    # print(news_title)

   # Scrape NASA website for News for paragraph and assign text to a variable
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_para = soup.find_all('div', class_="article_teaser_body")
    news_Title = news_title[0].text
    news_p = news_para[0].text
    # print(news_p)

    # New url
    jplurl = 'https://spaceimages-mars.com/'

    # Splinter url
    browser.visit(jplurl)
    time.sleep(1)

    # Retrieve page html
    html = browser.html

    # Create BeautifulSoup object; parse with ‘html.parser’
    soup = bs(html, 'html.parser')
    image_path = soup.find('a', class_="showimg fancybox-thumbs")['href']

    # featured_image = jplurl + image_path
    featured_imageURL = jplurl + image_path
    

    # featured_image
    # Mars Facts
    # Scrape table
    facts_url = 'https://space-facts.com/mars/'

    # Retrieve table
    tables = pd.read_html(facts_url)

    # Check that correct table is in dataframe
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Description', 'Value']

    # Use Pandas to convert the data to a HTML table string.
    mars_html_table = mars_facts_df.to_html(index=False)


    # Mars Hemispheres
    # Set up urls
    # import time
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    desc = soup.find_all('div', {'class': 'description'})
    hem_images = []
    usgs_url = 'https://astrogeology.usgs.gov'
    for div in desc:
        title = div.find('h3').text
        base_url = div.find('a')['href']
        image_url = usgs_url + base_url
        browser.visit(image_url)
        image_HTML = browser.html
        image_Soup = bs(image_HTML, 'html.parser')
        image_links = usgs_url + image_Soup.find('img', {'class': 'wide-image'})['src']
        hem_images.append({'title': title, 'img_url': image_links})
    # print(hem_images)

    # Create dictionary for all info scraped from sources above
    mars_dict = {
        'news_title': news_Title,
        'news_p': news_p,
        # ‘featured_image’: featured_image,
        'featured_image_url': featured_imageURL,
        'fact_table' : (mars_html_table),
        'hemisphere_images' : hem_images
        }
    return mars_dict