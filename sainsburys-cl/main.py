import logging
import re
import json

import click
import requests
from bs4 import BeautifulSoup


LOGGING_FORMAT = '%(asctime)s : %(levelname)s : %(message)s'

logger = logging.getLogger(__name__)


def _product_url(product_info):
    return product_info.find('a').get('href')


def _grabber(url):
    try:
        result = requests.get(url)
        logger.info('Fetching webpage: {url}'.format(url=url))

    except requests.exceptions.RequestException:
        logger.exception('Fetching webpage failed: {url}'.format(url=url))
        return None, None

    size = result.headers.get('content-length', len(result.content))
    # TODO: namedtuple
    return result.content, size


def _parser(html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs


def _find(html, *args, **kwargs):
    try:
        return html.find_all(**kwargs)
    except TypeError:
        return None


def _get_price(html):
    price_reg = re.compile('[0-9]*\.?[0-9]+')
    price_tag = html.find(class_='pricePerUnit').get_text()
    match = price_reg.search(price_tag)
    try:
        return float(match.group()) or 0
    except AttributeError:
        logger.exception('Could not find price in {price}'.format(price_tag))
        return 0


def _get_descr(html):
    return html.find('div', class_='productText').find('p').get_text()


def _get_title(html):
    return html.find(class_='productTitleDescriptionContainer').find('h1').get_text()


def product_details(product):
    html, size = _grabber(_product_url(product))
    parsed_html = _parser(html)
    return {'title': _get_title(parsed_html),
            'size': '{:.1f}kb'.format(int(size) / 1024),
            'unit_price': _get_price(parsed_html),
            'description': _get_descr(parsed_html)}


def calc_total(summary):
    return '{:.2f}'.format(sum([x.get('unit_price') for x in summary]))


@click.command()
@click.argument('url')
def grabber(url):
    html, size = _grabber(url)
    parsed_html = _parser(html)
    summary = []
    for product in _find(parsed_html, 'div', class_='productInfo'):
        summary.append(product_details(product))

    print json.dumps({'results': summary,
                      'total': calc_total(summary)})


if __name__ == '__main__':
    logging.basicConfig(format=LOGGING_FORMAT)
    grabber()
