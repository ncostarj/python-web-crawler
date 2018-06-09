import scrapy
from pymongo import MongoClient

class Post(scrapy.Item):
    title  = scrapy.Field()
    text   = scrapy.Field()
    date   = scrapy.Field()
    author = scrapy.Field()

class BlogSymphonyPosts(scrapy.Spider):
    """A Blog Reader"""
    name = 'Reader'
    start_urls = ['https://symfony.com/blog/']
    client = MongoClient('localhost', 27017)
    db = client.symphony
    posts = db.posts

    def parse(self, response):

        nextPage = response.css('ul.pager > li:nth-child(2)')

        for div in response.css('div.post__excerpt'):

            post = self.extrai_post(div)
            self.posts.insert(dict(post))
            self.log('Post id: %s' % post)
            yield post
        
        if (nextPage.css('a')):
            path = nextPage.css('a').xpath('@href')[0].extract()
            segments = path.split('/')
            url = self.parse_url(segments[2])
            # self.log('próxima pagina: %s' % url)
            yield scrapy.Request(url,self.parse)
        else:
            self.log('ultima página')

    def parse_url(self, url):
        return self.start_urls[0] + url

    def extrai_post(self, div):
        p = Post()

        p['title']  = ''.join(div.css('h2.m-b-5 > a::text').extract()).strip()
        p['text']   = ''.join(div.css('p.m-b-5::text').extract()).strip()
        p['date']   = ''.join(div.css('p.metadata > span:nth-child(1)::text').extract()).strip()

        a = div.css('p.metadata > span:nth-child(2)')

        if (a.css('a')):
            author = a.css('a:nth-child(2)::text').extract()
        else:
            author = div.css('p.metadata > span:nth-child(2)::text').extract()

        # self.log('author %s' % author)

        p['author'] = ''.join(author).strip()        

        return p