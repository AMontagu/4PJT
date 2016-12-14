"""
See https://channels.readthedocs.io/en/latest/routing.html
"""

from channels.routing import route, route_class, include
from server.ws.consumers import *

apiSocket = [
	route_class(TestJsonConsumer, path=r"^/test/"),
	route_class(ChatConsumer, path=r"^/api/"),
	route("websocket.connect", ws_add),  # default for getting connection not in hease protocol remove in release
	route("websocket.receive", ws_message),  # default for getting message not in hease protocol remove in release
	route("websocket.disconnect", ws_disconnect),
	# default for getting disconnection not in hease protocol remove in release
]

channel_routing = [
	include(apiSocket, path=r'^/ws')
]
