from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from website.forms import UserUpdateForm, DescriptionForm, AI_ResponseForm
from website.models import AI_Response


# @method_decorator(login_required, name='dispatch')
def DashboardView(request):
    if request.method == "POST":
        form = DescriptionForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            ai_response = AI_Response.objects.get(id=request.POST['ai_response_id'])
            ai_response.description = description
            ai_response.doctor = request.user
            messages.success(request, 'Feedback Send')
            ai_response.save()
            return redirect('doctor:dashboard')
    latest_responses = AI_Response.objects.filter(description=None).order_by('-id')
    template_name = 'doctor/dashboard.html'
    context = {"responses": latest_responses}
    print(context)
    return render(request, template_name, context)


def ReportHistoryView(request):
    template_name = 'doctor/doctor_report_history.html'
    ai_responses = AI_Response.objects.filter(doctor=request.user)

    if request.method == "POST":
        form = DescriptionForm(request.POST)
        if form.is_valid():
            instance = None
            if 'ai_response_id' in request.POST:
                instance = AI_Response.objects.get(pk=request.POST['ai_response_id'])

            form = DescriptionForm(request.POST, instance=instance)
            form.save()
            messages.success(request, 'Report Update successfully')
            return redirect('doctor:report-history')
        else:
            context = {'data': ai_responses, 'form': form}
            return render(request, template_name, context)
    else:
        context = {'data': ai_responses}
        return render(request, template_name, context)


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
