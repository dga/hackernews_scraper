#!/usr/bin/env python3

from __future__ import print_function
import argparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class Article:
    """
    This is a class to create article objects.

    Attributes:
        title (str): The article's title
        url (str): The link to the article
        votes (int): The number of votes the article has
    """

    def __init__(self, title, url, votes):
        self.title = title
        self.url = url
        self.votes = votes

    def __str__(self):
        return f"\n  Title: {self.title}\n  URL: {self.url}\n  [{self.votes}" \
            " votes]"


def get_top_articles(url, threshold):
    """
    Parse articles from page and return only those articles with votes 
    greater than or equal to threshold
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    articles = soup(class_="athing")
    top_articles = []

    # get the article's votes relative to where it is located in html
    # (article title and url is nested within .athing while votes are nested
    # within .athing's sibling, .subtext)
    if articles:
        for item in articles:
            votes = item.next_sibling.find(class_="score")
            if votes:
                votes = int(votes.text.split()[0])
                if votes >= threshold:
                    current_article = item.find(class_="storylink")
                    title = current_article.text
                    url = current_article.get('href')
                    top_articles.append(Article(title, url, votes))
    return top_articles


def print_articles_sorted(top_articles):
    """Print articles in descending order by votes"""
    for i, item in enumerate(sorted(top_articles, key=lambda k: k.votes,
                                    reverse=True)):
        print(f"{i + 1}. {item}\n")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Scrape top articles from Hacker News with at least n"
        " votes")
    parser.add_argument(
        "threshold", help="The minimum number of votes that posts should"
        " have", type=int)
    args = parser.parse_args()
    aggregate_articles = []

    print("Scraping...\n")

    for i in tqdm(range(1, 16)):
        url = f"https://news.ycombinator.com/news?p={i}"
        aggregate_articles += get_top_articles(url, args.threshold)

    print("\nDone.\n")
    print_articles_sorted(aggregate_articles)
