"""job_recommend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job_recommend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name="homepage"),
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('upload/', views.upload_pdf, name="upload"),
    path('results/', views.show_results, name="results"), 
    path('resumes/', views.resumes, name="resumes"),
    path('resumes/<int:id>', views.resume_detail),  
    path('edit/', views.edit_request, name="edit"),
    path('resultserror/', views.results_error, name="resultserror")
]
