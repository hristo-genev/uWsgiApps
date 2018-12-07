import requests
from django.contrib import admin
from .models import *

admin.site.site_title = "EpgApp Administration"
admin.site.site_header = "Electronic Program Guide App Administration"

class GrabbersInline(admin.TabularInline):
  model = Grabbers
  extra = 0

admin.site.register(Timeshifts)

class TimeshiftsInline(admin.TabularInline):
  model = Timeshifts
  extra = 0

class CategoryAdmin(admin.ModelAdmin):
  search_fields = ['name']
admin.site.register(Category,CategoryAdmin)

class ChannelAdmin(admin.ModelAdmin):
  list_display_links  = [ 'name', 'xmltv_id', 'slug' ]
  search_fields       = [ 'name', 'category__name' ]
  list_display        = [ 'name', 'xmltv_id', 'slug', 'enabled', 'get_siteinis', 'get_timeshifts' ]
  list_editable       = [ 'enabled' ]
  list_filter         = [ 'category' ]
  list_per_page       = 50
  inlines             = [ GrabbersInline, TimeshiftsInline ]
  prepopulated_fields = {'slug': ('name',)}
  preserve_filters    = True
  autocomplete_fields = [ 'category' ]
  actions             = ['sync_with_playlist']

  def sync_with_playlist(self, request, queryset):
    from .helper import sync_channels_with_playlist
    message = sync_channels_with_playlist(queryset)
    self.message_user(request, message)

  sync_with_playlist.short_description = "Sync with playlist (Enable/Disable channels)"

admin.site.register(Channel, ChannelAdmin)


class SiteiniAdmin(admin.ModelAdmin):
  search_fields       = ['name']
  prepopulated_fields = {'slug': ('name',)}
  list_display        = ('name', 'enabled', 'modified', 'created')
  ordering            = ['name']
  list_per_page       = 20


admin.site.register(Siteini, SiteiniAdmin)

MAX_SETTINGS_OBJECTS = 1

class SettingsAdmin(admin.ModelAdmin):
  list_display = ['name']
  fieldsets = [
     ('General settings', {'fields': ['name', 'filename', 'update']}),
     ('Timespan settings', {'fields': ['timespan', 'hours', 'keeppastdays']}),
     ('Post processing settings', {'fields': ['type', 'run', 'grab']}),
     ('Retry settings', {'fields': ['max_retries', 'retry_timeout', 'channeldelay', 'indexdelay', 'showdelay']}),
     ('More settings', {'fields': ['logging', 'mode', 'skip', 'useragent'] }),
     ('Proxy settings', {'fields': ['proxy_server', 'proxy_user', 'proxy_pass']}),
     ('Schedule settings', {'fields': ['start_time', 'run_interval', 'instances', 'timeout', 'convert_times', 'remove_empty', 'only_title', 'report']})
  ]

  #def has_add_permission(self, request, obj=None):
  #  if self.model.objects.count() >= MAX_SETTINGS_OBJECTS:
  #    return False
  #  return super().has_add_permission(request)

  def has_delete_permission(self, request, obj=None):
    if self.model.objects.count() == 1:
      return False
    return super().has_delete_permission(request)

admin.site.register(Settings,SettingsAdmin)
#admin.site.register(Modes)

class GrabbersAdmin(admin.ModelAdmin):
  list_display        = ['channel', 'siteini', 'site_id']
  search_fields       = ['channel', 'siteini', 'site_id']
  list_per_page       = 20
  list_filter         = ['siteini']
  #autocomplete_fields = ['name']
admin.site.register(Grabbers,GrabbersAdmin)
