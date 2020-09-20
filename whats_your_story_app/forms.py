from django import forms
from .models import Story_Image

class StoryImageForm(forms.ModelForm):


    class Meta:
        model = Story_Image
        fields = ['story_pic','story_cap']