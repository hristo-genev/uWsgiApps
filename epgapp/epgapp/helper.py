import os
import sys
import json
from .serializers import *
from rest_framework.renderers import JSONRenderer
import subprocess
import logging
import requests
import traceback
from .settings import APP_DIR
from importlib import import_module
from epgapp.proxy import pygrabbers

logger = logging.getLogger(__name__)

cwd = os.path.abspath(os.path.dirname(__file__))
temp_path = os.path.join(cwd, 'temp')

def get_config_file_path(location=None, file_name=None):
  '''
  Args:
    Location: the path relative to temp/
  Returns the path to the config file.
  Creates missing directories
  '''
  export_dir = temp_path

  if location:
    export_dir = os.path.join(temp_path, location)

  if not file_name:
    file_name = 'wgmulti.config.json'

  if not os.path.isdir(export_dir):
    os.makedirs(export_dir, True)
    os.chmod(export_dir, 0o777)

  return os.path.join(export_dir, file_name)

def create_dir(dir):
  try:
    if not os.path.isdir(dir):
      os.makedirs(dir, True)
      os.chmod(dir, 0o777)
    return True
  except Exception as er:
    logger.exception(er)
    return False

def isRunning(processId='wgmulti.exe'):
    """
    Checks whether a process is running
    """
    try:
      cmd = 'ps aux | grep %s | grep -v grep' % processId
      ret = os.system(cmd)
      return True if ret == 0 else False
    except Exception as er:
      message = traceback.format_exc()
      logger.exception('Error during isRunning execution')
      return False

def save_config_file(scheduler=None, wgmulti_settings_file_path=None):
  """
  Saves the wgmulti.exe.config file
  """
  status = False

  try:
    import xml.etree.ElementTree as ET
    config_file_name = 'wgmulti.exe.config'
    config_file_path = os.path.join(APP_DIR, 'bin', config_file_name)
    config_file_template = os.path.join(APP_DIR, 'bin', 'wgmulti.exe.config.template')
    tree = ET.parse(config_file_template)
    root = tree.getroot()

    def updateKey(key, value):
      el = root.find("./appSettings/add[@key='%s']" % key)
      if el != None:
        el.set('value', value)

    updateKey('GrabingTempFolder', os.path.join(temp_path, 'data'))
    updateKey('ConfigDir', temp_path)
    updateKey('WebGrabFolder', os.path.join(APP_DIR, 'bin'))

    if scheduler:
      updateKey('MaxAsyncProcesses', str(scheduler.instances))
      updateKey('RemoveChannelsWithNoProgrammes', str(scheduler.remove_empty))
      updateKey('CopyOnlyTitleForOffsetChannel', str(scheduler.only_title))
      updateKey('GenerateResultsReport', str(scheduler.report))
      updateKey('PostprocessScript', scheduler.postcommand)
      logger.debug("postprocess script: %s" % scheduler.postcommand)
      updateKey('PostprocessArguments', scheduler.postargs)
      logger.debug("postprocess script: %s" % scheduler.postargs)

    updateKey('ReportFolder', os.path.join(APP_DIR, 'logs'))
    updateKey('RunPostprocessScript', 'true')

    if not wgmulti_settings_file_path:
      wgmulti_settings_file_path = os.path.join(APP_DIR, 'temp', 'wgmulti.config.json')
    updateKey('JsonConfigFileName', wgmulti_settings_file_path)

    tree.write(config_file_path)

    status = True
    message = '%s successfully saved on disk!' % config_file_name

  except Exception as er:

    message = 'Error during saving wgmulti.exe.config on disk'
    logger.exception(message)

  return { 'status': status, 'message': message }

def generate_settings_file_content(settings, channels=None):
  """
  Export settings and channels to JSON
  """
  try:
    serializer = SettingsSerializer(settings)

    # copy serialized data to new object so it becomes mutable
    data       = {'channels': []}
    data.update(serializer.data)

    if channels:
      serializer = SingleChannelSerializer(channels)
      data['channels'].append(serializer.data)
    else:
      channels = Channel.objects.filter(enabled=True)
      serializer = ChannelSerializer(channels, many=True)
      data['channels'] = serializer.data

    return data

  except Exception as er:

    #message = traceback.format_exc()
    logger.exception('Error during saving siteinis to disk operation')

  return None


