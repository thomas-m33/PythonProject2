from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .utils import logout_all_sessions
from two_factor.views import LoginView
from django_otp import devices_for_user

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in.')
            return redirect('two_factor:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()

            profile = p_form.save(commit=False)
            profile.save()

            # save trusted users manually
            users = p_form.cleaned_data["trusted_users"]
            profile.trusted_users.set(users)

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

        initial = {
            "trusted_users": "\n".join(
                request.user.profile.trusted_users.values_list("username", flat=True)
            )
        }

        p_form = ProfileUpdateForm(
            instance=request.user.profile,
            initial=initial
        )

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

class LoginViewFor2FA(LoginView):
    def done(self, form_list, **kwargs):
        response = super().done(form_list, **kwargs)
        user = self.request.user
        has_2fa = any(devices_for_user(user, confirmed=True)) # checks if the user has 2FA set up through any method
        if has_2fa:
            return redirect('blog-home')
        else:
            return redirect('two_factor:profile') # user is prompted to set up 2FA if they don't have it enabled

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    def form_valid(self, form):
        response = super().form_valid(form)
        logout_all_sessions(self.user, current_session_key=self.request.session.session_key)   # invalidate all existing sessions
        return response