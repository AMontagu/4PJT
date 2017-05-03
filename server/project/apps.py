from django.apps import AppConfig
from server.customLogging import *


class ProjectConfig(AppConfig):
    name = 'project'

    def ready(self):
        initializeLog("ProjectWS", "ProjectWS.txt", True, 10)
        LOGINFO("LOG INITIALIZED in apps.py")