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
  return HttpResponse("Home", content_type="text/plain")

def grab(request, channel, startdaysahead=0):
  assert isinstance(request, HttpRequest)
  programs = get_programs(channel, startdaysahead)
  return JsonResponse(programs, json_dumps_params={"indent":2, "separators":(',', ': '), "ensure_ascii":False}, safe=False)

def get_raw_response(request):
  response = None
  url = request.GET.get("url")
  if url:
    r = requests.get(url)
    response = r.text
  return HttpResponse(response)
