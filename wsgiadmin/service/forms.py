from django import forms
from django.forms.models import ModelForm
from django.utils.translation import ugettext_lazy as _

class PassCheckForm(forms.Form):

    _pwd_min_length = 6

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Password again"), widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        if 'pwd_min_length' in kwargs:
            self._pwd_min_length = kwargs.pop('pwd_min_length')
        super(PassCheckForm, self).__init__(*args, **kwargs)

    def clean_password1(self):
        if not "password1" in self.cleaned_data:
            raise forms.ValidationError(_("You have to put your password into both inputs"))
        if len(self.cleaned_data["password1"]) < self._pwd_min_length:
            raise forms.ValidationError(_("Password needs at least %s chars") % self._pwd_min_length)
        return self.cleaned_data["password1"]

    def clean_password2(self):
        if not ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            raise forms.ValidationError(_("You have to put your password into both inputs"))

        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            raise forms.ValidationError(_("First password isn't equal to second one"))

        return self.cleaned_data["password2"]


class PassCheckModelForm(ModelForm):

    _pwd_min_length = 6

    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(label=_("Password again"), widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        if 'pwd_min_length' in kwargs:
            self._pwd_min_length = kwargs.pop('pwd_min_length')
        super(PassCheckModelForm, self).__init__(*args, **kwargs)

    def clean_password1(self):
        if not "password1" in self.cleaned_data:
            raise forms.ValidationError(_("You have to put your password into both inputs"))
        if len(self.cleaned_data["password1"]) < self._pwd_min_length:
            raise forms.ValidationError(_("Password needs at least %s chars") % self._pwd_min_length)
        return self.cleaned_data["password1"]

    def clean_password2(self):
        if not ("password1" in self.cleaned_data and "password2" in self.cleaned_data):
            raise forms.ValidationError(_("You have to put your password into both inputs"))

        print self.cleaned_data
        if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            raise forms.ValidationError(_("First password isn't equal to second one"))

        return self.cleaned_data["password2"]
