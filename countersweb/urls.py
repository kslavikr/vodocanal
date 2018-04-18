"""countersweb URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from webapp.views import (UserRegistration, UserAutorization, UserCountersInfo, 
                          CounterValueSet, RestorePass, HelpPageInfo,
                          UserChengePass,AdminPanelPage)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', HelpPageInfo.as_view(),
        name="main_page"),
    url(r'^registration$', UserRegistration.as_view(),
        name="user_registration"),
    url(r'^authorization$', UserAutorization.as_view(),
        name="user_authorization"),
    url(r'^counters/info$', UserCountersInfo.as_view(),
        name="counters_info"),
    url(r'^counter/value/set$', CounterValueSet.as_view(),
        name="counters_set_val"),
    url(r'^password/restore$', RestorePass.as_view(),
        name="restore_pass"),
    url(r'^help$', HelpPageInfo.as_view(),
        name="help_info"),
    url(r'^chenge/pass$', UserChengePass.as_view(),
        name="chenge_pass"),
    url(r'^admintool$', AdminPanelPage.as_view(),
        name="admintool"),
]
