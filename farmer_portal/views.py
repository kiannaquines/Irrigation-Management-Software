from django.forms.models import BaseModelForm
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main_app.models import Payment,Reservation,Operation,Equipment
from authentication.models import Farmer,FarmerLandInformation,User
from farmer_portal.forms import FarmerReservationForm,FarmerLandInformationForm,FarmerInformationForm
from django.views.generic import UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date,datetime
from django.utils.decorators import method_decorator
from main_app.decorators import user_logged_in_redirect

@user_logged_in_redirect
@login_required(login_url="/")
def equipment_view(request):
    context = {}
    context['equipments'] = Equipment.objects.all()
    return render(request,"equipment.html",context)


@user_logged_in_redirect
@login_required(login_url="/")
def add_reservation(request):
    context = {}
    if request.method == "POST":
        form = FarmerReservationForm(request.POST)
        if form.is_valid():
            
            equipment = Equipment.objects.get(eqiupment_id=request.POST.get('equipment'))
            schedule_date = form.cleaned_data['schedule']

            reservation_check = Reservation.objects.filter(equipment=equipment, schedule=schedule_date)

            if reservation_check.count() > 0:
                messages.success(request,"Your reservation is not successfull because the equipment is already reserved on the schedule you choosed. Please try again a new date. Thank you!",extra_tags="existed_equipment_today_reservation")
                return HttpResponseRedirect(reverse_lazy('my_reservations'))


            reservation = Reservation.objects.create(farmer=Farmer.farmer.get(id=request.user.id),schedule=form.cleaned_data['schedule'],equipment=form.cleaned_data['equipment'],end_date=form.cleaned_data['end_date'])

            reservation.save()
            messages.success(request,"Your reservation has been added.",extra_tags="add_my_reservation")
            return HttpResponseRedirect(reverse_lazy('my_reservations'))
        
    context['form'] = FarmerReservationForm()
    return render(request,"add_reservation.html",context)

@user_logged_in_redirect
@login_required(login_url="/")
def cancel_reservation(request,pk):
    instance = Reservation.objects.get(reservation_id=pk)
    instance.confirmation = Reservation.Status.CANCEL
    instance.save()

    messages.warning(request,"Your reservation has been cancelled.",extra_tags="cancelled_reservation")
    
    return HttpResponseRedirect(reverse_lazy('my_reservations'))

@user_logged_in_redirect
@login_required(login_url="/")
def view_balances(request):
    context = {}
    instance = Farmer.farmer.get(id=request.user.id)

    context['balances'] = Payment.objects.filter(reservation__farmer=instance).all()
    return render(request,"view_balance.html",context)

@method_decorator(user_logged_in_redirect,name='dispatch')
class UpdateReservationView(UpdateView):
    template_name = "update_reservation.html"
    form_class = FarmerReservationForm
    model = Reservation
    success_url = reverse_lazy("my_reservations")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request,"Your profile has been updated successfully.",extra_tags="update_my_reservation")
        return response
    
@method_decorator(user_logged_in_redirect,name='dispatch')    
class UpdateFarmerInfoView(UpdateView):
    template_name = "update_myprofileinfo.html"
    form_class = FarmerInformationForm
    model = User
    success_url = reverse_lazy("my_profile")
    pk_url_kwarg = 'pk'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request,"Your profile has been updated successfully.",extra_tags="update_my_profileinfo")
        return response
    
    def get_success_url(self):
        return reverse_lazy("my_profile", kwargs={'pk': self.object.pk})

@method_decorator(user_logged_in_redirect,name='dispatch')
class DeleteReservationView(DeleteView):
    template_name = "delete.html"
    model = Reservation
    success_url = reverse_lazy("my_reservations")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        messages.success(self.request,"Your reservation has been deleted successfully.",extra_tags="delete_my_reservation")
        return response
    
@method_decorator(user_logged_in_redirect,name='dispatch')
class UpdateFarmerLandInformationView(UpdateView):
    model = FarmerLandInformation
    template_name = "update_info.html"
    form_class = FarmerLandInformationForm
    success_url = reverse_lazy('my_profile')
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        user_id = self.request.user.id
        try:
            obj = FarmerLandInformation.objects.get(user_id=user_id)
        except FarmerLandInformation.DoesNotExist:
            raise Http404("Sorry, Farmer Land Information does not exist for this user")

        return obj

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request,"You have successfully updated your profile information.",extra_tags="update_my_profile")
        return response
    
    def get_success_url(self):
        return reverse_lazy("my_profile", kwargs={'pk': self.object.pk})
    
@user_logged_in_redirect
def reservations(request):
    context = {}
    instance = Farmer.farmer.get(id=request.user.id)
    context['reservations'] = Reservation.objects.filter(farmer=instance)
    return render(request,"reservations.html",context)