"""test_shane URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Import count_endpoint from views.py
from main.views import count_endpoint
from main.views import get_all_data_mdb
from main.views import get_all_data_psql


urlpatterns = [
    path('admin/', admin.site.urls),
    # create count_endpoint path
    path('count_endpoint/', count_endpoint, name='count_endpoint'),
    path('get_all_data_mdb/', get_all_data_mdb, name='get_mdb_data'),
    path('get_all_data_psql/', get_all_data_psql, name='get_psql_data'),
]
