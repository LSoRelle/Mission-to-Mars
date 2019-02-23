#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests


# # For Mac Users 
# - trying to be helpful with grading, ;)

# In[2]:


# Choose the executable path to driver 
#executable_path = {'executable_path': 'chromedriver.exe'}
#browser = Browser('chrome', **executable_path, headless=False)


# # For Windows Users 
# - because I don't mac =D

# In[3]:


# Choose the executable path to driver 
# 'chromedriver.exe'
executable_path = {'executable_path': 'C:/Users/39319362/Desktop/SMDA201811DATA2/01-Lesson-Plans/12-Web-Scraping-and-Document-Databases/2/Activities/08-Stu_Splinter/Solved/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


scrape_info = {}


# # Time to Code! 

# In[5]:


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
    
# Store data in a dictionary

# Pull the Title and Content apart to make it easier to call in the html
news_title = latest_news.find("div",{"class":"content_title"}).text
news_content = latest_news.find("div",{"class":"article_teaser_body"}).text

# Print to verify everything is there
print (news_title)
print (news_content)

# Close the browser after scraping
#browser.quit()
scrape_info['news_title']=news_title
scrape_info['news_content']=news_content


# In[6]:


# JPL Mars Space Images - Featured Image
# * Visit the url for JPL Featured Space Image here.
# * Use splinter to navigate the site and find the image url for the current Featured Mars Image 
#   and assign the url string to a variable called featured_image_url.
# * Make sure to find the image url to the full size .jpg image.
# * Make sure to save a complete url string for this image.
    
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
 
# Print to verify everything is there
print (featured_img_url)
    
# Close the browser after scraping
#browser.quit()

scrape_info['featured_img_url']=featured_img_url


# In[7]:


# Mars Weather
# * Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
#   Save the tweet text for the weather report as a variable called mars_weather.
    
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
        print(weather_tweet)
        break
    else: 
        pass
    
# Close the browser after scraping
#browser.quit() 

scrape_info['weather_tweet']=weather_tweet


# In[8]:


# Mars Facts
# * Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the 
#   planet including Diameter, Mass, etc.
# * Use Pandas to convert the data to a HTML table string.

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

# Show the set to verify everything is there before turning into html 
Mars_facts_df

# Close the browser after scraping
#browser.quit()


# In[9]:


# Convert to html
mars_facts_html = Mars_facts_df.to_html(header=False, index=False)

# Remove \n from the code 
mars_facts_html = mars_facts_html.replace('\n', '')

# Print to verify everything is there
mars_facts_html

scrape_info['mars_facts_html']=mars_facts_html


# In[10]:


# Mars Hemispheres
# * Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
# * You will need to click each of the links to the hemispheres in order to find the image url to the 
#   full resolution image.
# * Save both the image url string for the full resolution hemisphere image, and the Hemisphere title 
#   containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url 
#   and title.
# * Append the dictionary with the image url string and the hemisphere title to a list. This list will 
#   contain one dictionary for each hemisphere.

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

# Print to verify everything is there
print (hemisphere_image_urls)

# Close the browser after scraping
browser.quit()

scrape_info['hemisphere_image_urls']=hemisphere_image_urls


# In[11]:


print(scrape_info)

