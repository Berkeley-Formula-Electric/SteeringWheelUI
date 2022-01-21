import logging

from birge_comm_net import CommNetCore

server = CommNetCore(("0.0.0.0", 2400), log_level=logging.INFO)
server.run()
