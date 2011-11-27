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
import logging
from time import gmtime
from time import strftime
import httplib

from pydap.client import open_url
import pydap.lib
pydap.lib.CACHE = "/tmp/pydap-cache/"
logger=None
class WaveForecast(object):
    noaaurl='http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww320111119/nww320111119_18z'
    baseurl='http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'
    oururl='http://nomads.ncep.noaa.gov:9090/dods/wave/nww3/nww3'
    infourl = ''

    def __init__(self,settings,gmTime=gmtime()):
        logging.debug('Creating the WaveForecast:'+str(gmTime))

        if gmTime.tm_hour > 18:
            tm_hour = 18
        elif gmTime.tm_hour > 12:
            tm_hour = 12
        elif gmTime.tm_hour > 6:
            tm_hour = 6
        else:
            tm_hour = 0
        logging.debug('Hour:'+str(tm_hour))
        self.setDate(gmTime,tm_hour)

     def exists(site, path):
        conn = HTTPConnection(site)
        conn.request('HEAD', path)
        response = conn.getresponse()
        conn.close()
        return response.status == 200
        
    def setDate(self,gmTime,tm_hour):
        todayString = strftime('%Y%m%d',gmTime)
        self.oururl = self.baseurl + todayString+'/nww3'+todayString+'_%02dz'% tm_hour
        self.infourl = self.oururl+'.info'
        logging.debug('BASEURL:'+self.oururl+' INFO URL:'+self.infourl)


    def getConditions(self,lattidue,longitude):
        pass


if __name__ == "__main__":
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
