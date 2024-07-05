from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordResetForm,PasswordChangeForm
from authentication.models import Farmer,User

class FarmerRegisterForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(FarmerRegisterForm,self).__init__(*args,**kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-xl','placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-xl','placeholder':'Confirm password'})

    class Meta:
        model = Farmer
        fields = ('username', 'email', 'password1', 'password2', 'gender', 'address', 'mobile')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control form-control-xl','placeholder':'Username'}),
            'email': forms.TextInput(attrs={'class':'form-control form-control-xl','placeholder':'Email address'}),
            'address': forms.Textarea(attrs={'class':'form-control form-control-xl','placeholder':'Address','rows':'3'}),
            'gender': forms.Select(attrs={'class':'form-control form-control-xl'}),
            'mobile': forms.TextInput(attrs={'class':'form-control form-control-xl','placeholder':'Phone Number'}),
        }
class PasswordResetForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(PasswordResetForm,self).__init__(*args,**kwargs)
        self.fields['email'].widget.attrs.update({'class':'form-control form-control-xl','placeholder':'Email address'})
        self.fields['mobile'].widget.attrs.update({'class':'form-control form-control-xl','placeholder':'Phone Number'})
    class Meta:
        model = User
        fields = ('email','mobile',)


class SetNewPasswordForm(forms.Form):

    mobile = forms.CharField(widget=forms.HiddenInput())
    email = forms.CharField(widget=forms.HiddenInput())
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-xl','placeholder':'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-xl','placeholder':'Confirm password'}))
    

class FarmerLoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super(FarmerLoginForm,self).__init__(self,*args,**kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-xl','placeholder':'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-xl','placeholder':'Password'})
    class Meta:
        model = Farmer
        fields = ('username','password')