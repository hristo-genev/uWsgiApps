"""
Definition of views.
"""
import os
import traceback
from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, HttpResponse

from django.template import RequestContext
from datetime import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from epgapp.models import *
from epgapp.forms import *
from epgapp.helper import *
from epgapp.settings import APP_DIR, APP_NAME
from epgapp.serializers import ChannelSerializer

temp_path = os.path.join(APP_DIR, 'temp')

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def grabbing(request):

  assert isinstance(request, HttpRequest)
  is_running = isRunning()

  return render(
    request,
    'grabbing.html',
    {
      'title':'Grabbing',
      'message': '',
      'year': datetime.now().year,
      'isRunning': is_running,
      'schedulers': Scheduler.objects.all(),
      'nChannels': len(Channel.objects.filter(enabled=True)),
      'lastGrabbingTime': get_last_grabbing_time(),
      'log_content': get_log_content(os.path.join(APP_DIR, 'logs/wgmulti.log.txt'))
    }
  )

@login_required
def run(request, id):
    """
    Export grabbing settings, siteinis and start grabbing
    """
    assert isinstance(request, HttpRequest)

    result = {}

    scheduler  = Scheduler.objects.get(id=id)
    settings  = Settings.objects.get(id=scheduler.settings_id)

    settings_file_name = "wgmulti.{0}.config.json".format(settings.id);
    settings_file_path = os.path.join(APP_DIR, 'temp', settings_file_name)

    result['config']   = save_config_file(scheduler, settings_file_path)

    json_data = generate_settings_file_content(settings)
    result['settings'] = save_settings_file(json_data, settings_file_path )
    result['siteinis'] = save_siteinis()
    result['grabbing'] = start_grabbing()

    return JsonResponse(result)


@login_required
def exported_settings(request, id=None):
  if id:
    settings = Settings.objects.get(id=id)
    content = generate_settings_file_content(settings)
    file_name = 'wgmulti.%s.config.json' % id if id else None
    save_settings_file(content, None, file_name)
  return JsonResponse(content, json_dumps_params={'ensure_ascii': False, 'indent': 2})


@login_required
def settings(request):

  """ Renders the settings page"""

  assert isinstance(request, HttpRequest)
  settings = None
  message = None

  if Settings.objects.all():
    settings = Settings.objects.all()[0]

  form = SettingsForm(request.POST or None, instance=settings)

  if request.POST and form.is_valid():
    form.save()
    message = 'Successfully saved settings!'

  return render(
    request,
    'settings.html',
    {
      'form': form.as_table(),
      'message': message
    }
  )

def getUptodateColor(dateInEpg):
  try:
    today = '%s%02d%02d' % (datetime.now().year, datetime.now().month, datetime.now().day)
    dateInEpg = dateInEpg[0:8]
    itoday = int(today)
    idateInEpg = int(dateInEpg)

    #logger.debug("today: %s, epg: %s" % (today, dateInEpg))

    if dateInEpg > today:
      return "green"
    elif dateInEpg == today:
      return "yellow"
    else:
      return "red"
  except:
    return "red"


class ChannelListView(ListView):

    model = Channel
    paginate_by = 50
    ordering = ['-created']

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context['now'] = timezone.now()
      return context

    def get_queryset(self):
      channels = Channel.objects.filter(enabled=True)
      q = self.request.GET.get('q')
      if q:
        channels = channels.filter(name__icontains=q)

      channels = channels.order_by('created')

      #channels_in_report = get_report()['report']['channels']
      for channel in channels:
        ch = get_report(channel.xmltv_id)['report']
        #for ch in channels_in_report:
        #if ch['name'] == channel.name:
        channel.programsCount = ch.get('programsCount')
        channel.siteiniName = ch.get('siteiniName')
        channel.siteiniIndex = ch.get('siteiniIndex')
        channel.firstShowStartsAt = ch.get('firstShowStartsAt')
        channel.lastShowStartsAt = ch.get('lastShowStartsAt')
        channel.uptodateColor = getUptodateColor(channel.lastShowStartsAt)
        #continue

      return channels

