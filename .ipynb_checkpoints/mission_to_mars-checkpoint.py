from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mission={}
    url_news='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url_news)
    soup = BeautifulSoup(browser.html, 'html.parser')
    mission['news_title'] = soup.find_all('div', class_='content_title')[0].get_text()
    mission['news_p'] = soup.find_all('div', class_='article_teaser_body')[0].get_text()

    url_pic = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_pic)
    soup = BeautifulSoup(browser.html, 'html.parser')
    url = soup.find_all('article')[0]['style'][24:-3]
    base_url = base_url = url_pic[0:-34]
    mission['featured_image_url'] = f'{base_url}{url}'

    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)
    soup = BeautifulSoup(browser.html, 'html.parser')
    mission['tweet'] = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text[0:-26]
    
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    soup = BeautifulSoup(browser.html, 'html.parser')
    results = soup.find_all('tr')
    keys = []
    values = []
    for result in results: 
        key = result.find('td', {'class':'column-1'}).text
        keys.append(key)
        value = result.find('td', {'class':'column-2'}).text
        values.append(value)
    df = pd.DataFrame({'Category': keys,'Facts': values})
    mission['html_df'] = df.to_html(index=False)

    x=0
    mission['hemisphere_image_urls']= []
    image_urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced', 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']
    for url in image_urls: 
        dict_hemi = {}
        url=image_urls[x]
        browser.visit(url)
        soup = BeautifulSoup(browser.html, 'html.parser')
        img_url = soup.find_all('a', target='_blank')[0]['href']
        img_title = soup.find('h2', class_='title').text
        dict_hemi = {'title': img_title, 'img_url': img_url}
        mission['hemisphere_image_urls'].append(dict_hemi)
        x = x+1
    browser.quit()
    return mission