
from django.shortcuts import render, redirect,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreation
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import DescriptionForm,ImagesForm
from .models import Images,AI_Response
import tensorflow as tf
import os
from tensorflow import keras
from django.views.generic import View
from .decorators import user_required,doctor_required
from keras.preprocessing import image
from keras.applications.resnet import preprocess_input
import numpy as np


# Website----------------------------------------------------------------------------->

def home(request):
    images = Images.objects.all()
    records=None

    if request.user.is_authenticated:
        records = AI_Response.objects.filter(userId=request.user.id)

    context={"images":images,"records":records}
    template_name="website/home.html"
    return render(request, template_name, context)

def website_about(request):
    template_name='website/about.html'
    return render(request,template_name)

class Test(View):
    def get(self, *args, **kwargs):
        image = get_object_or_404(Images, id=self.kwargs['id'])
        context = {
            'image': image,
            'result': self.kwargs['result'],
            'value': self.kwargs['value']
        }
        return render(self.request, template_name="website/user_test.html", context=context)

    def post(self,*arg,**kwargs):
        if self.request.method == "POST":
            image = get_object_or_404(Images, id=self.kwargs['id'])
            ai_response = AI_Response(
                image=image.image,
                result=self.kwargs['result'],
                value=self.kwargs['value'],
                userId=self.request.user
            )
            ai_response.save()
            messages.success(self.request, "Report send to Doctor")
            return HttpResponseRedirect('/')



# User-------------------------------------------------------------------------------->

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    else:
        if request.method == "POST":
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request,"Login SuccessFully")
                    if (user.is_user):
                        return HttpResponseRedirect("/")
                    else:
                        return HttpResponseRedirect("/doctor/view/")
            else:
                 messages.error(request, "Invalid Username and Password")
        else:
            form = AuthenticationForm()

        template_name = "website/user_login.html"
        context = {"form": form}
        return render(request, template_name, context)

def user_signup(request):
    fm = UserCreation(request.POST or None)
    if fm.is_valid():
        user =fm.save(commit=False)
        user.is_user=True
        user.save()
        messages.success(request,"Registered SuccessFully")
        return redirect('user-login')
    template_name = 'website/user_signup.html'
    context = {"form": fm}
    return render(request, template_name, context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login/')


# View
@doctor_required
def doctor(request):
    if request.method == "POST":
        form = DescriptionForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            ai_response = AI_Response.objects.get(id=request.POST['ai_response_id'])
            ai_response.description = description
            ai_response.save()
            return redirect('doctor')
    latest_responses = AI_Response.objects.filter(description=None).order_by('-id')
    template_name = 'website/doctor_home.html'
    context = {"responses": latest_responses}
    print(context)
    return render(request, template_name, context)


# Description
@doctor_required
def description(request):
    if request.method == "POST":
        form = DescriptionForm(request.POST)
        if form.is_valid():
            ai_response = AI_Response(
                description=form.cleaned_data['description']
            )
            ai_response.save()
            messages.success(request, "Description Sent")
            return redirect('doctor')
        else:
            messages.error(request, "Invalid Data")
    else:
        form = DescriptionForm()
    return render(request, 'website/doctor_home.html', {'form': form})


# AI-MODEL---------------------------------------------------------------------------->

current_dir = os.path.dirname(os.path.realpath(__file__))

model_path = os.path.join(current_dir,'model1.hdf5')
loaded_model = keras.models.load_model(model_path)
@user_required
def image_detection(request):
    class_names = ["Positive", "Negative"]
    prediction = None
    form = ImagesForm(request.POST or None, request.FILES)
    if form.is_valid():
        relative_image_url = request.POST.get("image_url")
        image_id = request.POST.get("image_id_name")
        print("Image id", image_id)
        absolute_image_path = f'{current_dir}{relative_image_url}'

        if os.path.exists(absolute_image_path):
            img = tf.io.read_file(absolute_image_path)
            img = tf.io.decode_image(img)
            img = tf.image.resize(img, [100, 100])
            img = img / 255.0  # Normalize pixel values (assuming the model expects inputs in [0, 1])

            pred_prob = loaded_model.predict(tf.expand_dims(img, axis=0))
            pred_class_index = pred_prob.argmax()
            predicted_class = class_names[pred_class_index]

            prediction = predicted_class, pred_prob[0][pred_class_index]
            print(prediction)
            print(prediction[0])
            print(prediction[1])
            print(absolute_image_path)
            print(image_id)
            # Assuming image_id is a valid non-empty value
            return redirect("test", value=str(prediction[0]), result=str(prediction[1]), id=image_id)
        else:
            print("File does not exist")
            # Handle the case where the file does not exist
    return HttpResponseRedirect("/")
