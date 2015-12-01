import re
import logging

from bs4 import BeautifulSoup

logger = logging.getLogger('grabber')
PRICE_REGEX = '[0-9]*\.?[0-9]+'


def parse(html):
    return BeautifulSoup(html, 'html.parser')


def find_price(html):
    price_reg = re.compile(PRICE_REGEX)
    price_tag = html.find(class_='pricePerUnit').get_text()
    match = price_reg.search(price_tag)
    try:
        return float(match.group()) or 0
    except AttributeError:
        logger.exception('Could not find price in {price}'.format(price_tag))
        return 0


def find_description(html):
    return html.select_one('div.productText > p').get_text()


def find_title(html):
    return html.select_one('.productTitleDescriptionContainer > h1').get_text()


def all_links(parsed_html):
    for p in parsed_html.select('div.productInfo a'):
        yield p.get('href')
