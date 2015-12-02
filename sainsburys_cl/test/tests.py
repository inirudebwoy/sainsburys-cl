from main import calc_total


class TestCalcTotal:

    def test_empty_list(self):
        assert(calc_total([]) == '0.00')

    def test_full_list(self):
        assert(calc_total([{'unit_price': 1}, {'unit_price': 2}]) == '3.00')

    def test_full_list_with_empty_dict(self):
        assert(calc_total([{'unit_price': 1}, {'unit_price': 2}, {}]) == '3.00')
