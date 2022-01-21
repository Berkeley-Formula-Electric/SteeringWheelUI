import logging

from birge_comm_net import CommNetCore

server = CommNetCore(("localhost", 8000), log_level=logging.INFO)
server.run()
