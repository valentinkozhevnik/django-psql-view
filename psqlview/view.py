from psqlview.base import Singleton

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

    def __init__(self, connection=None, *args, **kwargs):
        # TODO: initial sql from psql
        if not connection:
            from django.db import connection
        self.connection = connection
        cursor = self.connection.cursor()
        cursor.execute(self.get_initial_view())
        self.connection.commit()
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
            return "%s=%s" % (key, dictionary[key])
        print(kwargs.keys())
        if set(kwargs.keys()) - set(self.rows_items):
           raise Exception('Fields \"%s\" not supported' % ','.join(set(kwargs.keys()) - set(self.rows_items)))
        print(dict(kwargs))
        from functools import partial
        map_function = partial(__query_generate, dictionary=dict(kwargs))
        query = " AND ".join(list(map(map_function, kwargs.keys())))

        print(query)
        result = []
        for items in self._query(wheres='WHERE %s' % query):
            result.append(self.item_class(self.rows_items, items))
        return result