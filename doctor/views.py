from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from website.forms import UserUpdateForm


# @method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'doctor/dashboard.html'


# @method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'doctor/profile.html'


# @method_decorator(login_required, name='dispatch')
class SettingView(View):
    template_name = 'doctor/setting.html'
    form = UserUpdateForm

    def get(self, request):
        form = self.form(instance=request.user)
        return render(request, template_name=self.template_name, context={"form": form})

    def post(self, request):
        form = self.form(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Updated Successfully')
            return redirect('doctor:setting')
        else:
            messages.error(request, "Error While Updating")
            return render(request, template_name=self.template_name, context={"form": form})
