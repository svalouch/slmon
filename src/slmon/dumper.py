
# Copyright 2020, Stefan Valouch (svalouch) <svalouch@valouch.com>
# SPDX-License-Identifier: GPL-3.0-only

'''
Query response dumper
'''

import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path

log = logging.getLogger('slmon.dumper')


class Dumper:
    '''
    Dumps the received string to filesystem. The timestamp can be set using :func:`fix_ts` to allow for multiple files
    to be written with the same timestamp encoded into the file name.

    To avoid stressing the filesystem, one file per hour is created. This ensures that the amount of files in a
    directory is somewhat limited. Each file written has the unix timestamp encoded into the filename, too.

    :param base_dir: Base directory, everything will be dumped below this path. An attempt to create it is made if it
       does not exist.
    '''
    def __init__(self, base_dir: str) -> None:
        self._dir = Path(base_dir)

        self._dir.mkdir(parents=True, exist_ok=True)
        log.debug(f'Initialized with dir {self._dir}')
        self.fix_ts()

    def fix_ts(self) -> None:
        '''
        Updates the internal timestamp to the current UTC time.
        '''
        self._ts = datetime.utcnow()
        log.debug(f'Fixed ts to {self._ts}')

    def dump(self, filename: str, data: str, ext: str = '.json') -> None:
        '''
        Dumps a string of data to a file. The current timestamp (see :func:`fix_ts`) is appended, following by the
        extension. The file is written in an atomic manner.

        :param filename: The base filename to use for dumping. Timestamp and extension are appended automatically.
        :param data: The data to dump.
        :param ext: Filename extension, appended after the timestamp.
        '''
        timestamp = int(datetime.timestamp(self._ts))
        target = self._dir / self._ts.strftime('%Y-%m-%d_%H')
        target.mkdir(parents=True, exist_ok=True)
        log.debug(f'dumping to {target} / {filename}')

        fd, tname = tempfile.mkstemp(dir=target)  # pylint: disable=invalid-name  # fd is well understood
        os.write(fd, data.encode('utf-8'))
        os.close(fd)
        os.rename(tname, target / f'{filename}-{timestamp}{ext}')
