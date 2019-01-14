from django.db import models
from django.utils import timezone
from django.urls import reverse
#

UPDATE_TYPES = [
  ('', ''),
  ('i', 'i - Incremental'),
  ('l', 'l - Light'),
  ('s', 's - Smart'),
  ('f', 'f - Forced'),
]

POSTPROCESS_TYPES = [
  ('mdb', 'mdb'),
  ('rex', 'rex'),
]

class Siteini(models.Model):
  import uuid
  name     = models.CharField('Name of siteini file', max_length=32)
  slug     = models.SlugField('Slug', unique=False, default="", help_text='How it appears in URL')
  enabled  = models.BooleanField(default=True)
  content  = models.TextField()
  created  = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)

  def get_absolute_url(self):
    return reverse('siteini-detail', args=[str(self.slug)])

  def __str__(self):
    return self.name

  class Meta:
    ordering = ['name']
    verbose_name_plural = '       Siteinis'

#class Broadcaster(models.Model):
#  name = models.CharField(max_length=256)

#  def get_absolute_url(self):
#    return reverse('model-detail-view', args=[str(self.id)])

#  def __str__(self):
#    return self.name

#  class Meta:
#    ordering = ['-name']
#    verbose_name_plural = ' TV Broadcasters'


class Category(models.Model):
  name = models.CharField(max_length=64)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = '        Channel categories'


class Channel(models.Model):
  enabled     = models.BooleanField(default=True)
  name        = models.CharField('Name of channel', max_length=32)
  xmltv_id    = models.CharField('Channel id in XMLTV', max_length=32)
  slug        = models.SlugField('Slug', max_length=32, unique=True, help_text='Name in URL')
  update      = models.CharField('Update type',default="i", max_length=1, choices=UPDATE_TYPES, blank=True)
  siteinis    = models.ManyToManyField(Siteini, through='Grabbers')
  #parent      = models.ForeignKey("self", verbose_name="Parent (if timeshifted)", on_delete=models.CASCADE, blank=True, null=True)
  #timeshifts  = models.OneToManyField()
  #offset      = models.IntegerField(default=0)
  include     = models.CharField(blank=True, max_length=256)
  exclude     = models.CharField(blank=True, max_length=256)
  period      = models.CharField(blank=True, max_length=16)
  created     = models.DateTimeField(auto_now_add=True)
  modified    = models.DateTimeField(auto_now=True)
  category    = models.ManyToManyField(Category, default="", blank=True)
  #alt_names   = models.OneToOneField(AlternativeName, on_delete=models.CASCADE, default="", blank=True)
  #broadcaster= models.ForeignKey(Broadcaster, verbose_name='Broadcaster', on_delete=models.SET_DEFAULT, default="", blank=True, null=True)

  def get_absolute_url(self):
    return reverse('channel-detail', args=[str(self.slug)])
    #return reverse('channel-detail', kwargs={'id': int(self.id)})

  def __str__(self):
    return self.name

  def get_siteinis(self):
    return len(self.siteinis.all())

  get_siteinis.short_description = 'Total siteinis'

  def get_timeshifts(self):
    return len(Timeshifts.objects.filter(parent=self))

  get_timeshifts.short_description = 'Timeshifts'

  class Meta: 
    ordering = ['-name']
    verbose_name_plural = '          Channels'

