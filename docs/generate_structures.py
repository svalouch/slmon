#!/usr/bin/env python3

# Copyright 2020, Stefan Valouch (svalouch) <svalouch@valouch.com>
# SPDX-License-Identifier: GPL-3.0-only

'''
Generates CSV tables from the structures definition file.
'''

import csv
from typing import Dict, List, Optional

import yaml


with open('structures.yml', 'rt') as fin:
    data = yaml.safe_load(fin.read())

f_r_100 = open('table_r_100.csv', 'wt')
f_s_141 = open('table_s_141.csv', 'wt')
f_s_143 = open('table_s_143.csv', 'wt')
f_r_200 = open('table_r_200.csv', 'wt')
f_r_300 = open('table_r_300.csv', 'wt')
f_r_400 = open('table_r_400.csv', 'wt')
f_r_500 = open('table_r_500.csv', 'wt')
f_r_600 = open('table_r_600.csv', 'wt')
f_r_700 = open('table_r_700.csv', 'wt')
f_r_800 = open('table_r_800.csv', 'wt')
f_s_800 = open('table_s_800.csv', 'wt')
f_s_801 = open('table_s_801.csv', 'wt')
f_s_860 = open('table_s_860.csv', 'wt')

csv_r_100 = csv.writer(f_r_100)
csv_s_141 = csv.writer(f_s_141)
csv_s_143 = csv.writer(f_s_143)
csv_r_200 = csv.writer(f_r_200)
csv_r_300 = csv.writer(f_r_300)
csv_r_400 = csv.writer(f_r_400)
csv_r_500 = csv.writer(f_r_500)
csv_r_600 = csv.writer(f_r_600)
csv_r_700 = csv.writer(f_r_700)
csv_r_800 = csv.writer(f_r_800)
csv_s_800 = csv.writer(f_s_800)
csv_s_801 = csv.writer(f_s_801)
csv_s_860 = csv.writer(f_s_860)

csv_r_100.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_s_141.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_s_143.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_r_200.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_r_300.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_r_400.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_r_500.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_r_600.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_r_700.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_r_800.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_s_800.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_s_801.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'L0', 'L1', 'L2', 'L3', 'T', 'Example', 'Description'])
csv_s_860.writerow(['ID1', 'ID2', 'ID3', 'ID4', 'ID5', 'ID6', 'ID7', 'L0', 'L1', 'L2', 'L3', 'T', 'Example',
                    'Description'])

TYPE_MAP = {None: '?', 'str': 'S', 'int': 'I', 'bool': 'B', 'array': 'A', 'object': 'O', 'float': 'F'}


