import logging
import json

import click
import requests

from parsing import parse, find_title, find_price, find_description, all_links


LOGGING_FORMAT = '%(asctime)s : %(levelname)s : %(message)s'

logger = logging.getLogger('grabber')


def get_html(url):
    try:
        result = requests.get(url)
        logger.info('Fetching webpage: {url}'.format(url=url))

    except requests.exceptions.RequestException:
        logger.exception('Fetching webpage failed: {url}'.format(url=url))
        return None, None

    size = result.headers.get('content-length', len(result.content))
    # TODO: namedtuple
    return parse(result.content), '{:.1f}kb'.format(int(size) / 1024)


def product_details(product):
    html, size = get_html(product)
    if not html:
        return {}

    return {'title': find_title(html),
            'size': size,
            'unit_price': find_price(html),
            'description': find_description(html)}


def calc_total(summary):
    return '{:.2f}'.format(sum([x.get('unit_price', 0) for x in summary]))


@click.command()
@click.argument('url')
def grabber(url):
    html, _ = get_html(url)
    summary = [product_details(link) for link in all_links(html)]

    print json.dumps({'results': summary,
                      'total': calc_total(summary)})


if __name__ == '__main__':
    logging.basicConfig(format=LOGGING_FORMAT)
    grabber()
