from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from .models import User
from .models import Address
phone_regex  = RegexValidator(
        regex=r'^\+?1?\d{8,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

class MyCustomSignupForm(SignupForm):
    
    first_name = forms.CharField(label=_("First Name"), required=True, widget=forms.TextInput(attrs={'placeholder': _("First Name")}))
    last_name = forms.CharField(label=_("Last Name"), required=True, widget=forms.TextInput(attrs={'placeholder': _("Last Name"), 'class': "form-input form-wide"}))
    # phone_number = forms.CharField(label=_("Phone Number"), required=True,widget=forms.TextInput(attrs={'placeholder': _("Phone Number"), 'class': "form-input form-wide"}), validators=[phone_regex])
    def save(self, request):
    
        user = super(MyCustomSignupForm, self).save(request)
        # user.phone_number = self.cleaned_data['phone_number']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        user.save()


        return user
    


class UserProfileUpdate(forms.ModelForm):
    first_name = forms.CharField(label=_("First Name"), required=True, widget=forms.TextInput(attrs={'placeholder': _("First Name"), 'class': "form-input form-wide"}))
    last_name = forms.CharField(label=_("Last Name"), required=True, widget=forms.TextInput(attrs={'placeholder': _("Last Name"), 'class': "form-input form-wide"}))
    phone_number = forms.CharField(label=_("Phone Number"), required=True,widget=forms.TextInput(attrs={'placeholder': _("Phone Number"), 'class': "form-input form-wide"}), validators=[phone_regex])
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-input form-widel'})) 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email']


class AddNewAddress(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ('user', )