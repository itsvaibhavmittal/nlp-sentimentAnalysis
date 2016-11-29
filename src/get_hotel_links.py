from bs4 import BeautifulSoup
import requests
import scrape_links
import time

try:
    #get hotel links
    f = open("city_links.txt", 'r')
    links = f.readlines()
    f.close()

    #link = "http://www.tripadvisor.com/Hotels-g34439-Miami_Beach_Florida-Hotels.html"
    for city_link in links:
        page = requests.get(city_link)
        html = BeautifulSoup(page.text)
        hotel_count = html.find("div", {"class": "tab0"}).find("span", {"class": "tab_count"}).text
        hotel_count = hotel_count[1:-1]
        print("Hotels: " + hotel_count)
        hotels_in_one_page = len(html.findAll("div", {"class": "listing"}))
        print(hotels_in_one_page)
        counter = 30

        for page_count in range(0, int(int(hotel_count)/hotels_in_one_page) + 1):
            hotel_links = html.findAll("a", {"class": "property_title"})
            for link in hotel_links:
                print("www.tripadvisor.com" + link['href'])
                scrape_links.scrape_review_links("http://www.tripadvisor.com" + link['href'])

            city_link_parts = city_link.split('-', 2)
            city_link = city_link_parts[0] + '-' + city_link_parts[1] + '-' + 'oa' + str(counter) + '-' + city_link_parts[2]
            counter = counter + 30
            
            page_content = requests.get(city_link)
            html = BeautifulSoup(page_content.text)

except Exception as e:
    print(e)
