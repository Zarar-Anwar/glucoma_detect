from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreation
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import DescriptionForm, ImagesForm
from .models import Images, AI_Response
import tensorflow as tf
import os
from tensorflow import keras
from django.views.generic import View
from .decorators import user_required, doctor_required
from django.conf import settings
from keras.preprocessing import image
from keras.applications.resnet import preprocess_input
import numpy as np

#____________________
import os
import tensorflow as tf
from django.shortcuts import redirect
from django.conf import settings
from .models import Images
from .forms import ImagesForm
from xgboost import XGBClassifier
import numpy as np
from tensorflow.keras.applications import DenseNet201
#____________________


# Website----------------------------------------------------------------------------->

def home(request):
    images = Images.objects.all()
    records = None

    if request.user.is_authenticated:
        records = AI_Response.objects.filter(user=request.user.id)

    context = {"images": images, "records": records}
    template_name = "website/home.html"
    return render(request, template_name, context)


def website_about(request):
    template_name = 'website/about.html'
    return render(request, template_name)


class Test(View):
    def get(self, *args, **kwargs):
        image = get_object_or_404(Images, id=self.kwargs['id'])
        context = {
            'image': image,
            'result': self.kwargs['result'],
            'value': self.kwargs['value']
        }
        return render(self.request, template_name="website/user_test.html", context=context)

    def post(self, *arg, **kwargs):
        if self.request.method == "POST":
            image = get_object_or_404(Images, id=self.kwargs['id'])
            ai_response = AI_Response(
                image=image.image,
                result=self.kwargs['result'],
                value=self.kwargs['value'],
                user=self.request.user,
                doctor=None
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
                    messages.success(request, "Login SuccessFully")
                    if (user.is_user):
                        return HttpResponseRedirect("/")
                    else:
                        return HttpResponseRedirect("/doctor/dashboard/")
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
        user = fm.save(commit=False)
        user.is_user = True
        user.save()
        messages.success(request, "Registered SuccessFully")
        return redirect('user-login')
    template_name = 'website/user_signup.html'
    context = {"form": fm}
    return render(request, template_name, context)


def doctor_signup(request):
    fm = UserCreation(request.POST or None)
    if fm.is_valid():
        user = fm.save(commit=False)
        user.is_doctor = True
        user.save()
        messages.success(request, "Registered SuccessFully")
        return redirect('user-login')
    template_name = 'website/doctor_signup.html'
    context = {"form": fm}
    return render(request, template_name, context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login/')


@user_required
def records_delete(request):
    if request.method == 'POST':
        messages.success(request, "Records Deleted")
        AI_Response.objects.filter(user=request.user.id).delete()
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("login")


# AI-MODEL---------------------------------------------------------------------------->

current_dir = os.path.dirname(os.path.realpath(__file__))

model_path = os.path.join(current_dir, "xgboost_model_150x150.model")
# Load your saved XGBoost model
xgb_model = XGBClassifier()
xgb_model.load_model(model_path)

# Create a pre-trained DenseNet201 model to extract features
base_model = DenseNet201(weights='imagenet', include_top=False, input_shape=(150, 150, 3))

@user_required
def image_detection(request):
    form = ImagesForm(request.POST or None, request.FILES)
    if form.is_valid():
        image1 = form.cleaned_data['image']
        new_image = Images(image=image1)
        new_image.save()
        image_url = settings.MEDIA_URL + str(new_image.image)

        relative_image_url = image_url
        image_id = new_image.id
        print("Image id", image_id)
        absolute_image_path = f'{current_dir}{relative_image_url}'
        print(absolute_image_path)

        if os.path.exists(absolute_image_path):
            img = tf.io.read_file(absolute_image_path)
            img = tf.image.decode_jpeg(img, channels=3)
            img = tf.image.resize(img, [150, 150])  # Resize to match the input size of the model
            img = np.array(img)
            img = img / 255.0
            img = np.expand_dims(img, axis=0)
            features = base_model.predict(img)

            # Reshape the features for XGBoost (2D matrix)
            features = features.reshape(features.shape[0], -1)

            # Make probability predictions using the XGBoost model
            probabilities = xgb_model.predict_proba(features)

            # Define class labels
            # predicted_class = class_names[predictions[0]]

            # Assuming 1 indicates Glaucoma and 0 indicates Non-Glaucoma
            glaucoma_probability = probabilities[0, 1]

            if glaucoma_probability > 0.5:
                predicted_class = "Glaucoma [Positive]"
            else:
                predicted_class = "Non-Glaucoma [Negative]"

            return redirect("test", value=str(glaucoma_probability), result=str(predicted_class), id=image_id)
        else:
            print("File does not exist")

    return HttpResponseRedirect("/")
