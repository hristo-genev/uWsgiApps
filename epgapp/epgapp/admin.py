import requests
from django.contrib import admin
from .models import *
from django.utils.html import format_html

admin.site.site_title = "EpgApp Administration"
admin.site.site_header = "Electronic Program Guide App Administration"

class GrabbersInline(admin.TabularInline):
  model = Grabbers
  extra = 0

admin.site.register(Timeshifts)

class TimeshiftsInline(admin.TabularInline):
  model = Timeshifts
  extra = 0

class AlternativeNameInline(admin.TabularInline):
  model = AlternativeName
  extra = 0

class CategoryAdmin(admin.ModelAdmin):
  search_fields = ['name']
admin.site.register(Category, CategoryAdmin)

class ChannelAdmin(admin.ModelAdmin):
  list_display_links  = [ 'name' ]
  search_fields       = [ 'name', 'category__name' ]
  list_display        = [ 'name', 'xmltv_id', 'slug', 'enabled', 'get_siteinis', 'get_timeshifts' ]
  list_editable       = [ 'xmltv_id', 'slug' ]
  list_filter         = [ 'category' ]
  list_per_page       = 50
  inlines             = [ GrabbersInline, TimeshiftsInline, AlternativeNameInline ]
  prepopulated_fields = {'slug': ('name',)}
  preserve_filters    = True
  autocomplete_fields = [ 'category' ]
  actions             = ['sync_with_playlist', 'batch_enable_channels', 'batch_disable_channels']
  ordering            = ['created']

  def sync_with_playlist(self, request, queryset):
    from .helper import sync_channels_with_playlist
    message = sync_channels_with_playlist(queryset)
    self.message_user(request, message)

  def batch_enable_channels(self, request, queryset):
    from .helper import batch_modify_channels
    message = batch_modify_channels(queryset, 'enable')
    self.message_user(request, message)

  def batch_disable_channels(self, request, queryset):
    from .helper import batch_modify_channels
    message = batch_modify_channels(queryset, 'disable')
    self.message_user(request, message)

  sync_with_playlist.short_description = "Sync with playlist (Enable/Disable channels)"
  batch_enable_channels.short_description = "Enable selected channels"
  batch_disable_channels.short_description = "Disable selected channels"

admin.site.register(Channel, ChannelAdmin)


class SiteiniAdmin(admin.ModelAdmin):
  list_display_links  = ['name', 'slug']
  search_fields       = ['name']
  prepopulated_fields = {'slug': ('name',)}
  list_display        = ('name', 'slug', 'enabled', 'modified', 'created')
  ordering            = ['name']
  list_per_page       = 20


admin.site.register(Siteini, SiteiniAdmin)

MAX_SETTINGS_OBJECTS = 1

class SettingsAdmin(admin.ModelAdmin):
  list_display = ['name', 'show_export_link']
  fieldsets = [
     ('General settings', {'fields': ['name', 'filename', 'update']}),
     ('Timespan settings', {'fields': ['timespan', 'hours', 'keeppastdays']}),
     ('Post processing settings', {'fields': ['type', 'run', 'grab']}),
     ('Retry settings', {'fields': ['max_retries', 'retry_timeout', 'channeldelay', 'indexdelay', 'showdelay']}),
     ('More settings', {'fields': ['logging', 'mode', 'skip', 'useragent'] }),
     ('Proxy settings', {'fields': ['proxy_server', 'proxy_user', 'proxy_pass']}),
     ('Schedule settings', {'fields': ['start_time', 'run_interval', 'instances', 'timeout', 'convert_times', 'remove_empty', 'only_title', 'report']})
  ]

  def get_urls(self):
    urls = super().get_urls()
    custom_urls = [
    #  url(r'^(?P<id>.+)/export/$',
    #    self.admin_site.admin_view(self.process_deposit),
    #    name='account-deposit',),
    ]
    return custom_urls + urls

  def show_export_link(self, obj):
    return format_html('<a href="%s" class="button">Export</a>' % reverse('exported-settings', args=[obj.pk]))
  show_export_link.short_description = 'Export to JSON'

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
  search_fields       = ['channel', 'siteini__name', 'site_id']
  list_per_page       = 20
  list_filter         = ['siteini']
  #autocomplete_fields = ['name']
admin.site.register(Grabbers,GrabbersAdmin)

class SchedulerAdmin(admin.ModelAdmin):
  list_display        = ['name', 'settings', 'start_time', 'run_interval', 'instances']
admin.site.register(Scheduler,SchedulerAdmin)