class AlternativeName(models.Model):
  channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
  name    = models.CharField(max_length=64, blank=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = 'Alternative channel names'


class Timeshifts(models.Model):
  enabled  = models.BooleanField(default=True)
  name     = models.CharField(max_length=32)
  xmltv_id = models.CharField('Channel id in XMLTV', max_length=32)
  offset   = models.IntegerField('Offset in hours', default=1)
  parent   = models.ForeignKey(Channel, on_delete=models.CASCADE)
  
  def __str__(self):
    return self.name
  
  class Meta: 
    ordering = ['offset']
    verbose_name_plural = '         Timeshifted channels'

class Epg(models.Model):
  channel   = models.ForeignKey(Channel, on_delete=models.CASCADE)
  start     = models.CharField(max_length=20)
  stop      = models.CharField(max_length=20)
  title     = models.CharField(max_length=1024)
  sub_title = models.CharField(max_length=1024, blank=True)
  ori_title = models.CharField(max_length=1024, blank=True)
  date      = models.CharField(max_length=20, blank=True)
  category  = models.CharField(max_length=1024, blank=True)
  episode   = models.CharField(max_length=128, blank=True)
  rating    = models.CharField(max_length=128, blank=True)
  subtitles = models.CharField(max_length=128, blank=True)
  audio     = models.CharField(max_length=128, blank=True)
  credits   = models.TextField(blank=True)
  desc      = models.TextField(blank=True)



class Grabbers(models.Model):
  channel  = models.ForeignKey(Channel, on_delete=models.CASCADE)
  siteini  = models.ForeignKey(Siteini, on_delete=models.CASCADE)
  site_id  = models.CharField(blank=True, max_length=32)
  enabled  = models.BooleanField(default=True)
  order    = models.IntegerField(default=1)

  def __str__(self):
    return '%s:%s' % (self.siteini, self.site_id)

  class Meta:
    verbose_name = "Siteini grabber"
    verbose_name_plural = "Grabbers"

class Modes(models.Model):
  name = models.CharField(max_length=16);
  def __str__(self):
    return self.name

class Settings(models.Model):
  name          = models.CharField('Configuration name', max_length=256, 
                                      help_text='Name of the current configuration set to distinguish between multiple configurations')
  filename      = models.CharField('Output file name', default='epg.xml', max_length=32, 
                                      help_text='Name of the xtml file that will be generated')
  update        = models.CharField('Update type', default="", max_length=1, choices=UPDATE_TYPES, blank=True, 
                                      help_text='Global update behaviour. Leave empty so evey channels uses its own update value')
  logging       = models.BooleanField('Enable logging', default=True,
                                         help_text='Change Webgrab logging behavior')
  timespan      = models.IntegerField('Days to grab', default=0, 
                                         help_text='The first is the number of days (including today) to download, note that 0 is today.')
  hours         = models.CharField("One show hour (debug)", max_length=5, blank=True, 
                                      help_text='HH:mm time which will reduce the grab to only the one show (per day)')
  keeppastdays  = models.IntegerField('Keep last N days', blank=True, default=0, null=True,
                                         help_text='Retain the epg of a number of past days')
  skip          = models.CharField(default='noskip', max_length=10, 
                                      help_text='Available values: H,m or noskip')
  mode          = models.ManyToManyField(Modes, default='n', verbose_name='Modes')
  grab          = models.BooleanField("Grab", default=True, 
                                         help_text='Specifies if the EPG grabbing is run first')
  run           = models.BooleanField("Run", default=False, 
                                         help_text='Specifies if a post process is run')
  type          = models.CharField("Type", default="mdb", max_length=3, choices=POSTPROCESS_TYPES, 
                                      help_text='The name of the process to run. "mdb" or "rex"')
  max_retries   = models.IntegerField("Max retries", default=6, 
                                         help_text='Number of times the engine will retry to capture a page')
  retry_timeout = models.IntegerField("Time between retries", default=10, 
                                         help_text='Delay between retries')
  channeldelay  = models.IntegerField("Channel delay", default=0, 
                                         help_text='Delay between grabbing of subsequent channels')
  indexdelay    = models.IntegerField("Index delay", default=0, 
                                         help_text='Delay between grabbing of index pages')
  showdelay     = models.IntegerField("Show delay", default=0, 
                                         help_text='Delay between grabbing of detail show pages')
  proxy_server  = models.CharField(default="", max_length=256, blank=True, 
                                      help_text='Proxy server address:port or "automatic" ')
  proxy_user    = models.CharField(default="", max_length=16, blank=True, 
                                      help_text='The user name needed by the proxy')
  proxy_pass    = models.CharField(default="", max_length=16, blank=True, help_text='The password needed by the proxy')
  useragent     = models.CharField(blank=True, max_length=512, help_text='Add any user-agent or just \'random\' and the program will generate a random string')
  

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "Configurations"
    verbose_name_plural = "      WebGrab Configurations"


class Scheduler(models.Model):
  name          = models.CharField('Name of the scheduler', default='Default scheduler', max_length=256)
  settings      = models.ForeignKey(Settings, on_delete=models.CASCADE, help_text='Select webgrab configuration')
  start_time    = models.CharField(max_length=5, default="05:00")
  run_interval  = models.IntegerField('Run every N days', default=1)
  instances     = models.IntegerField('Number of processes', default=1, 
                                         help_text='The maximum number of WebGrab processes running at the same time')
  timeout       = models.IntegerField('Process timeout', default=40, help_text='Minutes to wait before killing the WebGrab process')
  convert_times = models.BooleanField('Convert times to local time', default=True)
  remove_empty  = models.BooleanField('Remove channels with no programmes', default=True)
  only_title    = models.BooleanField('Copy only title of timeshifted channels', default=True)
  report        = models.BooleanField('Generate report file', default=True)

  
  def __str__(self):
    return self.name

  class Meta:
    verbose_name = "Grabbing Schedulers"
    verbose_name_plural = "     Grabbing Schedulers"