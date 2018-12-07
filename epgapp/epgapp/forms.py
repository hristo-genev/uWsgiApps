"""
Definition of forms.
"""

from django import forms
from epgapp.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class SettingsForm(ModelForm):
  class Meta:
    model = Settings
    fields = '__all__'


#from django.forms.models import inlineformset_factory
#GrabbersForm = inlineformset_factory(Channel, Grabbers, extra=1)