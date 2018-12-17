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

def save_config_file(settings=None):
  """
  Saves the wgmulti.exe.config file
  """
  status = False

  try:
    import xml.etree.ElementTree as ET
    config_file_name = 'wgmulti.exe.config'
    config_file_path = os.path.join(APP_DIR, 'bin', config_file_name)
    tree = ET.parse(config_file_path)
    root = tree.getroot()

    def updateKey(key, value):
      el = root.find("./appSettings/add[@key='%s']" % key)
      if el != None:
        el.set('value', value)

    updateKey('GrabingTempFolder', os.path.join(temp_path, 'data'))
    updateKey('ConfigDir', temp_path)
    updateKey('WebGrabFolder', os.path.join(APP_DIR, 'bin'))
    updateKey('MaxAsyncProcesses', str(settings.instances))
    updateKey('RemoveChannelsWithNoProgrammes', str(settings.remove_empty))
    updateKey('CopyOnlyTitleForOffsetChannel', str(settings.only_title))
    updateKey('GenerateResultsReport', str(settings.report))
    updateKey('ReportFolder', os.path.join(APP_DIR, 'logs'))

    tree.write(config_file_path)

    status = True
    message = '%s successfully saved on disk!' % config_file_name

  except Exception as er:

    message = str(er)
    logger.exception('Error during saving wgmulti.config.xml on disk')

  return { 'status': status, 'message': message }

def generate_settings_file_content(settings=None, channels=None):
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


def save_settings_file(data, location=None, file_name=None):
  """
  Saves settings and channels in config JSON file
  """
  status = False
  config_file_path = get_config_file_path(location, file_name)

  try:
    content = JSONRenderer().render(data, renderer_context={'indent': 2})
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
    wgmulti_log = os.path.join(APP_DIR, 'logs', 'wgmulti.log.txt')

    if not configDir:
      configDir = os.path.join(APP_DIR, 'temp')

    import uuid
    id = uuid.uuid4().hex[:6].upper()

    cmd = '%s -configDir %s -id %s > %s 2>&1 &' % (wgmulti, configDir, id, wgmulti_log)

    if os.name == 'nt': # Windows
      cmd.replace(' 2>&1 &', '')
      #cmd = 'START /B wgmulti.exe -configDir %s -id %s > ../logs/wgmulti.log.txt' % (configDir, id)
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


def get_report():
  details = ''
  status = False
  report = {}
  try:
    import json
    with open (os.path.join(APP_DIR, 'logs', 'wgmulti.report.json'), encoding='utf-8') as r:
      report = json.load(r)
    status = True

  except Exception as er:
    message = str(er)
    #details = traceback.format_exc()

  return {'status': status, 'message': message, 'details': details, 'report': report}

def get_raw_epg(siteini=None):
  content = ''
  try:
    if siteini:
      raw_epg_file_path = os.path.join(APP_DIR, 'temp/data/', siteini, 'epg.xml')
    else:
      raw_epg_file_path = os.path.join(APP_DIR, 'temp', 'epg.xml')
    content = open(raw_epg_file_path, 'r', encoding='utf-8').read()
  except Exception as er:
    logger.exception(er)

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
