import os
from channels.asgi import get_channel_layer

from server.customLogging import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_server.settings")

print("ici")
initializeLog("PJTWS", "PJTWS.txt", True, 10)
LOGINFO("LOG INITIALIZED in asgi")

channel_layer = get_channel_layer()
