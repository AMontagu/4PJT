"""PJT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from project import views
from rest_framework.authtoken import views as tokenView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.loginUser),
    url(r'^signin/', views.signinUser),
    url(r'^logout/', views.logoutUser),
    url(r'^isloggedin/', views.isLoggedIn),
    url(r'^addcontact/', views.addContact),
    url(r'^userinfos/', views.getUserInformations),
    url(r'^simpleuserinfos/', views.getSimpleUserInformations),
    url(r'^useredit/', views.editUser),
    url(r'^creategroup/', views.createGroup),
    url(r'^addusertogroup/', views.addUserToGroup),
    url(r'^removegroup/', views.removeGroup),
    url(r'^quitgroup/', views.quitGroup),
    url(r'^api-token-auth/', tokenView.obtain_auth_token),
    url(r'^user-autocomplete/$', views.userAutocomplete)
]
