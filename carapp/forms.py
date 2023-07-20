from django import forms
from carapp.models import OrderVehicle


class OrderVehicleForm(forms.ModelForm):
    """ form to get the details about the vehicles ordered, that is OrderVehicle model """
    class Meta:
        model = OrderVehicle
        fields = ['vehicle', 'buyer', 'number_of_Vehicles']
        labels = {
            'number_of_Vehicles': 'Number of Vehicles Ordered',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['buyer'].widget.attrs['size'] = 1

class ContactForm(forms.Form):
    """ form to contact the lab group """
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
