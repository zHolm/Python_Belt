from django.conf.urls import url
from . import views
                    
urlpatterns = [
    
    url(r'^trips/new/create$', views.create_trip),
    url(r'^trips/new$', views.new_trip),
    url(r'^trips/(?P<trip_id>\d+)/edit/submit$', views.submit_edit),
    url(r'^trips/(?P<trip_id>\d+)/cancel$', views.cancel),
    url(r'^trips/(?P<trip_id>\d+)/join$', views.join),
    url(r'^trips/(?P<trip_id>\d+)/edit$', views.edit_trip),
    url(r'^trips/(?P<trip_id>\d+)/remove$', views.remove_trip),
    url(r'^trips/(?P<trip_id>\d+)$', views.trips),
    url(r'^dashboard$', views.dashboard),
    url(r'^email$', views.email, name='email'),
    url(r'^success$', views.welcome),
    url(r'^register$', views.register, name='register'),
    url(r'^validate_login$', views.validate_login),
    url(r'^logout$', views.logout),
     url(r'^$', views.index),
]
