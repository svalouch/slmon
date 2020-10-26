
# Copyright 2020, Stefan Valouch (svalouch) <svalouch@valouch.com>
# SPDX-License-Identifier: GPL-3.0-only

'''
Data sink base class
'''

import logging
from datetime import datetime
from typing import Dict, List, Optional, Union

from .models import BatteryModel, OpenDataModel


class DataSink:
    '''
    Interface for receiving parsed data from the :class:`Mapper`. The mapper calls the functions, starting with
    :func:`on_begin` at the beginning of mapping, ending with :func:`on_end` after the mapper has finished.
    '''

    def on_begin(self, timestamp: Optional[datetime] = None) -> None:
        '''
        Called at the beginning before sending other data. If the mapper found a timestamp in the data, it is passed as
        argument.
        '''

    def on_plain(self, name: str, datatype: str, value: Union[int, str, Dict, List]) -> None:
        '''
        Called when a known free-standing value was found.

        :name: Name of the value according to current knowledge.
        :param datatype: Type of the data, one of: ``int``, ``str``, ``dict``, ``list``
        :param value: The value.
        '''

    def on_open_data(self, data: OpenDataModel) -> None:
        '''
        Called when data from the Open JSON API has been found.
        '''

    def on_battery(self, data: BatteryModel) -> None:
        '''
        Called when the battery overview has been found.
        '''

    def on_unknown(self, datatype: str, path: List[int], value: Union[int, str, Dict, List]) -> None:
        '''
        Called when an unknown data point is found.

        :param datatype: The type of data, one of: ``int``, ``str``, ``list``, ``dict``.
        :param path: The path of the data. The Open JSON timestamp {801:{170:{100}}} would be encoded as [801, 170,
           100] in this structure.
        :param value: The data value.
        '''

    def on_inventory(self, info: str, data: Dict) -> None:
        '''
        Called when inventory information is encountered.

        :param info: The type of information, such as ``serials`` for serial numbers.
        :param data: The data depending on the info.
        '''

    def on_complete(self) -> None:
        '''
        Called at the end of mapping. This can be used to commit transactions or do calculations on the data received.
        '''


class DebugSink(DataSink):
    '''
    Debugging tool. This DataSink will print debug information.
    '''
    _log = logging.getLogger('slmon.debugsink')

    def on_begin(self, timestamp: Optional[datetime] = None) -> None:
        self._log.debug(f'on_begin({timestamp})')

    def on_plain(self, name: str, datatype: str, value: Union[int, str, Dict, List]) -> None:
        self._log.debug(f'on_plain(name={name}, datatype={datatype}, value="{value}")')

    def on_open_data(self, data: OpenDataModel) -> None:
        self._log.debug(f'on_open_data({data})')

    def on_battery(self, data: BatteryModel) -> None:
        self._log.debug(f'on_battery({data})')

    def on_unknown(self, datatype: str, path: List[int], value: Union[int, str, Dict, List]) -> None:
        self._log.debug(f'on_unknown(datatype={datatype}, path={":".join([str(x) for x in path])}, value="{value})')

    def on_inventory(self, info: str, data: Dict) -> None:
        self._log.debug(f'on_inventory(info={info}, data="{data}")')

    def on_complete(self) -> None:
        self._log.debug('on_complete()')
