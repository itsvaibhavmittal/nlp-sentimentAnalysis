#from lxml import html
#from lxml.cssselect import CSSSelector
import requests
#from lxml import etree
import time
import os
import sys
import scrape
import io
from bs4 import BeautifulSoup

def scrape_review_links(base_url):
    try:
        dir_made = False
        page = requests.get(base_url)
        html = BeautifulSoup(page.text)

        hotel = html.find("div",{"id":"HEADING_GROUP"}) #List of element containing the hotel info
        hotel_name = hotel.find("h1",{"id":"HEADING"}).text.strip()
        print ("Hotel Name:", hotel_name)
     

        rating = hotel.find("span",{"class":"sprite-rating_rr"}).find("img")['alt']
        #rate_img= rating[0].xpath('//img/@alt')
        print("Rating:", rating)
        

        num_reviews =  hotel.find("a",{"property":"reviewCount"})['content']
        #print("Reviews:", num_reviews)
        
        num_reviews =  int(num_reviews)
        
        if num_reviews<250:
            return
        dir_name =  os.getcwd() +"/"+hotel_name.replace('/','-')
        try:
            os.makedirs(dir_name)
            os.chdir(dir_name)
            dir_made = True
            file = io.open("hotel_info.txt",'w', encoding="utf8")
     
        except Exception as e:
            print("Directory could not be formed:",e)
            return

        file.write("Hotel Name:" + hotel_name+"\n")
        file.write("Rating:"+rating+"\n")
        file.write("Total Reviews:" + str(num_reviews)+"\n")
     

        rank =  hotel.find("div",{"class":"rank_text"}).find("b",{"class":"rank"}).text
        print("Rank:", rank.replace('#','').strip())
        file.write("Rank:"+ rank.replace('#','').strip()+"\n")

        a_text =  hotel.find("div",{"class":"rank_text"}).find("a").text
        
        total_hotels  = hotel.find("div",{"class":"rank_text"}).text.replace(rank,'').replace(a_text,'').replace('of', '').strip()
        print("Total Hotels in group:", total_hotels)
        file.write("Total Hotels in group:" + total_hotels+"\n")
    

        address_info = hotel.find("div",{"class":"header_contact_info"}).find("address").find("div",{"property":"address"})
        address_info =  address_info  # get the first address_info element

        address = ""
        street_address = address_info.find("span",{"class":"street-address"}).text
        address += street_address + ','

        locality = address_info.find("span",{"class":"locality"}).find("span",{"property":"addressLocality"}).text
        address += locality + ','

        state = address_info.find("span",{"class":"locality"}).find("span",{"property":"addressRegion"}).text
        address += state + ' '

        code = address_info.find("span",{"class":"locality"}).find("span",{"property":"postalCode"}).text
        address += code + ','

        country = address_info.find("span",{"class":"country-name"})['content']
        address += country

        print("Address:", address)
        file.write("Address:"+ address)

        file.close()

        #Get links of various Reviews
        #base_url = 'http://www.tripadvisor.com/Hotel_Review-g34438-d2253238-Reviews-Hampton_Inn_Suites_by_Hilton_Miami_Brickell_Downtown-Miami_Florida.html#REVIEWS'
        #page = requests.get(base_url)
        #tree = html.fromstring(page.content)


        review_pages = int(num_reviews/10)
        all_reviews =[]
        i = 0;
        while (len(all_reviews)<200) and (i<review_pages):
            
            review_section = html.find("div",{"id":"REVIEWS"}) #List of element containing the hotel info

            reviews = review_section.findAll("div",{"class":"reviewSelector"})

            #rest_reviews = review_section.xpath('//div[@class="reviewSelector  "]')

            #reviews = first_review + rest_reviews
            #print("Reviews:",reviews)

            #Get all the review links inside this class
            #review_link = reviews[0].xpath('//div[@class="col2of2"]/div[@class="innerBubble"]//a/@href')
            for review in reviews:
                review_link = review.find("div",{"class":"col2of2"})
                if review_link is not None:
                    review_link =  review_link.find("div",{"class":"innerBubble"})
                    if review_link is not None:
                        review_link = review_link.find("a")
                        all_reviews.append(review_link['href'])
            #print("Review Links:", all_reviews)
            print("Review Links Length:", len(all_reviews))

            time.sleep(2)
            if i< (review_pages-1):
                #Form the link for next page
                base_tokens = base_url.partition('-Reviews-')
                new_url = base_tokens[0]+base_tokens[1]+'or'+str(i+1)+'0-'+base_tokens[2]
                print("New Url:",new_url)
                page = requests.get(new_url)
                html = BeautifulSoup(page.text)
            i = i+1
        
        scrape.scrape_review(all_reviews,dir_name)
    except Exception as e:
        print("Exception Caught:",e)
        if dir_made:
            os.chdir("..")
        return

#scrape_review_links('http://www.tripadvisor.com/Hotel_Review-g34439-d85096-Reviews-Courtyard_Miami_Beach_Oceanfront-Miami_Beach_Florida.html')




