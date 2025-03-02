from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import HydroponicSystem, Measurement


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class HydroponicSystemForm(forms.ModelForm):
    class Meta:
        model = HydroponicSystem
        fields = ['name', 'description']


class MeasurementForm(forms.ModelForm):
    timestamp = forms.DateTimeField(
        required=False,
        widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Measurement
        fields = ['sensor', 'value', 'timestamp']

    def clean_timestamp(self):
        timestamp = self.cleaned_data.get('timestamp')
        if not timestamp:
            from django.utils.timezone import now
            return now()
        return timestamp
