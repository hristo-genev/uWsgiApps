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

    return render(
        request,
        'grabbing.html',
        {
            'title':'Grabbing',
            'message': '',
            'year': datetime.now().year,
            'isRunning': isRunning(),
            'configs': Settings.objects.all(),
            'nChannels': len(Channel.objects.filter(enabled=True)),
            'lastGrabbingTime': '00:00:00'
        }
    )

@login_required
def run(request, id):
    """
    Export grabbing settings, siteinis and start grabbing
    """
    assert isinstance(request, HttpRequest)

    result = {}

    settings = Settings.objects.get(id=id)
    data = generate_settings_file_content(settings)
    result['config']   = save_config_file(settings)
    result['settings'] = save_settings_file(data)
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


class ChannelListView(ListView):

    model = Channel
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class ChannelDetailView(DetailView):

    model = Channel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        file_path = os.path.join(APP_DIR, 'temp/', context['channel'].xmltv_id + '.xml')
        context['content'] = get_raw_epg(file_path)
        context['now'] = timezone.now()
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
        try:
            name = self.kwargs['name']
        except:
            name = ''

        if (name != ''):
            object_list = self.model.objects.filter(name__icontains = name)
        else:
            object_list = self.model.objects.all()
        return object_list

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

  return render(
    request,
    'epgapp/grab.html',
    {
      'channel': channel,
      'siteinis': siteinis
    }
  )


@login_required
def siteini_test(request):
  slug = request.META.get('HTTP_REFERER').split('/')[-2]
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
    data = generate_settings_file_content(settings, channel)
    save_settings_file(data, location)
    save_siteini(siteini, location)
    res = start_grabbing(location)
    return JsonResponse(res)

  except Exception as ex:
    logger.exception(str(ex))
    return JsonResponse({'status': False, 'message': ex, 'details': traceback.format_exc() })


@login_required
def status(request, processId):
  status = isRunning(processId)
  return JsonResponse( { 'isRunning': status } )


@login_required
def get_siteini_epg(request, siteini):
  """
  Returns EPG for particular siteini or full epg
  """
  dt = ''
  details = ''
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
def epg_download(request):

  return redirect('/temp/epg.xml')


@login_required
def get_epg_log(request, siteini):

  try:
    log_file_path = os.path.join(APP_DIR, 'temp/data/', siteini, 'WebGrab++.log.txt')
    content = open(log_file_path, 'r', encoding='utf-8').read()

  except Exception as er:
    logger.exception(er)
    content = traceback.format_exc()

  return HttpResponse(content, content_type="text/plain")


def get_epg_report(request):
  return JsonResponse( get_report() )

@login_required
def stats(request):

  try:
    report = get_report()['report']

  except Exception as er:
    report = {}
    logger.exception(er)
    content = traceback.format_exc()

  return render(
    request,
    '%s/stats.html' % APP_NAME,
    {
      'report': report,
    }
  )
