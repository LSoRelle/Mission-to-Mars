#!/usr/bin/env python
# coding: utf-8

# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests


def init_browser():
    # # For Mac Users 
    # - trying to be helpful with grading, ;)

    # Choose the executable path to driver 
    #executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)

    # # For Windows Users 
    # - because I don't mac =D

    # Choose the executable path to driver 
    # 'chromedriver.exe'
    executable_path = {'executable_path': 'C:/Users/39319362/Desktop/SMDA201811DATA2/01-Lesson-Plans/12-Web-Scraping-and-Document-Databases/2/Activities/08-Stu_Splinter/Solved/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


scrape_info = (['scrape_info_news',  
    'scrape_info_feature', 
    'scrape_info_weather', 
    'scrape_info_facts', 
    'scrape_info_hemi'])

def scrape_info_news():
    browser = init_browser()

    # Create a dictonary for results of scrape
    mars_scrape = {}
    # NASA Mars News
    # * Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    #   Assign the text to variables that you can reference later.
   
    # Set url for use in scrape
    NASA_Mars_url = "https://mars.nasa.gov/news/"
    browser.visit(NASA_Mars_url)
    
    # Scrape page into Soup
    soup = bs(browser.html,"html.parser")
    
    # Get title and text for latest news based on html tags 
    latest_news = soup.find_all("div",{"class":"list_text"})[0]

    # Pull the Title and Content apart to make it easier to call in the html
    news_title = latest_news.find("div",{"class":"content_title"}).text
    news_content = latest_news.find("div",{"class":"article_teaser_body"}).text
    
    return ('news_title', 'news_content')

scrape_info_news()


def scrape_info_feature():
    browser = init_browser()

    # Set base url for call back later
    base_url = 'https://www.jpl.nasa.gov'
    
    # Set url for use in scrape
    JPL_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPL_url)
    
    # Scrape page into Soup
    soup = bs(browser.html,"html.parser")
    
    # Get Featured image based on html tags 
    featured_img = soup.find("div", class_="carousel_items").find("article")
    
    # Create url for featured image
    featured_img_url = base_url+featured_img['style'].split(':')[1].split('\'')[1]
    
    return ('featured_img_url')

scrape_info_feature()

def scrape_info_weather():
    browser = init_browser()

    # Set url for use in scrape
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    
    # Scrape page into Soup
    soup = bs(browser.html,"html.parser")
    
    # Find all elements that contain tweets based on html tags 
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
    
    # When I was looking for weather tweets, the first tweet was a retweet not about what I needed
    # for this project. Spent a lot of time trying to find a way to distinguish retweets and tweets
    # with weather data, there was not a difference in the html code, so had to write a for loop to
    # look for the data I did want in the body of a tweet. 
    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'high' in weather_tweet:
            break
        else: 
            pass

    return ('weather_tweet')

scrape_info_weather()

def scrape_info_facts():
    browser = init_browser()

 # Set url for use in scrape
    Mars_facts_url = "https://space-facts.com/mars/"

    #Read the html
    Mars_facts = pd.read_html(Mars_facts_url)

    # Pull facts in as a Dataframe
    Mars_facts_df = Mars_facts[0]

    # Assign columns to the Dataframe
    Mars_facts_df.columns = ["Description","Value"]

    # Get rid of the id column
    Mars_facts_df = Mars_facts_df.iloc[1:]
    Mars_facts_df.set_index("Description", inplace=True)

    # Convert to html
    mars_facts_html = Mars_facts_df.to_html(header=False, index=False)

    # Remove \n from the code 
    mars_facts_html = mars_facts_html.replace('\n', '')

    return ('mars_facts_html')

scrape_info_facts()

def scrape_info_hemi():
    browser = init_browser()

    # Set base url for call back later
    base_hemisphere_url = "https://astrogeology.usgs.gov"

    # Set url for use in scrape
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    # Scrape page into Soup
    soup = bs(browser.html,"html.parser")

    # Create list for hemisphere url and title
    hemisphere_image_urls = []

    # Find images based on html tags 
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    # for loop to pull each hemisphere into the list
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = base_hemisphere_url + end_link    
        browser.visit(image_link)
        soup = bs(browser.html,"html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    return ('hemisphere_image_urls')

scrape_info_hemi()

