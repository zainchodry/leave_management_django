from django.shortcuts import render, redirect
from . models import *
from . forms import *
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})

class PasswordChangeView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'accounts/password_change.html', {'form': form})

    def post(self, request):
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        return render(request, 'accounts/password_change.html', {'form': form})
    
class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'
    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, 'accounts/profile.html', {'form': form})
    
    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        return render(request, 'accounts/profile.html', {'form': form})
    
@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
