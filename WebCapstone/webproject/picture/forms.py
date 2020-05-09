from django import forms
from .models import Image
#
# from .widgets import PreviewFileWidget

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['pic1', 'pic2', 'pic3',]
        #fields = '__all__'
        #
        # widgets = {
        #     'pic1':PreviewFileWidget,
        #     'pic2':PreviewFileWidget,
        #     'pic3':PreviewFileWidget,
        # }