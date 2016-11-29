#from lxml import html
import requests
#from lxml.cssselect import CSSSelector
#from lxml import etree
import os
import sys
import io
import time
from bs4 import BeautifulSoup

def scrape_review(links, path):
    os.chdir(path)
    try:
        count = 1
        for link in links:
            try:
                file = io.open((str(count) + ".txt"),'w', encoding="utf8")
            except Exception as e:
                print(e)
                continue

            #page = requests.get('http://www.tripadvisor.com/ShowUserReviews-g34438-d2253238-r345923208-Hampton_Inn_Suites_by_Hilton_Miami_Brickell_Downtown-Miami_Florida.html#CHECK_RATES_CONT')
            link = "http://www.tripadvisor.com" + link
            page = requests.get(link)
            #*** tree = html.fromstring(page.content)
            html = BeautifulSoup(page.text)

            #print(html)
            review = html.find("div", {"class": "inlineReviewUpdate"})
            #print(review)
            #*** review = reviews[0]
            date = review.find("span", {"class":"ratingDate"})
            if date.has_attr('title'):
                date = date['title']
            elif date.has_attr('content'):
                date = date['content']
            else:
                date = date.text.replace('Reviewed', '').strip()

            #print("Date:", date)
            file.write("Date:" + date+"\n")

            rating = review.find("span", {"class": "rating_s"}).find("img")['alt']
            #rate_img= rating[0].xpath('//img/@alt')
            #print("Rating:", rating)
            file.write("Rating:" + rating +"\n")

            quote = review.find("div", {"class": "quote"}).text
            quote = quote[1:-1]
            #print("quote:", quote)
            file.write("Heading:" + quote.strip() + "\n")
            cont = review.find("p", {"property": "reviewBody"}).text
            #print("content:", cont)
            file.write("Content:" + cont.strip() + "\n")
            '''
            room_tip = review.xpath('//div[@class="reviewItem inlineRoomTip"]/text()')
            print("room_tip:", room_tip)
            '''
            meta = review.find("span", {"class": "recommend-titleInline"}).text
            #print("Meta Info:", meta)
            file.write("Meta Info:" + meta.strip() + "\n")

            other_info = review.find("ul", {"class": "recommend"})
            if other_info is not None:
                #*** other_info = other_info[0]
                other_info_list = other_info.findAll("li",{"class":"recommend-answer"})
                for item in other_info_list:
                    item_type = item.find("div", {"class": "recommend-description"}).text
                    item_val = item.find("img")['alt']
                    #print(item_type, ":", item_val)
                    file.write(item_type+ ":" + item_val + "\n")

            count = count + 1
            file.close()
            time.sleep(1)
        os.chdir("..")
    except Exception as e:
        print(e)
        file.close()
        os.chdir("..")
        return
#scrape_review("/ShowUserReviews-g34439-d85177-r338726728-Fontainebleau_Miami_Beach-Miami_Beach_Florida.html#CHECK_RATES_CONT", "/Users/Rahul/Documents/coursework/Information Retrieval/IR-Project Code")
