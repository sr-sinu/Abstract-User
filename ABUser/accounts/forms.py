from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Questions
import re
from django.core.exceptions import ValidationError
from datetime import date


class DateInput(forms.DateInput):
    input_type = 'date'


class CustomUserCreationForm(UserCreationForm):

    username = forms.CharField(max_length=50)
    emailF = forms.EmailField()
    dob = forms.DateField(widget=DateInput)
    gender = forms.CharField(widget=forms.RadioSelect(choices=[('M', 'male'), ('F', 'female')])
                             )
    phone = forms.CharField(max_length=20, widget=forms.NumberInput(attrs={'class': 'form-control',
                                                                           'placeholder': 'Enter Phone No.'}))
    pic = forms.FileField()

    class Meta:
        model = CustomUser
        fields = ['username', 'emailF', 'dob', 'gender', 'phone', 'pic']

    def clean_dob(self):
        bday = self.cleaned_data["dob"]
        fraud_detect = abs(date.today() - bday)
        if (fraud_detect.days / 365.0) < 18:
            raise forms.ValidationError("Sorry, you cannot create an account, you should be 18 at least",
                                        code="too_young",
                                        )
        return bday

    # def save(self, commit=True):
    #     user = super(CustomUserCreationForm, self).save(commit=False)
    #     if user.profile_pic:  # If the form includes an avatar
    #         user.set_profile_pic()  # Use this bool to check in templates
    #     if commit:
    #         user.save()
    #     return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'dob', 'gender', ]


class CreateQuestionForm(forms.Form):
    Qname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Enter Question'}))
    Qdesc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                         'placeholder': 'Describe Question'}))
    Qcode = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter Code'}))


class CreateAnswerForm(forms.Form):
    Aname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Enter Answer'}))
    Adesc = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                         'placeholder': 'Describe Answer'}))
    Acode = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                         'placeholder': 'Enter Code'}))