def save_settings_file(json_data, config_file_path):
  """
  Saves settings and channels in config JSON file
  """
  status = False
  create_dir(os.path.dirname(config_file_path))

  try:
    content = JSONRenderer().render(json_data, renderer_context={'indent': 2})
    with open(config_file_path, 'wb') as w:
      w.write(content)

    status = True
    message = 'Settings successfully saved on disk!'

  except Exception as er:
    message = str(er)
    logger.exception('Error during saving siteinis to disk operation')
    logger.exception(traceback.format_exc())

  return { 'status': status, 'message': message }

def get_settings_file_content(location=None, file_name=None):
  try:
    return open(get_config_file_path()).read()
  except:
    return {}


def save_siteini(siteini, location):
  """
    Saves siteini content in a given location
    Creates the directory if it doesn't exist
  """
  if not os.path.isdir(location):
    os.makedirs(location, True)
    os.chmod(location, 0o777)

  with open(os.path.join(location, siteini.name + '.ini'), 'wb') as w:
    w.write(siteini.content.encode('utf-8'))

def save_siteinis():
  """
    Save selected siteini or all on the disk
  """
  status = False
  details = ''
  siteinis_path = os.path.join(temp_path, 'siteini.pack')

  try:
    siteinis = Siteini.objects.filter(enabled=True)

    for siteini in siteinis:
      save_siteini(siteini, siteinis_path)

    status = True
    message = 'Siteinis successfully saved on disk!'

  except Exception as er:

    message = str(er)
    #details = traceback.format_exc()
    logger.exception('Error during saving siteinis to disk operation')

  return { 'status': status, 'message': message, 'details': details }

def start_grabbing(configDir=None):
  """
  Start wgmulti for given config folder.
  If config folder is not provided, the default one is used.
  Returns an object containing the ID of the started process - None if error occurs

  """
  status  = False
  details = ''
  pid     = -1

  try:
    wgmulti     = os.path.join(APP_DIR, 'bin', 'wgmulti.exe')

    if configDir:
      # we are running a single siteini test
      wgmulti_log = os.path.join(configDir, 'wgmulti.log.txt')
    else:
      configDir = os.path.join(APP_DIR, 'temp')
      wgmulti_log = os.path.join(APP_DIR, 'logs', 'wgmulti.log.txt')

    import uuid
    id = uuid.uuid4().hex[:6].upper()

    cmd = '%s -configDir %s -id %s > %s 2>&1 &' % (wgmulti, configDir, id, wgmulti_log)

    #if os.name == 'nt': # Windows
    #  cmd.replace(' 2>&1 &', '')
    #  cmd = 'START /B wgmulti.exe -configDir %s -id %s > ../logs/wgmulti.log.txt' % (configDir, id)
    logger.debug('COMMAND: %s' % cmd)

    #subprocess.call(cmd, shell=True)
    #import psutil
    p = subprocess.Popen(cmd, shell=True)
    #pid = p.pid
    logger.debug("wgmulti unique identifier: %s" % id)

    #process = psutil.Process(pid)
    #for proc in process.children(recursive=True):
    #  logger.debug("%s: %s" % (proc.name(), proc.pid))

    #pid = isRunning(id=id)
    status = True
    message = 'Successfully started grabbing process, PID is %s' % id

  except Exception as er:
    message = str(er)
    #details = traceback.format_exc()
    logger.exception('Error during start_grabbing()')

  return { 'status': status, 'message': message, 'processId': id} #, 'stdout': stdout.decode("utf-8")}


def get_report(channel_xmltv_id=None):
  message = ''
  details = ''
  status = False
  report = {}
  try:
    file_path = os.path.join(APP_DIR, 'logs', channel_xmltv_id + '.report.json')
    logger.debug("Getting report from file: %s" % file_path)
    with open (file_path, encoding='utf-8') as r:
      report = json.load(r)
    status = True
  except Exception as er:
    message = str(er)
    #details = traceback.format_exc()

  return {'status': status, 'message': message, 'details': details, 'report': report}

