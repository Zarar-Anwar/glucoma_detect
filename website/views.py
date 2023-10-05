
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db.models import Max
from django.contrib import messages
from .forms import DescriptionForm,UserCreation,ImagesForm
from .models import Images, Feedback, AI_Response
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
import tensorflow as tf
import os
from tensorflow import keras
import random
from django.views.generic import View

from .forms import UserLoginForm

# Website----------------------------------------------------------------------------->

# Home
def home(request):
    images = Images.objects.all()
    latest_description_id = Feedback.objects.aggregate(Max('id'))['id__max']
    description=None
    if latest_description_id:
        description = Feedback.objects.get(id=latest_description_id)
    else:
        description = None
    if request.method=="POST":
        messages.success(request,"Result Send to Doctor")
        return render(request, 'website/home.html', {"images": images, "description": description})

    return render(request, 'website/home.html', {"images": images, "description": description})

# About
def website_about(request):
    template_name='website/about.html'
    return render(request,template_name)

class Test(View):
    def get(self, *args, **kwargs):
        image = Images.objects.get(id=self.kwargs['id'])
        context = {
            'image': image,
            'result': self.kwargs['result'],
            'value': self.kwargs['value']
        }
        return render(self.request, template_name="website/user_test.html",context=context)
    def post(self, *args, **kwargs):
        pass


# User-------------------------------------------------------------------------------->

# Login
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
                    return HttpResponseRedirect("/")
        else:
            form = AuthenticationForm()

        template_name = "website/user_login.html"
        context = {"form": form}
        return render(request, template_name, context)

# SignUp
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

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login/')


# View
def doctor(request):
    if request.method=="POST":
        messages.success(request,"Results Send to Doctor")
        template_name='website/home.html'
        return render(request,template_name)
    latest_responses = AI_Response.objects.all().order_by('-id')[:6]
    template_name = 'website/doctor_home.html'
    context = {"responses": latest_responses}
    return render(request, template_name, context)

# Description
def description(request):
    if request.method == "POST":
        form = DescriptionForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            messages.success(request, "Description Send")
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
# @user_required
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