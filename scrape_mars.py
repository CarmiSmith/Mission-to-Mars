# import dendencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import requests
import pymongo
from webdriver_manager.chrome import ChromeDriverManager

# Create browser function to call as needed with scraping
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

# Create scraping function
def scrape():
    mars_dict = {}
    browser = init_browser()

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
    print(featured_image_url)

    # Mars Facts
    # Scrape table 
    facts_url = "https://space-facts.com/mars/"

    # Retrieve table 
    tables = pd.read_html(facts_url)

    # Check that correct table is in dataframe
    mars_facts_df = tables[2]
    mars_facts_df.columns = ["Description", "Value"]

    # Use Pandas to convert the data to a HTML table string.
    mars_html_table = mars_facts_df.to_html(index=False, header=False)
    mars_html_table.replace('\n', '')
    print(mars_html_table)  

    # Mars Hemispheres

    # Set up urls 
    usgs_url = 'https://https://astrogeology.usgs.gov'
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars' 

    # Visit url in splinter
    browser.visit(hemispheres_url)

    # Retrieve html
    hemispheres_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    hemispheres_soup = bs(hemispheres_html, 'html.parser')

    # Mars hemispheres products data
    all_mars_hemispheres = hemispheres_soup.find('div', class_='collapsible results')
    mars_hemispheres = all_mars_hemispheres.find_all('div', class_='item')

    hemisphere_image_urls = []

    # Iterate through each hemisphere data
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find('div', class_="description")
        title = hemisphere.h3.text
    
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(usgs_url + hemisphere_link)
    
        image_html = browser.html
        image_soup = bs(image_html, 'html.parser')
    
        image_link = image_soup.find('div', class_='downloads')
        image_url = image_link.find('li').a['href']

        # Create Dictionary to store title and url info
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = image_url
    
        hemisphere_image_urls.append(image_dict)

    print(hemisphere_image_urls)



    # Create dictionary for all info scraped from sources above
    mars_dict = {
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url': featured_image_url,
        'fact_table' : str(mars_html_table),
        'hemisphere_images' : hemisphere_image_urls
        }
    


    return mars_dict