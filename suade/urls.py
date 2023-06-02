from django.contrib import admin
from django.urls import path
from report_app.views import generate_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('report/', generate_report, name='generate_report'),
]
