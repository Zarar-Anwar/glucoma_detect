from django import forms
from .models import Images,Feedback,AI_Response


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['image']


class DescriptionForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['description']


class AI_ResponseForm(forms.ModelForm):
    class Meta:
        model=AI_Response
        fields=['image','predicted_class','probability']