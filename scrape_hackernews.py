import requests
from bs4 import BeautifulSoup

URL = "http://news.ycombinator.com"


class Article:
    def __init__(self, title, url, votes):
        self.title = title
        self.url = url
        self.votes = votes

    def __str__(self):
        return f"{self.title}\n{self.url}\n{self.votes} votes"


res = requests.get(URL)
soup = BeautifulSoup(res.text, 'lxml')

articles = soup(class_="athing")

top = []

for item in articles:
    votes = item.next_sibling.find(class_="score")
    if votes:
        votes = int(votes.text.split()[0])

        if votes >= 100:
            current_article = item.find(class_="storylink")
            title = current_article.text
            url = current_article.get('href')
            top.append(Article(title, url, votes))

for item in sorted(top, key=lambda k: k.votes, reverse=True):
    print(item, end='\n\n')
