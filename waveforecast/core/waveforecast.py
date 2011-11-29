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
__author__="cooke"
__date__ ="$27-Nov-2011 11:39:41$"
from datetime import datetime
from datetime import timedelta
from httplib import HTTP
from httplib import HTTPConnection
import logging
from time import gmtime
from time import strftime
from urlparse import urlparse

from pydap.client import open_url
from pydap.exceptions import ServerError
import pydap.lib
pydap.lib.CACHE = "/tmp/pydap-cache/"
logger=None
class WaveForecast(object):
    baseurl='http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'
    oururl='http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'
    dataset = None

    def __init__(self,settings,gmTime=datetime.utcnow()):
        logging.debug('Creating the WaveForecast:'+str(gmTime))
        tm_hour = self.chooseTime(gmTime)
        self.dataset = self.getDataSet(gmTime,tm_hour)

    def chooseTime(self,gmTime):
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
        logging.debug('Hour:'+str(tm_hour))
        return tm_hour
        
    def getDataSet(self,gmTime,tm_hour):
        todayString = gmTime.strftime('%Y%m%d')
        self.oururl = self.baseurl + todayString+'/nww3'+todayString+'_%02dz'% tm_hour
        logging.debug('BASEURL:'+self.oururl)
        try:
            return open_url(self.oururl)
        except ServerError:
            logging.debug('URL DOES NOTEXIST')
            gmTime -= timedelta(hours=6)
            return self.getDataSet(gmTime,self.chooseTime(gmTime))

    def getConditions(self,lattidue,longitude):
        pass


if __name__ == "__main__":
    dataset = None
    #dataset = open_url(url)
    #print type(dataset)
    #print dataset.keys()
    for key,dirpwsfc in dataset.items():
        print '########################################'
        print key
        if key != 'time':
            data = dirpwsfc[ : , (-10 == dirpwsfc.lat) , (dirpwsfc.lon == 340) ]
        else:
            print data.array
            print len(data.array)

        try:
            raw= data.array[:]
            print 'The first one:'
            print raw[0]
            print 'The Secdond one'
            print raw[1]
        except Exception:
            raw = data.array
            print 'The value: '+str(raw.data)