def get_raw_epg(raw_epg_file_path):
  content = ''
  try:
    #if siteini:
    #  raw_epg_file_path = os.path.join(APP_DIR, 'temp/data/', siteini, 'epg.xml')
    #else:
    #  raw_epg_file_path = os.path.join(APP_DIR, 'temp', 'epg.xml')
    content = open(raw_epg_file_path, 'r', encoding='utf-8').read()
  except Exception as er:
    logger.exception(er)
    content = str(er)
  return content

def htmlescape(content):
  return content.replace('<', '&lt;').replace('>', '&gt;')


def batch_modify_channels(channels, operation='enable'):

  message = ""
  enabled  = 0
  disabled = 0
  enabled_channel_names = []
  disabled_channel_names = []
  disabled_channel_names_grouped = ""
  enabled_channel_names_grouped = ""

  try:
    for channel in channels:
      if operation == 'disable' and channel.enabled:
        channel.enabled = False
        disabled_channel_names.append(channel.name)
        channel.save()
        disabled += 1

      elif operation == 'enable' and not channel.enabled:
        channel.enabled = True
        enabled_channel_names.append(channel.name)
        channel.save()
        enabled += 1

    message = "%s channels were %sd." % (disabled, operation)

    if enabled > 0 and enabled < 5:
      enabled_channel_names_grouped = ",".join(enabled_channel_names[:5])
      message = message.replace('enabled.', 'enabled (%s)' % enabled_channel_names_grouped)

    if disabled > 0 and disabled < 5:
      disabled_channel_names_grouped = ", ".join(disabled_channel_names[:5])
      message = message.replace('disabled.', 'disabled (%s)' % disabled_channel_names_grouped)

  except Exception as e:
    logger.exception(e)
    message = str(e)

  return message

def sync_channels_with_playlist(channels):

  names = []
  names_stripped = []
  disabled = 0
  enabled  = 0
  enabled_channel_names = []
  disabled_channel_names = []

  try:
    r = requests.get(os.environ['playlist_url'], stream=True) #
    for line in r.iter_lines():
      if line.startswith(b'#EXTINF'):
        name = line.split(b',')[1]
        names.append(name.decode("utf-8"))
        names_stripped.append(name.replace(b' HD', b'').replace(b' SD', b'').decode("utf-8"))

    for channel in channels:
      if channel.enabled:
        # If channel is enabled, disable it if it's NOT in the current playlist
        if channel.name not in names and channel.name not in names_stripped:
          channel.enabled = False
          disabled_channel_names.append(channel.name)
          channel.save()
          disabled += 1

      else:
        # If channel is disabled, enabled it if it's in the current playlist
        if channel.name in names or channel.name in names_stripped:
          channel.enabled = True
          enabled_channel_names.append(channel.name)
          channel.save()
          enabled += 1

    message = "%s channels were disabled. %s channels were enabled." % (disabled, enabled)

    if enabled > 0 and enabled < 5:
      enabled_channel_names_grouped = ",".join(enabled_channel_names[:5])
      message = message.replace('enabled.', 'enabled (%s)' % enabled_channel_names_grouped)

    if disabled > 0 and disabled < 5:
      disabled_channel_names_grouped = ",".join(enabled_channel_names[:5])
      message = message.replace('disabled.', 'disabled (%s)' % disabled_channel_names_grouped)

  except Exception as e:
    logger.exception(e)
    message = str(e)

  return message


def get_running_processes_details():
  output = ''
  try:
    cmd = 'ps -eo pid,ppid,pcpu,pmem,start_time,time,args | grep -v grep | grep WebGrab\+Plus\.exe'
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    p.wait()

    output = output.decode('utf-8')
    output = output.replace('/usr/bin/mono-sgen /home/g/uWsgiApps/epgapp/epgapp/bin/', '')
    output = output.replace('/home/g/uWsgiApps/epgapp/epgapp/temp/data/', '')
    output = output.replace('/usr/bin/mono-sgen ', '')

  except Exception as er:
    logger.exception(er)

  return output


