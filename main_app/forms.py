from django import forms
from main_app.models import Operation,Payment,Reservation,Equipment
from main_app.models import Operation,Reservation,Equipment
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User, Farmer,FarmerLandInformation

# class GenerateReportEquipmentForm(forms.ModelForm):
#     def __init__(self,*args,**kwargs):
#         super(GenerateReportEquipmentForm,self).__init__(*args,**kwargs)
#         self.fields['equipment'].widget.attrs.update({'class':'form-control form-control-md',})
#         self.fields['equipment'].label = "Equipment Name"
#     class Meta:
#         model = Payment
#         fields = ('equipment',)


class OperationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(OperationForm,self).__init__(*args,**kwargs)
        self.fields['operation_name'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Operation Name'})
        self.fields['operation_name'].label = "Operation"
    class Meta:
        model = Operation
        fields = ('operation_name','operation_status','operation_id')
        widgets = {
            'operation_status': forms.Select(attrs={'class':'form-control form-control-md',}),
            'operation_id': forms.Select(attrs={'class':'form-control form-control-md'})
        }

class EquipmentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(EquipmentForm,self).__init__(*args,**kwargs)

    class Meta:
        model = Equipment
        fields = ('eqiupment_name', 'eqiupment_status',)
        widgets = {
            'eqiupment_name': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Equipment Name',}),
            'eqiupment_status': forms.Select(attrs={'class':'form-control form-control-md',})
        }

class PaymentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(PaymentForm,self).__init__(*args,**kwargs)

        self.fields['balance'].required = False
        self.fields['payment_amount'].widget.attrs.update({'class':'form-control form-control-md','readonly':'true'})
        self.fields['balance'].widget.attrs.update({'class':'form-control form-control-md','value':'0'})

    class Meta:
        model = Payment
        fields = ('reservation','payment_amount','balance','payment_type')
        widgets = {
            'reservation': forms.Select(attrs={'class':'form-control form-control-md',}),
            'payment_type': forms.Select(attrs={'class':'form-control form-control-md',}),
        }

class UpdatePaymentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(UpdatePaymentForm,self).__init__(*args,**kwargs)

        self.fields['balance'].required = False
        self.fields['payment_amount'].widget.attrs.update({'class':'form-control form-control-md','readonly':'true'})
        self.fields['balance'].widget.attrs.update({'class':'form-control form-control-md','value':'0'})

    class Meta:
        model = Payment
        fields = ('payment_amount','balance','payment_type')
        widgets = {
            'payment_type': forms.Select(attrs={'class':'form-control form-control-md',}),
        }

class ReservationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ReservationForm,self).__init__(*args,**kwargs)
        self.fields['farmer'].label = "Select Farmer"
        self.fields['schedule'].label = "Select Schedule"
        self.fields['end_date'].label = "Select End Date"
        self.fields['equipment'].label = "Select equipment"
        self.fields['confirmation'].label = "Select Confirmation"

        
    class Meta:
        model = Reservation
        fields = ('farmer', 'schedule','equipment','confirmation','reservation_status','end_date')
        widgets = {
            'farmer': forms.Select(attrs={'class':'form-control form-control-md','placeholder':'Select Farmer'}),
            'end_date': forms.TextInput(attrs={'type':'date','class':'form-control form-control-md'}),
            'schedule': forms.TextInput(attrs={'type':'date','class':'form-control form-control-md'}),
            'equipment': forms.Select(attrs={'class':'form-control form-control-md',}),
            'reservation_status': forms.Select(attrs={'class':'form-control form-control-md',}),
            'confirmation': forms.Select(attrs={'class':'form-control form-control-md',}),
        }

class AddFarmerForm(UserCreationForm):
    def __init__(self,*args,**kwargs):
        super(AddFarmerForm,self).__init__(*args,**kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-md','placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-md','placeholder':'Confirm password'})

    class Meta:
        model = Farmer
        fields = ('username','first_name','last_name','email', 'password1', 'password2', 'gender', 'address', 'mobile')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Username'}),
            'first_name': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Firstname'}),
            'last_name': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Lastname'}),
            'email': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Email address'}),
            'address': forms.Textarea(attrs={'class':'form-control form-control-md','placeholder':'Address','rows':'3'}),
            'gender': forms.Select(attrs={'class':'form-control form-control-md'}),
            'mobile': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Phone Number'}),
        }

class UpdateFarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ('username','first_name','last_name','email','gender', 'address', 'mobile')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Username'}),
            'first_name': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Firstname'}),
            'last_name': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Lastname'}),
            'email': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Email address'}),
            'address': forms.Textarea(attrs={'class':'form-control form-control-md','placeholder':'Address','rows':'3'}),
            'gender': forms.Select(attrs={'class':'form-control form-control-md'}),
            'mobile': forms.TextInput(attrs={'class':'form-control form-control-md','placeholder':'Phone Number'}),
        }

        exclude = ("password1","password2")


class ProfileForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ProfileForm,self).__init__(*args,**kwargs)
        self.fields['lot_number'].label = "Enter lot number"
        self.fields['hectares'].label = "Enter number of hectares"
        self.fields['image'].label = "Upload land image"
        self.fields['long'].label = "Enter farm longitude"
        self.fields['lat'].label = "Enter farm latitude"
        self.fields['lot_number'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Lot Number'})
        self.fields['hectares'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Hectares'})
        self.fields['square_meter'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Lot square meter'})
        self.fields['region'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Region'})
        self.fields['province'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Province'})
        self.fields['municipality'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Municipality'})
        self.fields['barangay'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Barangay'})
        self.fields['image'].widget.attrs.update({'class':'form-control form-control-md',})
        self.fields['long'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Longitude'})
        self.fields['lat'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Latitude'})


    class Meta:
        model = FarmerLandInformation
        fields = ("lot_number","long","lat","hectares","square_meter","region","province","municipality","barangay","image",)

