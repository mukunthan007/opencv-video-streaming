from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm,UploadFileForm

from django.contrib.auth.decorators import login_required
from .models import UploadFile
from django.contrib import messages


import cv2
import threading
from django.http import StreamingHttpResponse
from django.views.generic import View

class VideoStream(View):
    def __init__(self):
        super().__init__()
        self.thread = None
        self.frame_generator = None

    def get(self, request, *args, **kwargs):  
        print("true")  
        video_id = kwargs.get('video_id')
        file_object = UploadFile.objects.get(id=video_id)
        print(file_object.file)
        file_path = file_object.file
        if self.thread is None or not self.thread.is_alive():
            # Create a new thread for streaming if it doesn't exist or it's not alive
            self.frame_generator = self.stream_video(video_path=file_path)
            
            self.thread = threading.Thread(target=self.stream_video_thread, daemon=True)
            self.thread.start()

        # Return a streaming response
        return StreamingHttpResponse(self.frame_generator, content_type='multipart/x-mixed-replace; boundary=frame')

    def stream_video_thread(self):
        # This function is run in a separate thread
        for frame_data in self.frame_generator:
            yield frame_data  # Yield each frame to the client

    def stream_video(self,video_path):
        cap = cv2.VideoCapture(str(video_path))
        while True:
            ret, frame = cap.read(1024)
            if not ret:
                break

            # Convert frame to JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Convert frame to bytes
            frame_bytes = jpeg.tobytes()

            # Yield the frame bytes to the client
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

        cap.release()

# def background_process():
#     import time
#     print("process started")
#     time.sleep(100)
#     print("process finished")

# def index(request):
#     import threading
#     t = threading.Thread(target=background_process, args=(), kwargs={})
#     t.setDaemon(True)
#     t.start()
#     return HttpResponse("main thread content")


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST,request.FILES)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            return render(request,
    'registration/register_done.html',
    {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
    'registration/register.html',
    {'user_form': user_form})

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user
            uploaded_file.file_name = request.FILES["file"].name
            uploaded_file.save()
            return render(request,'registration/dashboard.html')
    else:
        form = UploadFileForm()
    return render(request, 'registration/dashboard.html', {'form': form})


@login_required
def dashboard(request):
 form = UploadFileForm()
 uploaded_files = UploadFile.objects.filter(user=request.user)
 print(uploaded_files)
 return render(request,
 'registration/dashboard.html',
 {'files': uploaded_files,"form": form})
