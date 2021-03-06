import argparse
from collections import namedtuple
import json
from pathlib import Path
import requests

from bs4 import BeautifulSoup
from googlesearch import search

def web_scraper(newspaper, num_results=100):
    """ returns links from a given newspaper """
    queries = {
        "german": "Klimawandel site:",
        "english": "Climate Change site:"
    }
    website, lang = newspaper
    query = queries[lang] + website
    links = [j for j in search(query, tld="co.in", num=num_results, start=1, stop=100)]
    return links


def save_html(article):
    newspaper = article[0]
    url = article[1]
    lang = article[2]
    response = requests.get(url)
    data_home = Path.home() / "climate-nlp" / "raw" /  newspaper.replace(".", "_")
    data_home.mkdir(parents=True, exist_ok=True)
    filename = url.split("/")[-1] + ".html"
    with open(data_home / filename, 'w') as fp:
        fp.write(response.text)

    json_text = {
        "url": url
    }
    json_filename = url.split("/")[-1] + ".json"
    with open(data_home / json_filename, 'w') as fp:
        json.dump(json_text, fp)

def import_newspapers():
    with open("listofwebsites.json", "r") as listofwebsites:
        newspapers = json.load(listofwebsites)

    newspapers = [Newspaper(tup["url"], tup["lang"]) for tup in newspapers]
    print(newspapers)
    return newspapers
def main(language, news):
    websites = []
    for new in news:
        if new.language == language:
            links = web_scraper(new)

            for link in links:
                websites.append((new.url, link, new.language))
                print(websites[-1])
                save_html(websites[-1])


Newspaper = namedtuple('Newspaper', ['url', 'language'])
if __name__ == '__main__':
    newspapers = import_newspapers()
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', default="english", nargs='?')

    args = parser.parse_args()
    newspapers = [
        # Newspaper('foxnews.com', 'english'),
        Newspaper('bbc.com', 'english'),
        Newspaper('theaustralian.com.au', 'english'),
        Newspaper('telegraph.co.uk', 'english'),
        Newspaper('news.sky.com/uk', 'english'),
        Newspaper('skynews.com.au', 'english')
    ]
    main(args.language, newspapers)
