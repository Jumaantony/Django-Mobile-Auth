from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegistrationForm, VerifyForm
from . import verify
from .decorators import verification_required


# Create your views here.
@login_required
@verification_required
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            verify.send(form.cleaned_data.get('phone'))
            return redirect('core:login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            if verify.check(request.user.phone, code):
                request.user.is_verified = True
                request.user.save()
                return redirect('core:home')
    else:
        form = VerifyForm()
    return render(request, 'verify.html', {'form': form})
