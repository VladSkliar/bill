from models import Bill, BillRegion
from django.forms import ModelForm
from django.shortcuts import get_object_or_404


class BillCreationForm(ModelForm):
    class Meta:
        model = Bill
        fields = ('title', 'description', 'contacts',
                  'image', 'region')