class ChannelDetailView(DetailView):

    model = Channel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_path = os.path.join(APP_DIR, 'temp/', context['channel'].xmltv_id + '.epg.xml')
        context['content'] = get_raw_epg(file_path)
        context['now'] = timezone.now()
        context['xmltv_id'] = context['channel'].xmltv_id

        return context


class SiteiniListView(ListView):

    model = Siteini
    paginate_by = 30
    #ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def get_queryset(self):
      result = super(SiteiniListView, self).get_queryset()
      q = self.request.GET.get('q')
      if q:
        result = result.filter(name__icontains=q)

      return result

    #def get_queryset(self):
    #    try:
    #        name = self.kwargs['name']
    #    except:
    #        name = ''

    #    if (name != ''):
    #        object_list = self.model.objects.filter(name__icontains = name)
    #    else:
    #        object_list = self.model.objects.all()
    #    return object_list

class SiteiniDetailView(DetailView):

  model   = Siteini

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['now'] = timezone.now()
    file_path = os.path.join(APP_DIR, 'temp/data/', context['siteini'].name, 'epg.xml')
    context['content'] = get_raw_epg(file_path)
    return context


@login_required
def grab(request, slug):

  channel = Channel.objects.get(slug=slug)
  siteinis = Grabbers.objects.filter(channel=channel)
  configs = Settings.objects.all();

  return render(
    request,
    'epgapp/grab_channel.html',
    {
      'channel': channel,
      'siteinis': siteinis,
      'configs': configs,
      'update_types': UPDATE_TYPES
    }
  )


@login_required
def siteini_test(request):
  try: slug = request.META.get('HTTP_REFERER').split('/')[-2]
  except: slug = ""
  siteinis = Siteini.objects.filter(enabled=True)
  configs = Settings.objects.all();

  return render(
    request,
    'epgapp/siteini_test.html',
    {
      'siteinis': siteinis,
      'slug': slug,
      'configs': configs,
      'update_types': UPDATE_TYPES
    }
  )

@login_required
def run_siteini_test(request):

  if request.method == 'GET':
    return JsonResponse({'status': False, 'message': 'GET request not supported for this operation', 'details': 'Do POST' })

  siteini_id  = request.POST['siteini_id']
  name        = request.POST['channel_name']
  xmltv_id    = request.POST['xmltv_id']
  site_id     = request.POST['site_id']
  update_type = request.POST['update']
  config_id   = request.POST['webgrab_configuration_id']

  if name == '':
    name = 'TESTNAME'
  if xmltv_id == '':
    xmltv_id = 'TESTID'
  if update_type == '':
    update_type = 'i'

  channel    = { 'name': name, 'xmltv_id': xmltv_id, 'update': update_type }

  try:
    siteini  = Siteini.objects.get(id=siteini_id)
    location   = os.path.join(temp_path, 'data', siteini.name)

    channel['siteinis'] = [{ 'name': siteini.name, 'site_id': site_id}]

    settings = Settings.objects.get(id=config_id)
    settings.report = False # Disable report for single channel grabbing

    settings_file_path = os.path.join(location, 'wgmulti.config.json')
    save_config_file(None, settings_file_path)

    data = generate_settings_file_content(settings, channel)

    save_settings_file(data, settings_file_path)

    save_siteini(siteini, location)

    res = start_grabbing(location)

    return JsonResponse(res)

  except Exception as ex:
    logger.exception(str(ex))
    return JsonResponse({'status': False, 'message': ex, 'details': traceback.format_exc() })


def grab_single_channel_epg(request):

  if request.method == 'GET':
    return JsonResponse({'status': False, 'message': 'GET request not supported for this operation', 'details': 'Do POST' })

  siteini_id  = request.POST['siteini'].split("|||")[0]
  name        = request.POST['channel_name']
  xmltv_id    = request.POST['xmltv_id']
  site_id     = request.POST['siteini'].split("|||")[1]
  update_type = request.POST['update']
  config_id   = request.POST['webgrab_configuration_id']

  #return HttpResponse(request.POST.items())

  channel    = { 'name': name, 'xmltv_id': xmltv_id, 'update': update_type }

  try:
    siteini = Siteini.objects.get(id=siteini_id)
    channel['siteinis'] = [{ 'name': siteini.name, 'site_id': site_id}]

    location   = os.path.join(temp_path, 'data', siteini.name)

    settings_file_path = os.path.join(location, 'wgmulti.config.json')
    save_config_file(None, settings_file_path)

    settings = Settings.objects.get(id=config_id)
    data = generate_settings_file_content(settings, channel)

    save_settings_file(data, settings_file_path)

    save_siteini(siteini, location)

    res = start_grabbing(location)

    return JsonResponse(res)

  except Exception as ex:

    logger.exception(str(ex))
    return JsonResponse({'status': False, 'message': ex, 'details': traceback.format_exc() })


