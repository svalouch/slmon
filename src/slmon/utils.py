
# Copyright 2020, Stefan Valouch (svalouch) <svalouch@valouch.com>
# SPDX-License-Identifier: GPL-3.0-only

'''
Utility functions
'''

from typing import Dict


def cleaner(data: Dict) -> Dict:
    '''
    Clean all ``ACCESS DENIED`` fields from the input data. This is a recursive function.
    '''
    if isinstance(data, dict):
        data = {key: cleaner(value) for key, value in data.items() if value != 'ACCESS DENIED'}
    elif isinstance(data, list):
        data = [cleaner(item) for item in data if item != 'ACCESS DENIED']
    return data