def get_last_grabbing_time():
  try:
    return get_report()['report']['generatedOn']
  except Exception as er:
    logger.debug(er)
    return '00:00:00'


def regenerate_epg():
  status = False
  details = None
  epgfiles = []

  try:
    import glob
    import xml.etree.ElementTree as ET

    tv = ET.Element("tv")

    for file in glob.glob("epgapp/temp/*.epg.xml"):
      try:
        logger.debug(file)
        root = ET.parse( file ).getroot()
        tv.append( root.find( 'channel' ) )
        tv.extend( root.findall( 'programme' ) )

      except Exception as er:
        logger.exception(er)


    tree = ET.ElementTree(tv)
    tree.write(os.path.join(temp_path, "epg.xml"))

    status = True
    details = "EPG successfully regenerated!"

  except Exception as er:

    details = str(er)

  return (status, details)

def get_channels_map(channels):
  streams = {}

  try:
    map = {'streams' : streams}
    for c in channels:
      alt_names = AlternativeName.objects.select_related().filter(channel=c.id)
      if len(alt_names) > 0:
        for alt_name in alt_names:
          stream = {}
          streams[alt_name.name] = stream
          stream['name'] = alt_name.name
      else:
        stream = {}
        streams[c.name] = stream
        stream['name'] = c.name

  except Exception as er:
    logger.exception(er)

  return streams


def run_python_grabber(slug, startdaysahead=0, grabfordays=1):

  status = False
  details = ''
  out_dir = os.path.join(cwd, 'proxy')
  pythongrabbername = slug
  obj = Proxy.object.get(slug=pythongrabbername)

  with open(os.joing(out_dir, pythongrabbername + '.py'), w) as w:
    w.write(obj.content)

  if hasattr(pygrabbers, pythongrabbername):
    try:
      logger.debug("Executing %s(%s, %s)" % (pythongrabbername, startdaysahead, grabfordays))
      func = getattr(pygrabbers, pythongrabbername)
      res = func(out_dir, int(startdaysahead), int(grabfordays))
      status = True
      details = str(res)

    except Exception as er:
      logger.exception(er)
      details = str(er)

  return (status, details)



def get_epg_for_python_grabber(name, day=None):

  if day is None:
    import datetime
    day = datetime.date.today()

  day = '%02d' % int(day)

  file_path = os.path.join(cwd, 'pythongrabbers', name, "%s.json" % day)
  if os.path.isfile(file_path):
    with open(file_path) as f:
      return json.load(f)
  return {}



def kill_process_by_id(id):
  status = False
  details = ''
  try:
    cmd = 'ps -eo pid,args | grep -v grep | grep %s' % id
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    (output, err) = p.communicate()
    p.wait()
    output = output.decode('utf-8')
    logger.debug("Ouput: %s" % output)

    try:
      import re
      m = re.compile("(\d+?)\s").findall(output)
      logger.debug("Found %s matches" % len(m))
      if len(m) > 0:
        logger.debug("process id is: %s" % m[0])
        logger.debug("Sending kill signal")
        os.system("kill -9 %s" % m[0])
        details = "Process with identifier %s should have been killed" % m[0]
        logger.debug(details)
        status = True
      else:
        details = 'No process with identifier %s was found to be running!' % id
    except Exception as er:
      logger.exception(er)
      details = str(er)

  except Exception as er:
    logger.exception(er)
    details = str(er)

  return (status, details)


def get_log_content(log_file_path=None):
  content = ''
  try:
    logger.debug("Getting log content from file: %s" % log_file_path)
    content = open(log_file_path, 'r', encoding='utf-8').read()
  except Exception as er:
    logger.exception(er)
    content = "Error! Could not load the log file!"
  return content


def save_content_to_file(content, file_path):
  status = False
  details = ""
  try:
    with open(file_path, 'w') as w:
      w.write(content)
      status = True
  except Exception as er:
    details = str(er)
    logger.exception(er)

  return (status, details)
