import os, site, inspect
site.addsitedir(os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe()))))

import logging
import time

import DemoService
import ttypes

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.TMultiplexedProcessor import TMultiplexedProcessor

from Config import Config

from DemoHandler import DemoHandler

if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)-15s %(message)s',
                      datefmt='%Y-%m-%dT%H:%M:%S')
  logging.Formatter.converter = time.gmtime

  processor = TMultiplexedProcessor()

  processor.registerProcessor("Demo", DemoService.Processor(DemoHandler()))

  transport = TSocket.TServerSocket(
      '10.1.20.59', port='9090')
  tfactory = TTransport.TBufferedTransportFactory()
  pfactory = TBinaryProtocol.TBinaryProtocolFactory()

  # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
  # You could do one of these for a multithreaded server
  #server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
  #server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)
  server = TServer.TForkingServer(processor, transport, tfactory, pfactory)

  logging.info('Starting the server...')
  server.serve()
  logging.info('done.')
