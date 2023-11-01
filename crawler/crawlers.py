from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import re


from enum import Enum


class CrawlerType(Enum):
    OVERALL_RATING = 0
    DEFENDING_MARKING_RATING = 1


def crawl_overall_rating(url):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()

        page_soup = soup(webpage, "html.parser")

        meta_description = page_soup.find("meta", attrs={"name": "description"})
        description = meta_description["content"]
        overall_rating = re.search(
            r"overall rating is (\d+)", description, re.IGNORECASE
        )
        if overall_rating:
            return int(overall_rating.group(1))
        else:
            print(f"No meta description found for {url}")
            return None
    except Exception as e:
        print("An error occurred:", e)


def crawl_defending_marking_rating(url):
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(req).read()

        page_soup = soup(webpage, "html.parser")

        marking_span = page_soup.find("span", text="Marking")

        if marking_span:
            number = marking_span.find_previous("span", class_="bp3-tag").text
            return int(number)
        else:
            print("Marking attribute not found.")
            return None
    except Exception as e:
        print("An error occurred:", e)
