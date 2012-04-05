# Unless otherwise specified by LICENSE.txt files in individual
# directories, all code is:

# Copyright (c) 2011, Python Wave Forecast team
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#     2. Redistributions in binary form must reproduce the above copyright notice,
#        this list of conditions and the following disclaimer in the documentation
#        and/or other materials provided with the distribution.
#     3. Neither the name of the Python Wave Forecast team nor the names of its
#        contributors may be used to endorse or promote products derived from this
#        software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from datetime import datetime
from datetime import timedelta
import logging
from math import fabs
import unittest

import pydap
from waveforecast.core.waveforecast import chooseNearestHour
from waveforecast.core.waveforecast import getWaveConditions
import waveforecast.core.settings as settings
class  WaveForecast_TestCase(unittest.TestCase):
    def setUp(self):
        pass
        

    #def tearDown(self):
    #    self.foo.dispose()
    #    self.foo = None
    def test_choosetime(self):
        gmTime = datetime.utcnow()
        gmTime = gmTime.replace(hour=23)
        self.assertEqual(chooseNearestHour(gmTime),18)
        gmTime = gmTime.replace(hour=18)
        self.assertEqual(gmTime.hour,18)
        self.assertEqual(chooseNearestHour(gmTime),18)
        gmTime = gmTime.replace(hour=17)
        logging.debug(gmTime.hour)
        self.assertEqual(chooseNearestHour(gmTime),12)
        gmTime = gmTime.replace(hour= 12)
        self.assertEqual(chooseNearestHour(gmTime),12)
        gmTime = gmTime.replace(hour= 11)
        self.assertEqual(chooseNearestHour(gmTime),6)
        gmTime = gmTime.replace(hour= 6)
        self.assertEqual(chooseNearestHour(gmTime),6)
        gmTime = gmTime.replace(hour= 5)
        self.assertEqual(chooseNearestHour(gmTime),0)
        gmTime = gmTime.replace(hour= 0)
        self.assertEqual(chooseNearestHour(gmTime),0)


    def test_getconditions(self):
        dataset = getWaveConditions(-34,-16);
        logging.debug(dataset)

if __name__ == '__main__':
    settings.setLogger()
    logging.debug('test_waveforecast')
    unittest.main()

