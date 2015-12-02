import logging
import json
from collections import namedtuple

import click
import requests

from parsing import parse, find_title, find_price, find_description, all_links


logger = logging.getLogger('grabber')
LOGGING_FORMAT = '%(asctime)s : %(levelname)s : %(message)s'


def get_html(url):
    """Retrieve webpage content using provided URL.

    :param url: webpage address
    :type url: str
    :returns: Tuple with HTML content and size of the content
    :rtype: namedtuple(content, size)

    """
    try:
        result = requests.get(url)
        logger.info('Fetching webpage: {url}'.format(url=url))

    except requests.exceptions.RequestException:
        logger.exception('Fetching webpage failed: {url}'.format(url=url))
        return None, None

    size = result.headers.get('content-length', len(result.content))
    Result = namedtuple('Result', ['content', 'size'])
    return Result(content=parse(result.content),
                  size='{:.1f}kb'.format(int(size) / 1024))


def product_details(url):
    """Fetch and parse product details page

    Product page is parsed for specific information and returned
    in form of dict.

    Example returned value:
    {'title': 'The gizmo',
     'size': 1023,
     'unit_price': 0.99,
     'description': 'Cheap and good'}

    :param url: webpage address
    :type url: str
    :returns: product details
    :rtype: dict

    """
    html, size = get_html(url)
    if not html:
        logger.error('Fetched content was empty. {url}'.format(url=url))
        return {}

    return {'title': find_title(html),
            'size': size,
            'unit_price': find_price(html),
            'description': find_description(html)}


def calc_total(product_details):
    """ Calculate total price of all products

    :param product_details: product details as dictionary,
                            for structure see product_details()
    :type product_details: dict
    :returns: sum of all unit_price values
    :rtype: str

    """
    return '{:.2f}'.format(sum([x.get('unit_price', 0) for x
                                in product_details]))


@click.command()
@click.argument('url')
def scl(url):
    """Fetch provided URL and parse webpage for products.
    Tool provides summary of parsed products and total price of all
    found products.

    Usage example:

    scl http://page.com/products.html

    """
    html, _ = get_html(url)
    summary = [product_details(link) for link in all_links(html)]

    print json.dumps({'results': summary,
                      'total': calc_total(summary)})


if __name__ == '__main__':
    logging.basicConfig(format=LOGGING_FORMAT)
    scl()
