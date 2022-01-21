import logging

from birge_comm_net import CommNetCore

server = CommNetCore(("0.0.0.0", 8000), log_level=logging.INFO)
server.run()
