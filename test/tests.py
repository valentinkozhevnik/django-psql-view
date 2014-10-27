__author__ = 'vako'

from psqlview.view import BasePostgresView, ItemsRows

import unittest

class ItemFromTest(ItemsRows):
    one=None
    two=None

    def get_sum(self):
        return self.one + self.two

class TestBase(BasePostgresView):
    initial_view = """
    CREATE OR REPLACE VIEW HELLO_MAN AS
        SELECT sum(1+1) AS one, sum(1+2) AS two;
    """
    sql_view_name = 'HELLO_MAN'
    rows_items = ('one', 'two')
    item_class = ItemFromTest


class TestedWork(unittest.TestCase):
    def setUp(self):
        import psycopg2
        self.test_view = TestBase(connection=psycopg2.connect("dbname=test user=vako password=1508"), debug=True)
        self.item = self.test_view.all()[0]

    def test_view_database(self):
        self.assertEqual(self.test_view.sql_view_name, 'HELLO_MAN')
        self.assertEqual(len(self.test_view.rows_items), 2)

    def test_values(self):
        self.assertEqual(len(self.test_view.all()), 1)
        self.assertIsInstance(self.item, self.test_view.item_class)
        self.assertIsInstance(self.item, ItemFromTest)

    def test_item_from_test(self):
        self.assertEqual(self.item.get_sum(), 5)
        self.assertEqual(self.item.one, 2)
        self.assertEqual(self.item.two, 3)


if __name__ == "__main__":
    unittest.main()