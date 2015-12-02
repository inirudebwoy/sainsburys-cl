from mock import patch

from bs4 import BeautifulSoup

from sainsburys_cl.main import calc_total, product_details, get_html
from sainsburys_cl.parsing import HTML_PARSER, _find_item, find_title, \
    find_description, find_price


class TestCalcTotal:

    def test_empty_list(self):
        assert(calc_total([]) == '0.00')

    def test_full_list(self):
        assert(calc_total([{'unit_price': 1}, {'unit_price': 2}]) == '3.00')

    def test_full_list_with_empty_dict(self):
        assert(calc_total([{'unit_price': 1}, {'unit_price': 2}, {}]) == '3.00')


class TestProductDetails:

    def test_empty_html(self):
        assert(product_details('') == {})

    def test_correct_html(self):
        with patch('sainsburys_cl.main.get_html') as mock_get_html:
            with open('sainsburys_cl/test/test_product_details.html') as test_html:
                html = test_html.read()
                html_size = len(html)
                expected = {'title': 'Testing gizmo',
                            'size': html_size,
                            'unit_price': 999,
                            'description': 'So much gizmo.'}
                mock_get_html.return_value = (BeautifulSoup(html, HTML_PARSER),
                                              html_size)
            assert(product_details('') == expected)


class TestGetHtml:

    def test_failed_get(self):
        assert(get_html('') == (None, None))

    def test_successful_get(self):

        class RequestMock(object):
            headers = {'content-length': 10}
            content = open('sainsburys_cl/test/test_product_details.html').read()

        with patch('sainsburys_cl.main.requests') as mock_requests:
            mock_requests.get.return_value = RequestMock()
            result = get_html('')
            assert(result.size == '0.0kb')
            assert(result.content)


class TestFinders:

    def test__find_not_found_element(self):
        html = BeautifulSoup('<!DOCTYPE html>', HTML_PARSER)
        assert(_find_item(html, '.productTitleDescriptionContainer > h1') ==
               '')

    def test__find_found_element(self):
        with open('sainsburys_cl/test/test_product_details.html') as test_html:
            html = BeautifulSoup(test_html.read(), HTML_PARSER)
            assert(_find_item(html, '.productTitleDescriptionContainer > h1') ==
                   'Testing gizmo')

    def test_title_found(self):
        with open('sainsburys_cl/test/test_product_details.html') as test_html:
            html = BeautifulSoup(test_html.read(), HTML_PARSER)
            assert(find_title(html) == 'Testing gizmo')

    def test_description_found(self):
        with open('sainsburys_cl/test/test_product_details.html') as test_html:
            html = BeautifulSoup(test_html.read(), HTML_PARSER)
            assert(find_description(html) == 'So much gizmo.')

    def test_price_found(self):
        with open('sainsburys_cl/test/test_product_details.html') as test_html:
            html = BeautifulSoup(test_html.read(), HTML_PARSER)
            assert(find_price(html) == 999.0)
