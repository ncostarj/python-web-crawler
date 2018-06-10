import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time
from pymongo import MongoClient

class Robot():

    urls = []
    posts = []
    client = MongoClient('localhost', 27017)
    db = client.symfony_blog
    collection = db.posts

    def __init__(self, urls):
         self.urls = urls
   
    def extract_posts(self, html):

        div_posts = html.find_all('div', class_="post__excerpt")

        for post in div_posts:
            title = post.h2.a
            headline = post.h2.next_sibling.next_sibling
            date = headline.next_sibling.next_sibling.span
            strDate = date.get_text('', strip=True)
            fDate = datetime.strptime(strDate, '%B %d, %Y').strftime("%Y-%m-%dT%H:%M:%S.000Z+0000")
            author = date.next_sibling.next_sibling
            p = dict({'title': title.get_text('', strip=True),'headline': headline.get_text('', strip=True), 'date': fDate,'author': author.get_text('',strip=True)})
            self.collection.insert(p)
            self.posts.append(p)
    
    def crawl_url(self):
        for url in self.urls:
            response = requests.get(url, verify=False)
            html = BeautifulSoup(response.text, 'html.parser')
            self.extract_posts(html)
        # print(json.dumps(self.posts))
        # self.html =
    
    def crawl_html(self, html_doc):
        html = BeautifulSoup(html_doc, 'html.parser')
        self.extract_posts(html)