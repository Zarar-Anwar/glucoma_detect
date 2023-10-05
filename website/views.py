
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
from .decorators import user_required
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
model_path =os.path.join(current_dir,"model","model1.hdf5")
loaded_model = keras.models.load_model(model_path)
test_dir = os.path.join(current_dir, "model", "data", "Testing")
class_names = os.listdir(test_dir)

@user_required
def image_detection(request):
    print("here")
    class_names = ["Positive", "Negative"]
    prediction = None
    form = ImagesForm(request.POST or None, request.FILES)
    if form.is_valid():
        relative_image_url = request.POST.get("image_url")
        image_id = request.POST.get("image_id_name")
        print("Image id", image_id)
        absolute_image_path = f'D:/Projects/glucoma_detect/glucoma_detect{relative_image_url}'

        print(f"Absolute image path: {absolute_image_path}")  # Debugging line

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
            return redirect("test", value=str(prediction[0]), result=str(prediction[1]), id=str(image_id))
        else:
            print("File does not exist")
            # Handle the case where the file does not exist
    messages.success(request, "Image Uploaded")
    return redirect('home')
    return render(request, 'website/home.html', {'form': form, 'prediction': prediction})


# model Handling Logic
def random_image_predictions(request):
    image_predictions = []

    for _ in range(6):
        class_name = random.choice(class_names)
        filenames = os.listdir(os.path.join(test_dir, class_name))

        if not filenames:
            print(f"No image files found in directory: {os.path.join(test_dir, class_name)}")
            continue

        filename = random.choice(filenames)
        filepath = os.path.join(test_dir, class_name, filename)

        if not os.path.exists(filepath):
            print(f"File does not exist: {filepath}")
            continue

        img = tf.io.read_file(filepath)
        img = tf.io.decode_image(img)
        img = tf.image.resize(img, [100, 100])

        pred_prob = loaded_model.predict(tf.expand_dims(img, axis=0))
        pred_class = class_names[pred_prob.argmax()]

        # Save the image file to the media directory
        ai_response = AI_Response(
            image=f'images/{filename}',  # Relative path within 'upload_to' subdirectory
            predicted_class=pred_class,
            probability=round(float(pred_prob.max()), 2)
        )
        ai_response.save()

        # Append data to image_predictions list
        image_predictions.append({
            'actual_class': class_name,
            'predicted_class': pred_class,
            'probability': round(float(pred_prob.max()), 2),
            'image_path': ai_response.image.url,  # Use the image URL
        })

    context = {
        'image_predictions': image_predictions,
    }
    return render(request, 'website/user_test.html', context)
