"""dlan URL Configuration

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

from home import views as home_views  # main views, see home/views.py
from booking import views as booking_views  # ticket views, se booking/views.py

urlpatterns = [
    path("", home_views.home, name='home'),
    path("admin/", admin.site.urls),
    path("tournament/", home_views.tournament, name="tournament"),
    path("hall-of-fame/", home_views.hof, name='hall-of-fame'),
    path("information/", home_views.info, name="information"),
    path("tickets/", booking_views.tickets, name='tickets'),
    path("checkout", booking_views.checkout, name='checkout'),
    path("canceled", booking_views.canceled, name="canceled"),
    path('stripe_checkout/', booking_views.stripe_checkout, name='stripe_checkout'),
    path('check_liuid_exists/', booking_views.check_liuid_exists,
         name='check_liuid_exists'),  # for AJAX query to database
]
