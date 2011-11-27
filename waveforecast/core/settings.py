import logging
import sys
settings={
'DEBUGLEVEL':logging.DEBUG,
'DEBUGSTREAMOUT':sys.stdout,
'DEBUGFORMAT':'%(name)s->%(filename)s:%(lineno)d|%(levelname)s=>%(message)s',
}

def setLogger():
    logging.basicConfig(level=settings['DEBUGLEVEL'],
        format=settings['DEBUGFORMAT'],
        stream=settings['DEBUGSTREAMOUT']
        )
