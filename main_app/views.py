from io import BytesIO
from django.forms.models import BaseModelForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from main_app.models import Operation,Reservation,Payment,Equipment
from main_app.forms import OperationForm,PaymentForm,ReservationForm,AddFarmerForm,ProfileForm,UpdateFarmerForm,EquipmentForm,UpdatePaymentForm
from authentication.models import FarmerLandInformation,User,Farmer
from django.db.models import Sum
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
from irrigation_core.settings import BASE_DIR
from django.http import JsonResponse
from .decorators import logged_in_redirect,not_logged_in_redirect


def is_staff_or_superuser(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@not_logged_in_redirect
@login_required(login_url=reverse_lazy('farmer_portal'))
def map_view(request):
    context = {}

    land_information = FarmerLandInformation.objects.exclude(barangay__isnull=True,long__isnull=True,lat__isnull=True)
    
    geojson_data = {
        "type": "FeatureCollection",
        "features": []
    }


    for land_info in land_information:
        feature = {
            "type": "Feature",
            "properties": {
                "title": f"{land_info.user.first_name} {land_info.user.last_name}",
                "description": f"<strong>Land Owner: </strong> {land_info.user.first_name} {land_info.user.last_name} <br> <strong>Address: </strong> {land_info.municipality}, {land_info.province} <br> <strong>Barangay: </strong> {land_info.barangay} <br> <strong>Municipality: </strong> {land_info.municipality} <br> <strong>Provice: </strong> North Cotabato <br> <strong>Land Longitude: </strong> {land_info.long} <br> <strong>Land Latitude: </strong> {land_info.lat}",
            },
            "geometry": {
                "type": "Point",
                "coordinates": [land_info.long, land_info.lat]
            }
        }

        geojson_data["features"].append(feature)

    context['geomap_data'] = geojson_data
    
    return render(request,'map.html',context)

@not_logged_in_redirect
@login_required(login_url=reverse_lazy('farmer_portal'))
def generate_reports_filter_by_date_view(request):
    context = {}
    if request.method == "POST":
        current_date = request.POST.get('current_date', None)
        future_date = request.POST.get('future_date', None)
        payments = Payment.objects.filter(date_added__date__range=[current_date,future_date]).order_by('-reservation__equipment__eqiupment_name')

        if payments.count() > 0:
            current_date_obj = datetime.strptime(current_date, "%Y-%m-%d")
            future_date_obj = datetime.strptime(future_date, "%Y-%m-%d")


            fromdate = current_date_obj.strftime("%B %d")
            todate = future_date_obj.strftime("%B %d %Y")

            context['data_date'] = payments
            context['current_date'] = f'{str(fromdate)} - {str(todate)}'

            return render(request,"pdf_templates/filter_by_date_payment.html",context)
        else:
            messages.error(request,f"At the moment there is no payments ranges to the following dates {current_date} - {future_date} found in your records, you can try it again.",extra_tags="no_payments_date")
            return redirect(reverse_lazy('report'))


@not_logged_in_redirect
@login_required(login_url=reverse_lazy('farmer_portal'))
def generate_reports_view(request):
    context = {}
    current_date = datetime.now()
    context['current_date'] = current_date.strftime("%B, %d, %Y")
    if request.method == 'POST':
        report_type = request.POST.get('report_type', None)
        if report_type == '1':
            context['fullpaid'] = Payment.objects.filter(payment_type='FULL PAID').order_by('-reservation__equipment__eqiupment_name')
            return render(request,'pdf_templates/fullpaid.html',context)
        elif report_type == '2':
            context['halfpaid'] = Payment.objects.filter(payment_type='HALF PAID').order_by('-reservation__equipment__eqiupment_name')
            return render(request, 'pdf_templates/halfpaid.html',context)
        elif report_type == '3':
            context['all_payment'] = Payment.objects.all().order_by('-reservation__equipment__eqiupment_name')
            return render(request, 'pdf_templates/all_payment.html',context)

    return HttpResponse('Invalid request, please try again')

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class AddOperation(CreateView):
    model = Operation
    form_class = OperationForm
    template_name = 'add_templates/create_operation.html'
    success_url = '/main/operation/'


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Operation added successfully!',extra_tags="add_operation")
        return response

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class AddPayment(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'add_templates/create_payment.html'
    success_url = '/main/payment/'
    
    def form_valid(self, form):

        reservation = form.instance.reservation.reservation_id
        checkPayment = Payment.objects.filter(reservation=reservation).exists()

        if checkPayment:
            messages.success(self.request, 'Payment already existed with the reservation you choose, no operation being process.',extra_tags="existing_payment")
            return redirect('/main/payment/')
        else:
            response = super().form_valid(form)

            messages.success(self.request, 'Payment added successfully & The reservation is now marked as "OPERATION DONE"!',extra_tags="add_payment")
            return response

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class AddReservation(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'add_templates/create_reservation.html'
    success_url = '/main/reservation/'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Reservation added successfully!',extra_tags="add_reservation")
        return response

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class AddUserView(CreateView):
    model = Farmer
    form_class = AddFarmerForm
    template_name = 'add_templates/create_user.html'
    success_url = '/main/users/'


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User added successfully!',extra_tags="add_user")
        return response

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class AddEquipmentView(CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'add_templates/create_equipment.html'
    success_url = reverse_lazy('add_equipment')


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Equipment has added successfully!',extra_tags="add_equipment")
        return response
###################################################################

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class UpdateUserView(View):
    def get(self,request,pk):
        context = {}
        user_instance = Farmer.farmer.get(id=pk)
        context['form'] = UpdateFarmerForm(instance=user_instance)
        return render(request,"update_templates/update_farmer.html",context)
    
    def post(self,request,pk):
        context = {}
        user_instance = User.objects.get(id=pk,role=Farmer.Role.FARMER)
        update_form = UpdateFarmerForm(request.POST,instance=user_instance)

        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'User updated successfully!',extra_tags="edit_user")
            return HttpResponseRedirect(reverse_lazy('farmer'))

        context['form'] = UpdateFarmerForm(instance=user_instance)
        return render(request,"update_templates/update_farmer.html",context)
    
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class UpdateOperation(UpdateView):
    model = Operation
    form_class = OperationForm
    template_name = 'update_templates/update_operation.html'
    success_url = '/main/operation/'
    pk_url_kwarg = 'pk'


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Operation updated successfully!',extra_tags="edit_operation")
        return response

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class UpdatePayment(UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'update_templates/update_payment.html'
    success_url = '/main/payment/'
    pk_url_kwarg = 'pk'

    def form_valid(self, form):

        payment_obj = Payment.objects.get(payment_id=self.object.pk)  
        associated_reservation = payment_obj.reservation.reservation_id

        if associated_reservation != form.instance.reservation.reservation_id:
            messages.success(self.request, 'The associated reservation on this particular payment is incorrect base on our record, no process has been made.', extra_tags="edit_payment_wrong_id")
            return redirect('/main/payment')
        else:

            if form.instance.payment_type == 'FULL PAID':
                reservation_obj = Reservation.objects.get(reservation_id=form.instance.reservation.reservation_id)
                reservation_obj.payment_status = 'FULLY PAID'

                reservation_obj.save()
            elif form.instance.payment_type == 'HALF PAID':
                reservation_obj = Reservation.objects.get(reservation_id=form.instance.reservation.reservation_id)
                reservation_obj.payment_status = 'HALF PAID'
                reservation_obj.save()

            form.instance.save()     
            messages.success(self.request, f'Payment updated successfully with the payment status {reservation_obj.payment_status}!', extra_tags="edit_payment")
            return super().form_valid(form) 

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class UpdateReservation(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'update_templates/update_reservation.html'
    success_url = '/main/reservation/'
    pk_url_kwarg = 'pk'


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Reservation updated successfully!',extra_tags="edit_reservation")
        return response


###################################################################
@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class DeleteOperation(DeleteView):
    model = Operation
    template_name = 'delete_templates/delete_operation.html'
    success_url = '/main/operation/'


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Operation deleted successfully!',extra_tags="delete_operation")
        return response

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class DeletePayment(DeleteView):
    model = Payment
    template_name = 'delete_templates/delete_payment.html'
    success_url = '/main/payment/'


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Payment deleted successfully!',extra_tags="delete_payment")
        return response

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class DeleteReservation(DeleteView):
    model = Reservation
    template_name = 'delete_templates/delete_reservation.html'
    success_url = '/main/reservation/'


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Reservation deleted successfully!',extra_tags="delete_reservation")
        return response
    
@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class DeleteUserView(DeleteView):
    model = Farmer
    template_name = 'delete_templates/delete_users.html'
    success_url = '/main/users/'


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User deleted successfully!',extra_tags="delete_user")
        return response

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class DeleteEquipmentView(DeleteView):
    model = Equipment
    template_name = 'delete_templates/delete_equipment.html'
    success_url = reverse_lazy('equipment')


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Equipment has been deleted successfully!',extra_tags="delete_equipment")
        return response

###################################################################

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class DashboardView(View):
    def get(self,request):
        context = {}
        context['latest_reservation'] = Reservation.objects.all()

        context['count_reservation'] = Reservation.objects.all().count()
        context['count_schedule'] = Reservation.objects.all().count()
        context['count_farmer'] = Farmer.farmer.all().count()
        context['total_income'] = Payment.objects.filter(payment_type="FULL PAID").aggregate(Sum('payment_amount'))['payment_amount__sum']
        context['total_balance'] = Payment.objects.filter(payment_type="HALF PAID").aggregate(Sum('balance'))['balance__sum']
        return render(request,"dashboard.html",context)

    def post(self,request):
        context = {}
        
        return render(request,"dashboard.html",context)

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class OperationView(View):
    def get(self,request):
        context = {}
        context['operations'] = Operation.objects.all()
        return render(request,"operation.html",context)

    def post(self,request):
        context = {}

        return render(request,"operation.html",context)

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class ReservationView(View):
    def get(self,request):
        context = {}
        context['reservation'] = Reservation.objects.all()
        return render(request,"reservation.html",context)

    def post(self,request):
        context = {}

        return render(request,"reservation.html",context)

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class PaymentView(View):
    def get(self,request):
        context = {}
        context['payments'] = Payment.objects.all()
        context['total_income'] = Payment.objects.filter(payment_type="FULL PAID").aggregate(Sum('payment_amount'))['payment_amount__sum']
        context['total_balance'] = Payment.objects.filter(payment_type="HALF PAID").aggregate(Sum('balance'))['balance__sum']

        return render(request,"payment.html",context)

    def post(self,request):
        context = {}

        return render(request,"payment.html",context)

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class ReportView(View):
    def get(self,request):
        context = {}
        context['payments'] = Payment.objects.all()
        context['total_income'] = Payment.objects.filter(payment_type="FULL PAID").aggregate(Sum('payment_amount'))['payment_amount__sum']
        context['total_balance'] = Payment.objects.filter(payment_type="HALF PAID").aggregate(Sum('balance'))['balance__sum']

        return render(request,"report.html",context)

    def post(self,request):
        context = {}

        return render(request,"report.html",context)

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class FarmerView(View):
    def get(self,request):

        count_active = User.objects.filter(is_active=True).count()

        context = {}

        if count_active > 0:
            context['farmer'] = User.objects.filter(role=User.Role.FARMER).order_by('is_active')
        else:
            context['farmer'] = User.objects.filter(role=User.Role.FARMER).order_by('-date_joined')


        return render(request,"users.html",context)

    def post(self,request):
        context = {}

        return render(request,"users.html",context)
    
@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class EquipmentView(View):
    def get(self,request):
        context = {}
        context['equipments'] = Equipment.objects.all()
        return render(request,"equipments.html",context)

    def post(self,request):
        context = {}

        return render(request,"equipments.html",context)

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class UpdateEquipmentView(UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'update_templates/update_equipment.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('edit_equipment')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Equipment has been updated successfully!',extra_tags="update_equipment")
        return response
    
    def get_success_url(self) -> str:
        return reverse_lazy("edit_equipment", kwargs={'pk': self.object.pk})

@method_decorator(not_logged_in_redirect, name='dispatch')
@method_decorator(user_passes_test(is_staff_or_superuser,login_url=reverse_lazy('farmer_portal')),name='dispatch')
class UpdateProfileView(UpdateView):
    model = FarmerLandInformation
    form_class = ProfileForm
    template_name = 'update_templates/update_farmer_profile.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('farmer')


    def get_object(self,queryset=None):
        user_id = self.kwargs.get('pk')
        try:
            obj = FarmerLandInformation.objects.get(user_id=user_id)
        except FarmerLandInformation.DoesNotExist:
            raise Http404("Sorry, Farmer Land Information does not exist for this user")

        return obj

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User Profile updated successfully!',extra_tags="update_userprofile")
        return response

@not_logged_in_redirect
def activate_account(request,pk):
    if request.method == "POST":

        user = User.objects.get(id=request.POST.get('user_id'))
        user.is_active = True
        user.save()
        messages.success(request,f"You have successfully active the account of {user.username}, thank you!",extra_tags="active_account_message")
        return redirect(reverse_lazy('farmer'))
    
@not_logged_in_redirect
def change_payment_value(request):
    if request.method == 'POST':
        reservation_obj = Reservation.objects.get(reservation_id=request.POST.get("reservation"))
        user_reservation = reservation_obj.farmer.id
        user_info = FarmerLandInformation.objects.get(user=Farmer.farmer.get(id=user_reservation))

        if user_info.hectares is not None:
            amount_to_pay = user_info.hectares * 1000
            return JsonResponse({'amount':amount_to_pay})
        else:
            return JsonResponse({'message':'This user does not have a profile information, please try again.','amount':0})
  