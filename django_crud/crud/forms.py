from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import HydroponicSystem, Measurement
from django.utils.timezone import now


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
        return timestamp if timestamp else now()

    def clean_value(self):
        value = self.cleaned_data.get('value')
        sensor = self.cleaned_data.get('sensor')

        if sensor:
            if sensor.sensor_type == "pH":
                if not (0.0 <= value <= 14.0):
                    raise forms.ValidationError("Wartość pH musi być w zakresie od 0 do 14.")

            elif sensor.sensor_type == "temperature":
                if value < -273.15:
                    raise forms.ValidationError("Temperatura nie może być niższa niż -273.15°C.")

        return value
