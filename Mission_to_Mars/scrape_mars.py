#dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd


#initializing browser 
def init_browser(): 
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    
    #scraping data from the NASA Mars News Site
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text,'html.parser')
    
  
    title = soup.find('div', class_= "content_title").find('a').text.strip()
    paragraph_txt = soup.find('div', class_= "rollover_description_inner").text.strip()
     
    
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    
    #creating HTML object and parsing
    html_image = browser.html
    soup = bs(html_image, 'html.parser')
    
    featured_image_sub_url = soup.find('div',class_='carousel_items')('article')[0]['style'].\
        replace('background-image: url(','').replace(');','')[1:-1]
    
    main_url = 'https://www.jpl.nasa.gov'
    
    #create the full url 
    featured_image_url = main_url + featured_image_sub_url
    
    #using splinter to view the space facts for mars
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    #Reading the tables in the url using Pandas
    mars_tables = pd.read_html(mars_facts_url)
    
    #checking to see if there are multiple tables
    type(mars_tables)
    
    #locating table on the page contains our "Mars Facts"
    mars_facts_table = mars_tables[0]
    #formatting data frame
    mars_facts=mars_facts_table.rename(columns={0:'Fact',1:'Value'}).set_index('Fact').copy()
    
    #converting to html
    mars_facts_html = mars_facts.to_html()
    #visiting the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
    mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemisphere_url)
    #creating HTML object and parsing
    html_hemisphere_image = browser.html
    soup = bs(html_hemisphere_image, 'html.parser')
    
    # get all the info that contains the image links
    items = soup.find_all('div', class_='item')
    # List to collect all hemisphere urls 
    hemisphere_image_urls = []
    
    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'

    #for all the info containing the image links
    for i in items: 
        title = i.find('h3').text                                               # image title     
        sub_image_url = i.find('a', class_='itemLink product-item')['href']     # image url     
        browser.visit(hemispheres_main_url + sub_image_url)     # visiting the storage url     
        partial_image_html = browser.html                       # HTML Object for full image url storage website
        soup = bs( partial_image_html, 'html.parser')           # Parsing HTML for that specific website     
        image_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']  # creating full image url
        hemisphere_image_urls.append({"title" : title, "img_url" : image_url}) # Adding to dictionary
    
    mars_data = {
        "Mars_News_Title": title,
        "Mars_News_Paragraph": paragraph_txt,
        "Mars_Featured_Image": featured_image_url,
        "Mars_Facts": mars_facts_html,
        "Mars_Hemisphere_Images": hemisphere_image_urls
    }
    browser.quit()

    return mars_data