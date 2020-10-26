
# Copyright 2020, Stefan Valouch (svalouch) <svalouch@valouch.com>
# SPDX-License-Identifier: GPL-3.0-only

'''
Query builder
'''

import json
from typing import Dict, List, Union


class QueryBuilder:
    '''
    Constructs queries for querying a Solar-Log™ device. The query can be constructed by repeatedly calling
    `add_query`.
    '''

    _data: Dict

    def __init__(self) -> None:
        self._data = dict()

    def json(self) -> str:
        '''
        Returns the JSON string result.
        '''
        return json.dumps(self._data)

    def add_query(self, query: Union[str, List[int]]) -> None:
        '''
        Adds the given query. Query parts can either be added via lists such as ``[800, 170]``, or via strings. For
        strings, the format is as follows:

        * Separate distinct queries using a semicolon (``;``)
        * Separate elements in a query using colons (``:``)

        Thus, these two parameters are identical: ``[800, 170]``, ``800:170``, but with strings it is possible to add
        multiple queries in one go.
        '''
        if isinstance(query, str) and len(query) > 0:
            queries = query.split(';')
            for parts in queries:
                self.add_query([int(x) for x in parts.split(':')])
        elif isinstance(query, list):
            ptr = self._data
            i = 0
            while i < len(query):
                elem = query[i]
                i += 1
                if i == len(query):
                    ptr[elem] = None
                else:
                    if elem not in ptr:
                        ptr[elem] = dict()
                    ptr = ptr[elem]
