import re
import logging

from bs4 import BeautifulSoup

logger = logging.getLogger('grabber')
PRICE_REGEX = '[0-9]*\.?[0-9]+'
HTML_PARSER = 'html.parser'


def parse(html):
    """Helper method for parsing HTML from string
    into BeautifulSoup object

    :param html: HTML in form of string
    :type html: str
    :returns: parsed HTML
    :rtype: bs4.BeautifulSoup

    """
    return BeautifulSoup(html, HTML_PARSER)


def _find_item(html, selector):
    """Helper method for searching html with CSS selector

    :param html: HTML with seeked data
    :type html: bs4.BeautifulSoup
    :param selector: CSS selector
    :type selector: str
    :returns: searched text
    :rtype: str

    """
    return html.select_one(selector).get_text()


def find_price(html):
    """Find price within HTML

    :param html: HTML with seeked data
    :type html: bs4.BeautifulSoup
    :returns: searched text
    :rtype: str

    """
    price_reg = re.compile(PRICE_REGEX)
    price_tag = html.find(class_='pricePerUnit').get_text()
    match = price_reg.search(price_tag)
    try:
        return float(match.group()) or 0
    except AttributeError:
        logger.exception(
            'Could not find price in {price_tag}'.format(price_tag=price_tag))
        return 0


def find_description(html):
    """Find description within HTML

    :param html: HTML with seeked data
    :type html: bs4.BeautifulSoup
    :returns: searched text
    :rtype: str

    """
    return _find_item(html, 'div.productText > p')


def find_title(html):
    """Find title within HTML

    :param html: HTML with seeked data
    :type html: bs4.BeautifulSoup
    :returns: searched text
    :rtype: str

    """
    return _find_item(html, '.productTitleDescriptionContainer > h1')


def all_links(html):
    """Generator function returning links

    :param html: HTML with links
    :type html: bs4.BeautifulSoup
    :returns: URL to a webpage
    :rtype: str
    :raises: StopIteration

    """
    try:
        for product in html.select('div.productInfo a'):
            yield product.get('href')
    except AttributeError:
        logger.exception('Unable to find links.')
        raise StopIteration
