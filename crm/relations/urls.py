from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('kurumlar/', CompanyApiView.as_view()),
    path('kurumlar/rol/<str:role>/', CompanyByRoleList.as_view()),
    path('kurumlar/<int:pk>/', CompanyApiDetailView.as_view()),
    path('kisiler/', PeopleApiView.as_view()),
    path('kisiler/<int:pk>/', PeopleApiDetailView.as_view()),
    path('firsatlar', ProjectApiView.as_view()),
    path('firsatlar/<int:pk>/', ProjectApiDetailView.as_view()),
    path('urunler/', ProductApiView.as_view()),
    path('notlar/', NotesApiView.as_view()),
    path('notlar/<int:pk>', NotesApiDetailView.as_view()),
    path('veriler/', Statistics.as_view()),
    path('sonlanan/', FinishedProjectApiView.as_view()),
    path('download/<int:pk>', download),
    path('mailer/', MailerView.as_view()),
    path('dosyalar/', FilesView.as_view()),
    path('excel/<int:download_type>', DownloadDatabaseExcel.as_view()),

]