def handle_element(id: int, element: Dict, toplevel_id: int, l0: Optional[bool] = None, l1: Optional[bool] = None,
                   l2: Optional[bool] = None, l3: Optional[bool] = None, level: int = 0,
                   struct_type: str = 'r') -> None:

    if 'exists' in element and not element['exists']:
        sl0 = ''
        sl1 = ''
        sl2 = ''
        sl3 = ''
        rtype = ''
        example = ''
        comment = 'Does not exist'
    else:
        comment = element['comment'] if element['comment'] else 'Unknown'

        rtype = TYPE_MAP[element['type']]
        if rtype not in ['A', 'O'] and 'children' in element and 'substructure' not in element:
            print(f'{toplevel_id}/id {id}/level {level} has children but is not an array/object')
        elif rtype in ['A', 'O'] and 'children' not in element and 'substructure' not in element:
            print(f'{toplevel_id}/id {id}/level {level} is an array/object without children')

        # TODO there are legitimate null values!
        if 'value' in element:
            example = element['value']
            if rtype == 'S' and example == '':
                example = '``""``'
            else:
                example = f'``{element["value"]}``' if element['value'] is not None else ''
        else:
            if rtype not in ['O', 'A']:
                print(f'{toplevel_id}/level {level}/id {id}: no value but not an object either')
            example = ''

        if 'l0' in element:
            l0 = element['l0']
        sl0 = 'Y' if l0 else 'N' if l0 is not None else ''
        if 'l1' in element:
            l1 = element['l1']
        sl1 = 'Y' if l1 else 'N' if l1 is not None else ''
        if 'l2' in element:
            l2 = element['l2']
        sl2 = 'Y' if l2 else 'N' if l2 is not None else ''
        if 'l3' in element:
            l3 = element['l3']
        sl3 = 'Y' if l3 else 'N' if l3 is not None else ''

    if struct_type == 'r' or (struct_type == 's' and toplevel_id != 860):
        if 300 <= toplevel_id < 400 or 700 <= toplevel_id < 800:
            if level == 0:
                submit_row(toplevel_id, [id, '', '', '', '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            elif level == 1:
                submit_row(toplevel_id, ['', id, '', '', '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            elif level == 2:
                submit_row(toplevel_id, ['', '', id, '', '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            elif level == 3:
                submit_row(toplevel_id, ['', '', '', id, '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            elif level == 4:
                submit_row(toplevel_id, ['', '', '', '', id, '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            elif level == 5:
                submit_row(toplevel_id, ['', '', '', '', '', id, sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            else:
                print(f'{toplevel_id}/id {id}/level {level} not accepted, exceeds level limit')
        else:
            if level == 0:
                submit_row(toplevel_id, [id, '', '', '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            elif level == 1:
                submit_row(toplevel_id, ['', id, '', '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            elif level == 2:
                submit_row(toplevel_id, ['', '', id, '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            elif level == 3:
                submit_row(toplevel_id, ['', '', '', id, '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            elif level == 4:
                submit_row(toplevel_id, ['', '', '', '', id, sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
            else:
                print(f'{toplevel_id}/id {id}/level {level} not accepted, exceeds level limit')
    else:
        if level == 0:
            submit_row(toplevel_id, [id, '', '', '', '', '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
        elif level == 1:
            submit_row(toplevel_id, ['', id, '', '', '', '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
        elif level == 2:
            submit_row(toplevel_id, ['', '', id, '', '', '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
        elif level == 3:
            submit_row(toplevel_id, ['', '', '', id, '', '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
        elif level == 4:
            submit_row(toplevel_id, ['', '', '', '', id, '', '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
        elif level == 5:
            submit_row(toplevel_id, ['', '', '', '', '', id, '', sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
        elif level == 6:
            submit_row(toplevel_id, ['', '', '', '', '', '', id, sl0, sl1, sl2, sl3, rtype, example, comment], struct_type)
        else:
            print(f'{toplevel_id}/id {id}/level {level} not accepted, exceeds level limit')

    if 'children' in element and len(element['children']) > 0:
        for n_id, n_element in element['children'].items():
            handle_element(n_id, n_element, toplevel_id, l0=l0, l1=l1, l2=l2, l3=l3, level=level + 1,
                           struct_type=struct_type)
    elif 'substructure' in element and len(element['substructure']) > 0:
        for n_id, n_element in element['substructure'].items():
            handle_element(n_id, n_element, toplevel_id, l0=l0, l1=l1, l2=l2, l3=l3, level=0, struct_type='s')


def submit_row(id: int, row: List, struct_type: str = 'r') -> None:
    if 100 <= id < 200:
        if struct_type == 's' and id in [141, 143]:
            if id == 141:
                csv_s_141.writerow(row)
            else:
                csv_s_143.writerow(row)
        else:
            csv_r_100.writerow(row)
    elif 200 <= id < 300:
        csv_r_200.writerow(row)
    elif 300 <= id < 400:
        csv_r_300.writerow(row)
    elif 400 <= id < 500:
        csv_r_400.writerow(row)
    elif 500 <= id < 600:
        csv_r_500.writerow(row)
    elif 600 <= id < 700:
        csv_r_600.writerow(row)
    elif 700 <= id < 800:
        csv_r_700.writerow(row)
    elif 800 <= id < 900:
        if struct_type == 's' and id in [800, 801, 860]:
            if id == 800:
                csv_s_800.writerow(row)
            elif id == 801:
                csv_s_801.writerow(row)
            else:
                csv_s_860.writerow(row)
        else:
            csv_r_800.writerow(row)
    else:
        print(id)


for id in range(100, 1000):
    try:
        struct = data['structures'][id]
    except KeyError:
        continue

    handle_element(id=id, element=struct, toplevel_id=id, level=0)


for f in [f_r_100, f_s_141, f_s_143, f_r_200, f_r_300, f_r_400, f_r_500, f_r_600, f_r_700, f_r_800, f_s_800, f_s_801,
          f_s_860]:
    try:
        f.close()
    except Exception:
        pass
