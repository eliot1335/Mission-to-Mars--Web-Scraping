# Import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def init_browser():
    # Setup splinter
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    mars_data = {}

    url = "https://mars.nasa.gov/news/"

    browser.visit(url)
    html = browser.html

    soup = bs(html, "html.parser")

    titles = soup.find_all("div", class_="content_title")
    # news_titles

    # A blank list to hold titles
    news_titles = []
    # Loop over results
    for news_title in titles:
        # Check if it has an anchor...
        if (news_title.a):
            # Check if it has non-blank text...
            if (news_title.a.text):
                # Strip it for text and push to list
                news_titles.append(news_title.a.text.strip())

    mars_data["news_title"] = news_titles[0]
# --------------------------------------------------------------------
    time.sleep(1)

    paragraphs = soup.find_all("div", class_="article_teaser_body")

    # A blank list to hold teaser paragraphs
    news_paragraphs = []

    for news_paragraph in paragraphs:
        # Check if it has non-blank text...
        if (news_paragraph.text):
            # Strip it for text and push to list
            news_paragraphs.append(news_paragraph.text.strip())

    mars_data["news_paragraph"] = news_paragraphs[0]
# ---------------------------------------------------------------------
    time.sleep(1)
    # Find the image url for the current Featured Mars Image and assign the url to featured_image_url
    # The url to scrape,  JPL Featured Space Image
    given_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(given_url)

    # Get splinter to click on the link of the latest featured image
    browser.click_link_by_partial_href("/images/daedalia-planum-70/")
    html = browser.html
    soup = bs(html, "html.parser")

    images = soup.find_all("img")
    for i in range(len(images)):
        featured_image_url = browser.find_by_css("img[class='BaseImage object-scale-down']")["src"]
    
    mars_data["featured_image_url"] = featured_image_url


    # images = soup.find_all("img", class_="BaseImage object-scale-down")
    # for image in images:
    #     mars_data["featured_image_url"] = image["src"]

    # mars_data["feature_image_url"] = featured_image_url
# ---------------------------------------------------------------------
    time.sleep(1)
    # Scrape Mars Facts page to convert a HTML table using pandas
    facts_url = "https://space-facts.com/mars/"

    mars_facts = pd.read_html(facts_url)

    mars_df = mars_facts[0]
    mars_df.columns = ["Description", "Value"]
    mars_df.set_index("Description", inplace=True)


    mars_df_html = mars_df.to_html()

    mars_data["mars_facts_table"] = mars_df_html
# ---------------------------------------------------------------------
    time.sleep(1)
    # Scrape the USGS Astrogeology site for high res pics of Mar's hemispheres
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)

    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere_image_urls = []
    hemi_list = soup.find_all("div", class_="item")

    for x in range(len(hemi_list)):
        hemi_dict = {}
        hemi_dict["title"] = browser.find_by_css("h3")[x].text
        browser.links.find_by_partial_text("Hemisphere")[x].click()
        hemi_dict["img_url"] = browser.find_by_css("img[class='wide-image']")["src"]
        hemisphere_image_urls.append(hemi_dict)
        browser.back()

    mars_data["hemisphere_image_urls"] = hemisphere_image_urls




    browser.quit()

    return mars_data

# Call the scrape function if main
if __name__ == "__main__":
    scrape()

    
