from django.conf.urls import url
import app.views

urlpatterns = [
  url(r'^$', app.views.home, name='home'),
  url(r'(?P<channel>.*?)/(?P<startdaysahead>\d)/(?P<maxdays>\d)*/*$', app.views.grab, name='grab'),
  url(r'^get', app.views.get_raw_response, name='get-raw-response'),
]
