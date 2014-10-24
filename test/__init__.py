__author__ = 'vako'

from psqlview.view import BasePostgresView, ItemsRows

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


if __name__ == "__main__":
    import psycopg2
    test_view = TestBase(connection=psycopg2.connect("dbname=test user=vako password=1508"))
    test_view2 = TestBase(connection=psycopg2.connect("dbname=test user=vako password=1508"))
    df = test_view.iterator()
    print(df)
    print(next(df))
    print(test_view.all()[0].get_sum())
    print(test_view2.filter(one=4))