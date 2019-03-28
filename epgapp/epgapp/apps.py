from django.apps import AppConfig

class EpgappConfig(AppConfig):
  name = 'epgapp'

  def ready(self):
    #from forecastUpdater import updater
    #updater.start()
    pass
