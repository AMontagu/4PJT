"""
See https://channels.readthedocs.io/en/latest/routing.html
"""

from channels.routing import route, route_class, include
from project.consumers import *

apiSocket = [
	route_class(ChatJsonConsumer, path=r"^/chat/(?P<token>[0-9A-Za-z]+)/(?P<groupname>[0-9A-Za-z-]+)"),
	route_class(UserJsonConsumer, path=r"^/user/(?P<token>[0-9A-Za-z]+)/(?P<username>[0-9A-Za-z-]+)"),
	route("websocket.connect", ws_add),  # default for getting connection not in hease protocol remove in release
	route("websocket.receive", ws_message),  # default for getting message not in hease protocol remove in release
	route("websocket.disconnect", ws_disconnect),
	# default for getting disconnection not in hease protocol remove in release
]

channel_routing = [
	include(apiSocket, path=r'^/ws')
]
