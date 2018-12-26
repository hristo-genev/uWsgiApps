from rest_framework import serializers
from .models import *

class GrabbersSerializer(serializers.ModelSerializer):
  name = serializers.ReadOnlyField(source='siteini.name')
  class Meta:
    model    = Grabbers
    ordering = ['-order']
    fields   = ['name', 'site_id']

class SiteiniSerializer(serializers.ModelSerializer):
  class Meta:
    model  = Siteini
    fields = '__all__'

class TimeshiftsSerializer(serializers.ModelSerializer):
   class Meta:
    model  = Timeshifts
    fields = [ 'name', 'xmltv_id', 'offset', 'enabled']

class ChannelSerializer(serializers.ModelSerializer):
  siteinis   = GrabbersSerializer(source='grabbers_set', many=True)
  timeshifts = TimeshiftsSerializer(source='timeshifts_set', many=True)
  class Meta:
    model  = Channel
    fields = [ 'name', 'xmltv_id', 'update', 'siteinis', 'timeshifts' ]

#class CategorySerializer(serializer.ModelSerializer):
#  class Meta:
#    meta = Category
#    fields = ['name']

#class MapSerializer(serializers.ModelSerializer):
#  timeshifts = TimeshiftsSerializer(source='timeshifts_set', many=True)
#  category = CategorySerializer(source='category_set', many=True}
#  class Meta:
#    model = Channel
#    fields = ['name', 'xmltv_id', 'category', 'timeshifts']

class SingleSiteiniSerializer(serializers.Serializer):
  name = serializers.CharField(max_length=200)
  site_id  = serializers.CharField(max_length=512)

class SingleChannelSerializer(serializers.Serializer):
  name  = serializers.CharField(max_length=200)
  xmltv_id  = serializers.CharField(max_length=200)
  update  = serializers.CharField(max_length=1)
  siteinis  = SingleSiteiniSerializer(many=True)


class ModesSerializer(serializers.ModelSerializer):
  class Meta:
    model  = Modes
    fields = [ 'name' ]

class SettingsSerializer(serializers.ModelSerializer):
  mode        = serializers.SerializerMethodField()
  retry       = serializers.SerializerMethodField()
  proxy       = serializers.SerializerMethodField()
  timespan    = serializers.SerializerMethodField()
  postprocess = serializers.SerializerMethodField()

  class Meta:
    model  = Settings
    fields = ('filename', 'update', 'logging', 'timespan', 'skip', 'mode', 
              'postprocess', 'retry', 'useragent', 'proxy')

  def get_timespan(self, obj):
    return {'days': obj.timespan }#, 'run': obj.run, 'grab': obj.grab }

  def get_postprocess(self, obj):
    return {'type': obj.type, 'run': obj.run, 'grab': obj.grab }

  def get_retry(self, obj):
    return {'channelDelay': obj.channeldelay, 'indexDelay': obj.indexdelay, 'attempts': obj.max_retries, 'timeOut': obj.retry_timeout, 'showDelay': obj.showdelay}

  def get_proxy(self, obj):
    return {'server': obj.proxy_server, 'user': obj.proxy_user, 'password': obj.proxy_pass }

  def get_mode(self, obj):
    names = [mode.name for mode in obj.mode.all()]
    return ",".join(names)
