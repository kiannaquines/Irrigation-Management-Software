from django import forms
from main_app.models import Reservation
from authentication.models import FarmerLandInformation,Farmer

class FarmerReservationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(FarmerReservationForm,self).__init__(*args,**kwargs)
        self.fields['schedule'].label = "Select Start Date"
        self.fields['end_date'].label = "Select End Date"
        self.fields['schedule'].required = True
        self.fields['equipment'].widget.attrs.update({'class':'form-select form-control-md','required':'true'})

    class Meta:
        model = Reservation
        fields = ("schedule","equipment","end_date")
        widgets = {
            'schedule': forms.TextInput(attrs={'type':'date','class':'form-control form-control-md','required':'true'}),
            'end_date': forms.TextInput(attrs={'type':'date','class':'form-control form-control-md','required':'true'}),
        }


class FarmerLandInformationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(FarmerLandInformationForm,self).__init__(*args,**kwargs)

        self.fields['lot_number'].label = "Enter lot number"
        self.fields['hectares'].label = "Enter number of hectares"
        self.fields['long'].label = "Enter farm longitude"
        self.fields['lat'].label = "Enter farm latitude"
        self.fields['image'].label = "Upload land image"
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



class FarmerInformationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(FarmerInformationForm,self).__init__(*args,**kwargs)

        self.fields['first_name'].label = "Enter your firstname"
        self.fields['last_name'].label = "Enter your lastname"
        self.fields['email'].label = "Enter your email address"
        self.fields['first_name'].widget.attrs.update({'class':'form-control form-control-md'})
        self.fields['last_name'].widget.attrs.update({'class':'form-control form-control-md'})
        self.fields['email'].widget.attrs.update({'class':'form-control form-control-md'})
        self.fields['address'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Address'})
        self.fields['mobile'].widget.attrs.update({'class':'form-control form-control-md','placeholder':'Mobile Number'})


    class Meta:
        model = Farmer
        fields = ("first_name","last_name","email","address","mobile",)