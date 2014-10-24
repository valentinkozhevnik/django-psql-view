from psqlview.base import Singleton
from django.db.transaction import TransactionManagementError
__author__ = 'vako'


class ItemsRows(object):
    def __init__(self, row_list, row_values):
        for attr, value in zip(row_list, row_values):
            setattr(self, attr, value)


class BasePostgresView(object):
    __metaclass__ = Singleton
    rows_items = []
    initial_view = ""
    item_class = ItemsRows
    sql_view_name = None

    def __init__(self, connection=None, debug=False, *args, **kwargs):
        # TODO: initial sql from psql
        if not connection:
            from django.db import connection
        self.connection = connection
        if debug:
            cursor = self.connection.cursor()
            cursor.execute(self.get_initial_view())
            try:
                self.connection.commit()
            except TransactionManagementError as e:
                pass
        self.cache = {}

    def get_initial_view(self):
        if self.initial_view:
            return self.initial_view
        raise NotImplementedError

    def _query(self, items="*", wheres='', orders=''):
        cursor = self.connection.cursor()
        cursor.execute('SELECT {items} FROM {view_name} {wheres}'.format(
            view_name=self.sql_view_name, items=items, wheres=wheres))
        return cursor.fetchall()

    def _query_filter(self, **kwargs):
        pass

    def all(self):
        result = []
        for items in self._query():
            result.append(self.item_class(self.rows_items, items))
        return result

    def iterator(self):
        for items in self._query():
            yield self.item_class(self.rows_items, items)

    def filter(self, **kwargs):
        def __query_generate(key, dictionary):
            if isinstance(dictionary[key], str):
                return "%s=\'%s\'" % (key, dictionary[key])
            return "%s=%s" % (key, dictionary[key])
        if set(kwargs.keys()) - set(self.rows_items):
           raise Exception('Fields \"%s\" not supported' % ','.join(set(kwargs.keys()) - set(self.rows_items)))
        from functools import partial
        map_function = partial(__query_generate, dictionary=dict(kwargs))
        query = " AND ".join(list(map(map_function, kwargs.keys())))

        result = []
        for items in self._query(wheres='WHERE %s' % query):
            result.append(self.item_class(self.rows_items, items))
        return result