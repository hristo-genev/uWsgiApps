from django.contrib import admin
from freetvandradio.model import *
from django.utils.html import format_html

admin.site.site_title = "Free BG TVs And Radios Administration"
admin.site.site_header = "Free BG TVs And Radios App Administration"


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(Category, CategoryAdmin)


class User_AgentAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(User_Agent, User_AgentAdmin)

class ChannelAdmin(admin.ModelAdmin):
    list_display_links  = ['name']
    search_fields       = [ 'name', 'category__name' ]
    list_display        = [ 'name', 'image_tag', 'epg_id', 'enabled', 'get_streams', 'ordering']
    list_editable       = [ 'ordering' ]
    list_filter         = [ 'category' ]
    #list_per_page       = 50
    prepopulated_fields = {'slug': ('name',)}
    #preserve_filters    = True
    #autocomplete_fields = [ 'category' ]
    ordering            = ['ordering']
    readonly_fields = ('image_tag',)
    
    def image_tag(self, obj):
        return format_html('<img src="{}" height="30" />'.format(obj.logo))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    
    def get_streams(self, obj):
        return 1
    get_streams.short_description = 'Streams'

admin.site.register(Channel, ChannelAdmin)

class StreamAdmin(admin.ModelAdmin):
    list_display_links  = ['get_channel']
    search_fields       = ['get_channel']
    list_display        = ['get_channel', 'stream_url', 'comment', 'enabled', 'preferred']
    list_filter         = ['channel']
    list_editable       = ['stream_url', 'preferred']
    #list_per_page       = 50
    #preserve_filters    = True
    #autocomplete_fields = ['channel']
    
    def get_channel(self, obj):
        return obj.channel.name
    get_channel.short_description = 'Channel'
    get_channel.admin_order_field = 'channel__order'
 
admin.site.register(Stream, StreamAdmin)