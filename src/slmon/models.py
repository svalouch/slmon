
# Copyright 2020, Stefan Valouch (svalouch) <svalouch@valouch.com>
# SPDX-License-Identifier: GPL-3.0-only

'''
Definitions of models.
'''

from pydantic import BaseModel


class BatteryModel(BaseModel):
    '''
    Battery overview.
    '''
    voltage: int
    charge_percent: int
    charge_power: int
    discharge_power: int


class OpenDataModel(BaseModel):
    '''
    Represents the Open JSON dataset.
    '''

    pac: int
    pdc: int
    uac: int
    udc: int
    yield_day: int
    yield_yesterday: int
    yield_month: int
    yield_year: int
    yield_total: int
    cons_pac: int
    cons_yield_day: int
    cons_yield_yesterday: int
    cons_yield_month: int
    cons_yield_year: int
    cons_yield_total: int
    total_power: int
