
# Copyright 2020, Stefan Valouch (svalouch) <svalouch@valouch.com>
# SPDX-License-Identifier: GPL-3.0-only

'''
Exception classes used by the application.
'''


class SLMonException(Exception):
    '''
    Base exception raised by the various parts of the application
    '''


class WriterException(SLMonException):
    '''
    Raised by writer plugins.
    '''


class SolarLogError(SLMonException):
    '''
    Raised when a problem with the connection to the data logger occurs.
    '''
