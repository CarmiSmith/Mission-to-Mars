# import dendencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager
browser = Browser()

# Create browser function to call as needed with scraping
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

# Create scraping function
def scrape():
    mars_dict = {}

    # Nasa News
    # url to scrape
    url = 'https://mars.nasa.gov/news/'
    
    # Retrieve page with the requests module
    html = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html.text, 'html.parser')

    # Store first head line as news_title
    news_title = soup.find('div', class_='content_title').text.strip()
    print(news_title)

   # Scrape NASA website for News for paragraph and assign text to a variable                  
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_p = soup.find('div', class_="article_teaser_body").text.strip()
    print(news_p)
     
    # New url 
    jlp_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    # Splinter url 
    browser.visit(jlp_url)

    # Retrieve page html
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')
    image_path = soup.find('a', class_="showimg")['href']
    featured_image_url = jlp_url + image_path
  

    # Mars Facts
    # Scrape table 
    facts_url = "https://space-facts.com/mars/"

    # Retrieve table 
    tables = pd.read_html(facts_url)

    # Check that correct table is in dataframe
    mars_facts_df = tables[2]

    # Use Pandas to convert the data to a HTML table string.
    mars_html_table = mars_facts_df.to_html(index=False, header=False)  

    # Mars Hemispheres

    # Set up urls 
    usgs_url = 'https://astrogeology.usgs.gov'
    hemisphere_url = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 

    # Visit url in splinter
    browser.visit(usgs_url + hemisphere_url)

    # Retrieve html
    hemisphere_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(hemisphere_html, 'html.parser')

    # Name is in div class='item' in h3 element
    names = soup.find_all('div', class_='item') 

    # Loop to get and store names in a list
    titles=[]

    for name in names:
        titles.append(name.find('h3').text.strip())
    
    # Loop to get and store hemisphere urls to get image sub url
    # Base url
    title_url = []

    for name in names:
        title_url.append(usgs_url + (name.find('a')['href']))



    # Retrieve html
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html, 'html.parser')

    # Loop to pull all full size image urls
    hemp_image_url = []

    for hemp_url in title_url:

        # Open browser for each url
        browser.visit(hemp_url)

        # Create BeautifulSoup object; parse with 'html.parser'
        soup = bs(html, 'html.parser')

        # Create new url for list
        image_url = usgs_url + soup.find('img', class_='wide-image')['src']

        # Add url to list for dict 
        hemp_image_url.append(image_url)

    browser.quit() 

    # Create a list of dict called 'hemisphere_image_url'  
    # Blank list
    hemisphere_image_url =[]

    # Loop to combine list into dictonary and then add to blank list
    for x in range(len(hemp_image_url)):

        # For x combine the key value pair with comprehension and add the hemp_image_url list
        hemisphere_image_url.append({'title':titles[x], 'hemp_image_url': hemp_image_url[x]})
    print(hemisphere_image_url)

    # Create dictionary for all info scraped from sources above
    mars_dict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'fact_table' : str(mars_html_table),
        'hemisphere_images' : hemisphere_image_url
        }
    


    return mars_dict