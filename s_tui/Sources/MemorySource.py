#!/usr/bin/env python

# Copyright (C) 2017-2018 Alex Manuskin, Maor Veitsman
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

from __future__ import absolute_import
from collections import OrderedDict

import os
import time
import math

from s_tui.Sources.Source import Source

import logging
logger = logging.getLogger(__name__)


class MemorySource(Source):

    procmen = '/proc/meminfo/'

    def __init__(self, package_number=0):
        self.package_number = package_number
        self.update()

    def get_meminfo(self):
        ''' Return the information in /proc/meminfo as a dictionary '''
        meminfo=OrderedDict()
        with open('/proc/meminfo') as f:
            for x in range(3):
                key, value = f.readline().split(':')
                meminfo[key] = value.split()[0].strip()
        self.total = int(meminfo['MemTotal']) >> 10
        self.avail = int(meminfo['MemAvailable']) >> 10

    # Source super class implementation
    def get_is_available(self):
        return self.is_available

    def update(self):
        self.get_meminfo()

    def get_reading(self):
        return self.total-self.avail

    def get_maximum(self):
        return self.total

    def reset(self):
        pass

    def get_summary(self):
        return {'Memory in use': '%d %s' %
                (self.total-self.avail, self.get_measurement_unit()),
                'Available Memory': '%d %s' %
                (self.avail, self.get_measurement_unit())}

    def get_source_name(self):
        return 'Memory'

    def get_measurement_unit(self):
        return 'MB'

    def is_available(self):
        return True


if '__main__' == __name__:
    mem = MemorySource()
    while True:
        print(mem.get_summary())
        time.sleep(2)
