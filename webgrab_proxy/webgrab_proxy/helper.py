#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import time
import base64
import codecs
import datetime
import requests
from webgrab_proxy.utils import *

out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')

def get_programs(channel, startdaysahead, maxdays):
  if channel == 'moviestar':
    return moviestar(startdaysahead, maxdays)

def moviestar(startdaysahead, maxdays):
  STARTDAY = startdaysahead #3 means start capturing 3 days ahead
  MAXDAYS = maxdays #capture for how many days
  GRAB_DETAILS = True
  channel = "moviestar"
  host = base64.b64decode("aHR0cDovL21vdmllc3Rhci5iZy8=")
  headers = {"User-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36" , "Referer": host}
  url_template = "%s?rhc_action=get_calendar_events&post_type[]=events&start=%s&end=%s&rhc_shrink=0&view=agendaDay"
  output = json.dumps({})

  ### Calculate dates for for scrabbing days
  dates = get_dates(MAXDAYS, STARTDAY)
  total = 0


  ### Iterate day
  daily_programs = {}
  for i in range(0, int(MAXDAYS)):

    programs = []
    programs_sorted = []
    url = url_template % (host.decode('utf-8'), dates[i].epochtime, dates[i+1].epochtime)
    items = get_content_json(url, headers)
    file_name = get_file_name( out_dir, channel, dates[i].day )
    #return items.encode("utf-8").decode('unicode-escape')
    #return codecs.decode(items, 'unicode_escape')
    #return json.dumps(items, ensure_ascii=False)
    #return bytes(items, "utf-8").decode("unicode_escape")

    # Save full content and convert to json
    #with open(file_name, "wb") as f:
    #  f.write(items.encode('utf8'))

    # load json
    #items = json.load(codecs.open(file_name, 'r', 'utf-8-sig'))
    #items = json.loads(codecs.open(text, 'r', 'utf-8-sig'))
    #with open(file_name, 'r') as f:
    #  items = json.load(f)

    #with open(file_name, "wb") as f:
    #  f.write(json.dumps(items, ensure_ascii=False).encode('utf-8'))
    #  #f.write(_json)
    #with open(file_name, 'r', encoding="utf8") as f:
    #  items = json.load(f)

    for item in items["EVENTS"]:
      rdates = item["fc_rdate"].split(",")

      for rdate in rdates:
        if dates[i].datetime in rdate:
          title = normalize(item["title"]) .capitalize()
          starttime = rdate[9:11]+":"+rdate[11:13]
          program = Program(starttime, title)

          program.url = item.get("url")
          programs.append(program)

    if GRAB_DETAILS:
      print ("Searching for movie details")
      for program in programs:
        try:
          text = get_content(program.url, headers)

          m = re.compile("og:description\"\s+content=\"(.*?)\"\s*/>").findall(text)
          if len(m) > 1:
            program.description = m[1]
            print ("Description found!")
          elif len(m) == 1:
            program.description = m[0]

          m = re.compile("og:image:url\" content=\"(.*?)\"").findall(text)
          if len(m) > 0:
            program.icon = m[0]
            print ("Icon found")

          m = re.compile("<li><strong>Режисьор:</strong>(.*)</li>").findall(text)
          if len(m) > 0:
            program.director = normalize(m[0])
            print ("Director found")

          m = re.compile("<li><strong>.*?(\d\d\d\d).*?</strong>").findall(text)
          if len(m) > 0 and m[0] != "0000":
            program.year = m[0]
            print ("Year found")

          m = re.compile("<li><strong>(\D*?)</strong></li>").findall(text)
          if len(m) > 0:
            program.category = normalize(m[0]).replace("<span lang=\\\"BG\\\">", "")
            print ("Category found!")

          m = re.compile("<li><strong>\d\d\d\d\s(.+?)</strong>").findall(text)
          if len(m) > 0:
            program.country = normalize(m[0])
            print ("Country found")

          m = re.compile("<li><strong>В ролите:.*?</strong>(.+?)</li>").findall(text)
          if len(m) > 0:
            program.cast = normalize(m[0])
            print ("Cast found")

        except Exception as er:
          print(er)

        if hasattr(program, "url"):
          del program.url
    # Add daily programs to day object
    daily_programs[dates[i].day] = sort(to_dict(programs))

  return daily_programs



