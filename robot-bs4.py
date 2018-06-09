from bs4 import BeautifulSoup

class Robot():

    html = ''

    def __init__(self, page):
        self.html = BeautifulSoup(page, 'html.parser')      
    def extract_head_title(self):
        return self.html.head.title.get_text().strip()


html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

robot = Robot(html_doc)
print(robot.extract_head_title())

