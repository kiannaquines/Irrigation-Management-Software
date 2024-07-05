from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import logout,authenticate,login
from authentication.forms import FarmerRegisterForm,FarmerLoginForm,PasswordResetForm,SetNewPasswordForm
from django.contrib import messages
from authentication.models import User,Farmer
from django.contrib.auth.hashers import make_password
from main_app.decorators import logged_in_redirect
from django.utils.decorators import method_decorator


@method_decorator(logged_in_redirect, name='dispatch')
class LoginView(View):
    def get(self,request):
        context = {}

        context['form'] = FarmerLoginForm()
        return render(request,"login.html",context)

    def post(self, request):
        context = {}
        form = FarmerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request,user)

                if user.is_staff and user.is_superuser: 
                    return redirect("dashboard")
                else:
                    myprofileinfo = Farmer.farmer.get(id=user.id)

                    if myprofileinfo.first_name == "" or myprofileinfo.last_name == "":

                        url = reverse("my_profileinfo", args=[user.id])

                        return redirect(url)
                    
                    return redirect("add_my_reservation")
                
            else:
                context['form'] = form
                context['error_messages'] = form.errors

                return render(request, "login.html", context)

        else:
            context['form'] = form
            context['error_messages'] = form.errors
            return render(request, "login.html", context)
        
@method_decorator(logged_in_redirect, name='dispatch')
class RegisterView(View):
    def get(self,request):
        context = {}

        context['form'] = FarmerRegisterForm()
        return render(request,"register.html",context)


    def post(self,request):
        context = {}

        form = FarmerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"You have successfully registered, please wait until your account to be activated.",extra_tags="success_registered")
            return redirect("login")
        else:
            print(form.error_messages)
            context['error_messages'] = form.errors
            context['form'] = form
            return render(request,"register.html",context)

@method_decorator(logged_in_redirect, name='dispatch')
class PasswordResetView(View):
    def get(self,request):
        context = {}
        context['form'] = PasswordResetForm()
        return render(request,"forgot.html",context)

    def post(self,request):
        context = {}

        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        user = User.objects.filter(email=email,mobile=mobile)

        if user.count() > 0:

            return redirect("new_password", email=email, mobile=mobile)

        if email == '' and mobile == '':
            context['empty_fields'] = 'Sorry, provide your detials since fields must not be empty, please try again.'

        context['form'] = PasswordResetForm({'email':email,'mobile':mobile})
        context['user_not_found'] = 'Sorry, we cannot found the information you provided, please try again.'
        return render(request,"forgot.html",context)

@method_decorator(logged_in_redirect, name='dispatch')
class SetNewPasswordView(View):
    def get(self,request,email,mobile):
        context = {}
        context['form'] = SetNewPasswordForm({'email':email,'mobile':mobile})
        return render(request,"reset.html",context)

    def post(self,request,email,mobile):
        context = {}

        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password_new = request.POST.get('new_password')
        password_conf = request.POST.get('confirm_password')
        
        user = User.objects.filter(email=email,mobile=mobile,role=User.Role.FARMER)

        if password_new != password_conf:
            context['password_not_matched'] = 'Sorry, your password does not matched, please try again.'
            context['form'] = SetNewPasswordForm({'email':email,'mobile':mobile})
            return render(request,"reset.html",context)
        
        if user.count() > 0:

            instance = user.first()
            instance.set_password(password_conf)
            print(instance.save())

            messages.success(request,'Congrats, your password has been updated successfully, you can now login.',extra_tags='password_reset_success')

            return redirect('login')

        
        context['user_not_found'] = 'Sorry, we cannot found the information you provided, please try again.'
        context['form'] = SetNewPasswordForm({'email':email,'mobile':mobile})
        return render(request,"reset.html",context)

def logout_view(request):
    logout(request)
    return redirect("login")