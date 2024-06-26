# Create your views here.
# detector/views.py
import cv2
from skimage.metrics import structural_similarity as ssim
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import UploadedImage
import os

# Resize function
def resize_image(img, width, height):
    return cv2.resize(img, (width, height))

def home(request):
    if request.method == 'POST':
        image = request.FILES['image']
        UploadedImage.objects.create(image=image)
        # Implementation of fake logo detection logic
        uploaded_img_path = os.path.join(settings.MEDIA_ROOT, 'uploads/', image.name)
        # Load the uploaded image
        uploaded_img = cv2.imread(uploaded_img_path)

        if uploaded_img is None:
            raise ValueError(f"Error: Uploaded image not loaded: {uploaded_img_path}")

        # Resize the uploaded image to a consistent size
        resize_width = 100  # Set your desired width
        resize_height = 100  # Set your desired height
        uploaded_img_resized = resize_image(uploaded_img, resize_width, resize_height)
        # Path to the dataset folder containing real logo images
        dataset_folder = os.path.join(settings.MEDIA_ROOT, "real_logos")
        # Iterate through the images in the dataset folder
        for filename in os.listdir(dataset_folder):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                # Construct path for the dataset image
                dataset_img_path = os.path.join(dataset_folder, filename)
                # Load the dataset image
                dataset_img = cv2.imread(dataset_img_path)
                if dataset_img is None:
                    raise ValueError(f"Error: Dataset image not loaded: {dataset_img_path}")
                 # Resize the dataset image to a consistent size
                dataset_img_resized = resize_image(dataset_img, resize_width, resize_height)

                # Calculate SSIM for the pair of images with an explicitly specified window size (e.g., 3x3)
                similarity_index, _ = ssim(uploaded_img_resized, dataset_img_resized, full=True, win_size=3)

                # Set a threshold for the SSIM
                threshold = 0.70  
                if similarity_index > threshold:
                    return render(request, 'home.html', {'images': f"Real logo detected. Similarity: {similarity_index}"})
        return render(request, 'home.html', {'images': "Fake logo detected"})

    images = UploadedImage.objects.all()
    return render(request, 'home.html', {'images': images})

def about(request):
    if request.method == 'GET':
        return render(request, 'about.html')

def contact(request):
    if request.method == 'GET':
        return render(request, 'contact.html')
