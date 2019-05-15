"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpRequest, JsonResponse, HttpResponse
from datetime import datetime
from webgrab_proxy.helper import *
import requests

def home(request):
  assert isinstance(request, HttpRequest)
  content = '<h3>Sites</h3>'
  content += '<a href="moviestar/">Moviestar</a><br />'
  return HttpResponse(content, content_type="text/plain")

def grab(request, channel, startdaysahead=0, maxdays=1):
  assert isinstance(request, HttpRequest)
  maxdays = int(maxdays) if maxdays else 1
  programs = get_programs(channel, startdaysahead, maxdays)
  return JsonResponse(programs, json_dumps_params={"indent":2, "separators":(',', ': '), "ensure_ascii":False}, safe=False)

def get_raw_response(request):
  response = None
  url = request.GET.get("url")
  if url:
    r = requests.get(url)
    response = r.text
  return HttpResponse(response)
