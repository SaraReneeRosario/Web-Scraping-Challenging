#scrape.py: one function to scrape all of mars

#dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import platform
import time
import requests
import warnings
warnings.filterwarnings('ignore')


# Create Mission to Mars global dictionary that can be imported into Mongo
mars_info = {}

def init_browser():
    # Get current system type Mac/Windows/Linux
    system = platform.system()
    
    # Load from Windows(Windows) or Mac(Darwin)/Linux(Posix)
    if system == "Windows":
        executable_path = {
            "executable_path": "C:\\Users\\charm\\Desktop\chromedriver"
        }
    else:
        executable_path = {
            "executable_path": "/usr/local/bin/chromedriver"
        }
    return Browser("chrome", **executable_path, headless=False)

def scrape_nasa():
    #initiate browser & set url
    browser = init_browser()
    url = "https://mars.nasa.gov/news/"
    
    #Visit and grab html with splinter; parse with Beautiful Soup
    browser.visit(url)
    
    # Need to wait for page load
    time.sleep(3)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    
    # Search through itemlist class
    news_title = soup.find('li', class_='slide').find('h3').text
    news_p = soup.find('div', class_='article_teaser_body').text
    browser.quit()

    mars_info["Latest Mars News Title"] = news_title
    mars_info["Latest Mars News article"] = news_p
    mars_info["Latest Mars News url"] = url
    # return mars_info

# FEATURED IMAGE
def scrape_mars_image():
    # Initialize browser & set url
    browser = init_browser()
    featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        
    #Visit and grab HTML object with splinter and Parse with Beautiful Soup
    browser.visit(featured_image_url)
    html_image = browser.html
    soup = bs(html_image, 'html.parser')
    browser.quit()

    # Website Base Url
    main_url = 'https://www.jpl.nasa.gov'
        
    # Retrieve background-image url from style tag
    image_url = soup.article['style'].replace("background-image: url('", main_url).replace("');", '')

    # Dictionary entry from FEATURED IMAGE
    mars_info['image_url'] = image_url
    
    # not needed because dictionary is defined outside of functions
    # return mars_info

# MARS WEATHER
'''def scrape_mars_weather():
    #technically only scraping from InSight rover
    # Initialize browser & set URL
    browser = init_browser()
    weather_url = 'https://twitter.com/marswxreport?lang=en'

    # Visit Mars Weather Twitter with splinter; save HTML object
    browser.visit(weather_url)
    time.sleep(5)
    html_weather = browser.html
    browser.quit()

    # Parse HTML with Beautiful Soup
    soup = bs(html_weather, 'html.parser')
    
    
    # Find all elements that contain tweets
    #tweets = soup.find_all('div', class_='js-tweet-text-container')
    #tweets = soup.find_all('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")
    tweets = soup.find_all("article").text
  

    for i, tweet in enumerate(tweets):
        if "InSight sol" in tweet.text:
            latest_mars_weather = tweets[i].text.replace('\n', ' ')
            break

    # Dictionary entry for WEATHER TWEET
    mars_info['mars_weather'] = latest_mars_weather
'''   

# MARS FACTS
def scrape_mars_facts():

    # Set URL & Use Pandas "read_html" to parse the URL
    url = 'http://space-facts.com/mars/'
    tables = pd.read_html(url)

    #Find Mars Facts DataFrame in the lists of DataFrames
    mars_facts = tables[0]
    mars_facts.columns = ['Description','Value']

    html_table = mars_facts.to_html(table_id='html_tbl_css', justify='left',index=False, classes ='table table-striped')

    # Dictionary entry from Mars Facts
    mars_facts_dictionary = {}
    for i, description in enumerate(mars_facts.Description):
        col1 = description.replace(":", "")
        mars_facts_dictionary[col1] = mars_facts.iloc[i, 1]

    html_table = html_table.replace("\n", "")
    mars_info['tablestring'] = html_table
    mars_info['tabledictionary'] = mars_facts_dictionary
    
# Mars Hemisphere
def scrape_mars_hemispheres():
    # Initialize browser & set URL + main URL
    browser = init_browser()
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    
    #splinter and get html object, parse with Beautiful Soup
    browser.visit(hemispheres_url)
    time.sleep(3)
    html_hemispheres = browser.html
    soup = bs(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

   
    
    
    hemisphere_image_urls_download = []

    for item in items:
        title = item.h3.text
        title = title.replace(" Enhanced", "")
        img_src = item.a["href"]
        img_location = hemispheres_main_url + img_src
        #visit page and get image
        browser.visit(img_location)
        img_html= browser.html
        img_soup = bs(img_html, "html.parser")
        img_url = img_soup.find_all('li')[1].a["href"]
        dictionary = {"title": title, "img_url": img_url}
        hemisphere_image_urls_download.append(dictionary)
    '''
    #loop through to get image urls, save to list as dictionaries
       hemisphere_specific_pages = []
       titles = []
    for item in items:
        title = item.find('h3').text
        title = title.replace(" Enhanced", "")
        img_src = item.a["href"]
        img_location = hemispheres_main_url + img_src
        hemisphere_specific_pages.append(img_location)
        titles.append(title)
    
    hemisphere_image_urls = []
    browser.quit()
    
    for i, url in enumerate(hemisphere_specific_pages):
        #visit page and get image and close browser
        browser = init_browser()
        browser.visit(url)
        time.sleep(10)
        img_html= browser.html
        img_soup = bs(img_html, "html.parser")
        browser.quit()
        print(soup.find_all('img', class_='wide-image'))
        # Retrieve full image source & append to list as dictionary
        img_partial = soup.find('img', class_='wide-image')['src']
        print(img_partial)
        img_url = hemispheres_main_url + img_partial
        
        hemisphere_image_urls.append({"title" : title[i], "img_url" : img_url})
    '''
    browser.quit()
    hemisphere_image_urls = hemisphere_image_urls_download
    mars_info['hemisphere_image_urls'] = hemisphere_image_urls
    
def scrape():
    scrape_nasa()
    #scrape_mars_weather()
    scrape_mars_facts()
    scrape_mars_hemispheres()
    #return mars_info #technically we shouldn't need to do this
    import pymongo 
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.scrape_db
    collection = db.items
    collection.insert_one(mars_info)