@login_required
def status(request, processId):
  details = ''
  status = isRunning(processId)
  if status:
    details = get_running_processes_details()
  return JsonResponse( { 'isRunning': status, 'details': details } )


@login_required
def get_siteini_epg(request, siteini):
  """
  Returns EPG for particular siteini or full epg
  """
  dt = ''
  details = ''
  content = ''
  status = True

  try:
    file_path = os.path.join(APP_DIR, 'temp/data/', siteini, 'epg.xml')
    content = get_raw_epg(file_path)
    content = htmlescape(content)
    dt = datetime.fromtimestamp(os.path.getmtime(file_path))

  except Exception as er:
    status = False
    logger.exception(er)
    details = str(er)

  return JsonResponse( { 'status': status, 'raw_epg': content, 'datatime': dt, 'details': details} )


@login_required
def get_channel_epg(request, xmltv_id):
  """
  Returns EPG for particular channel epg
  """
  dt = ''
  details = ''
  status = True
  content = ''

  try:
    file_path = os.path.join(APP_DIR, 'temp/', xmltv_id + '.epg.xml')
    content = get_raw_epg(file_path)
    content = htmlescape(content)

  except:
    status = False
    logger.exception(er)
    details = str(er)

  return JsonResponse( { 'status': status, 'raw_epg': content, 'datatime': dt, 'details': details} )


@login_required
def epg_download(request):

  return redirect('/temp/epg.xml')



def get_epg_report(request):
  return JsonResponse( get_report() )

@login_required
def downloads(request):

  try:
    report = get_report()['report']

  except Exception as er:
    report = {}
    logger.exception(er)
    content = traceback.format_exc()

  return render(
    request,
    '%s/downloads.html' % APP_NAME,
    {
      'report': report,
    }
  )

def regenerate(request):
  (status, details) = regenerate_epg()
  return JsonResponse( { 'status': status, 'details': details} )


def map(request):
  channels = Channel.objects.all()
  #serializer = ChannelSerializer(channels, many=True)
  serializer = ChannelSerializer(channels, many=True)
  for c in serializer.data:
    if c.id:
      del c.id
  #map = json.loads(serializer.data)
  #data = get_channels_map(channels)
  return JsonResponse(serializer.data, json_dumps_params={'ensure_ascii': False, 'indent': 2 }, safe=False)


def python_grabber(request, slug, startdaysahead, grabfordays):
  (status, details) = run_python_grabber(slug, startdaysahead, grabfordays)
  return JsonResponse( {  'pythongrabbername': slug, 'status': status, 'details': details} )

def get_json_epg(request, pythongrabbername, day):
  data = get_epg_for_python_grabber(pythongrabbername, day)
  return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 2 }, safe=False)

def cancel_grabbing(request, processId):
  (status, details) = kill_process_by_id(processId)
  return JsonResponse( { 'status': status, 'details': details} )


@login_required
def get_epg_log(request, siteini=None):

  if siteini:
    log_file_path = os.path.join(APP_DIR, 'temp/data/', siteini, 'WebGrab++.log.txt')
  else:
    log_file_path = os.path.join(APP_DIR, 'logs/wgmulti.log.txt')
  content = get_log_content(log_file_path)

  return HttpResponse(content, content_type="text/plain")

@login_required
def save_modified_epg(request, slug):
  try:
    content = request.POST.get("content")
    xmltv_id = request.POST.get("xmltv_id")
    file_path = os.path.join(APP_DIR, 'temp/', xmltv_id + '.epg.xml')

    (status, details) = save_content_to_file(content, file_path)
  except Exception as er:
    logger.error(ex)
    details = str(er)
    status = False
  return JsonResponse( { 'status': status, 'details': details} )
