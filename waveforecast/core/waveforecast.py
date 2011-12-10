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
__author__ = "cooke"
__date__ = "$27-Nov-2011 11:39:41$"
from datetime import datetime
from datetime import timedelta
import logging
import threading

import numpy
from pydap.client import open_dods
from pydap.exceptions import ServerError
import pydap.lib
#pydap.lib.CACHE = "/tmp/pydap-cache/"
wavemetrics = {
'dirpwsfc':'** surface none primary wave direction [deg] ',
'dirswsfc':'** surface none secondary wave direction [deg]',
'htsgwsfc':'** surface none significant height of combined wind waves and swell [m] ',
'perpwsfc':'** surface none primary wave mean period [s] ',
'perswsfc':'** surface none secondary wave mean period [s] ',
'ugrdsfc':'** surface none u-component of wind [m/s] ',
'vgrdsfc':'** surface none v-component of wind [m/s] ',
'wdirsfc':'** surface none wind direction (from which blowing) [deg] ',
'windsfc':'** surface none wind speed [m/s] ',
'wvdirsfc':'** surface none direction of wind waves [deg] ',
'wvpersfc':'** surface none mean period of wind waves [s] ',
#'time':'*'
}

dataset = {}
baseurl = 'http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'

def chooseTime(gmTime):
    if isinstance(gmTime, datetime):
        gmTime = gmTime.utctimetuple()
    if gmTime.tm_hour >= 18:
        tm_hour = 18
    elif gmTime.tm_hour >= 12:
        tm_hour = 12
    elif gmTime.tm_hour >= 6:
        tm_hour = 6
    else:
        tm_hour = 0
    logging.debug('Hour:' + str(tm_hour))
    return tm_hour

class GetForeCastThread(threading.Thread):
    def __init__ (self, variable, gmTime, tm_hour, lattitudeIndex, longitudeIndex):
        self.variable = variable
        self.gmTime = gmTime
        self.tm_hour = tm_hour
        self.lattitudeIndex = lattitudeIndex
        self.longitudeIndex = longitudeIndex
        threading.Thread.__init__ (self)

    def getData(self):
        todayString = self.gmTime.strftime('%Y%m%d')
        global baseurl
        oururl = baseurl + todayString + '/nww3' + \
            todayString + '_%02dz' % self.tm_hour
        dodsUrl = oururl + ".dods?" + \
            "{2}.{2}[0:1:60][{0}:1:{0}][{1}:1:{1}]".format(
                                                           self.lattitudeIndex,
                                                           self.longitudeIndex,
                                                           self.variable)
        logging.debug('DODS:' + dodsUrl)
        try:
            return open_dods(dodsUrl)
        except ServerError:
            logging.debug('URL DOES NOTEXIST')
            self.gmTime -= timedelta(hours=6)
            self.tm_hour = chooseTime(self.gmTime)
            return self.getData()

    def run (self):
        global dataset
        dataset[self.variable] = self.getData()

lattitudes = range(-78, 79)
longitudes = list(numpy.linspace(0, 358.75, 288))

def getWaveConditions(lattitude, longitude,gmTime=datetime.utcnow()):
        tm_hour = chooseTime(gmTime)
        lattitude = round(float(lattitude));
        #Find closest in database...
        longitude = round(float(longitude) / 1.25) * 1.25
        if longitude < 0 and longitude > -180:
            longitude = 360 + longitude

        lattitudeIndex = lattitudes.index(lattitude)
        longitudeIndex = longitudes.index(longitude)
        getForeCastThreads = []
        for variable in wavemetrics.keys():
            if variable == 'time'or variable == 'lat' or variable == 'lon':
                continue
            logging.debug('Starting Thread: ' + variable)
            newThread = GetForeCastThread(variable, gmTime, tm_hour,
                                          lattitudeIndex, longitudeIndex)
            newThread.start()
            getForeCastThreads.append(newThread)
            logging.debug('Thread Started')

        logging.debug('\n\n\n-----------------------------------------------\nWaiting for threads to stop')
        for thread in getForeCastThreads:
            thread.join()
        logging.debug('\n\n\n-----------------------------------------------\nAll threads stopped:'+str(dataset))

        retDict = {'results':dataset,
            'lat':lattitude,
            'lon':longitude, }

        return retDict

