from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = ' Categories'
        app_label = 'freetvandradio'
        
    
    
class Channel(models.Model):
    enabled     = models.BooleanField(default=True)
    name        = models.CharField('Name of channel', max_length=64)
    logo        = models.CharField('Channel logo', blank=True, max_length=1024)
    epg_id      = models.CharField('Channel id in XMLTV', max_length=64)
    slug        = models.SlugField('Slug', max_length=64, unique=True, help_text='Name in URL')
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    category    = models.ManyToManyField(Category, default="", blank=True)
    ordering    = models.IntegerField(default=999)
    
    def get_absolute_url(self):
        return "" #reverse('channel-detail', args=[str(self.slug)])
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = '    Channels'
        app_label = 'freetvandradio'

class User_Agent(models.Model):
    name        = models.CharField('Name', max_length=32)
    string      = models.CharField('String', max_length=512)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'User Agents'
        app_label = 'freetvandradio'
    
class Stream(models.Model):
    channel    = models.ForeignKey(Channel, on_delete=models.CASCADE)
    stream_url = models.CharField('Stream url', blank=True, max_length=1024) 
    page_url   = models.CharField('Page url', blank=True, max_length=1024) 
    player_url = models.CharField('Player url', blank=True, max_length=1024) 
    comment    = models.CharField('Comments', blank=True, max_length=1024)
    preferred  = models.IntegerField('Preference number', default=1, blank=True) 
    enabled    = models.BooleanField(default=True);
    created    = models.DateTimeField(auto_now_add=True)
    modified   = models.DateTimeField(auto_now=True)
    user_agent_id = models.ForeignKey(User_Agent, on_delete=models.CASCADE)
  
    def __str__(self):
        return self.channel.name

    class Meta:
        verbose_name_plural = '  Streams'
        app_label = 'freetvandradio'
