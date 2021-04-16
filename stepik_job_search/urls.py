"""stepik_job_search URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from accounts.views import MySignupView, MyLoginView, LogoutView
from vacancies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.MainView.as_view(), name='main'),
    path('vacancies', views.ListVacanciesView.as_view(), name='list_vacancies'),
    path('vacancies/cat/<str:specialty>', views.ListSpecialtyView.as_view(), name='specialty_list'),
    path('companies/<int:company_id>', views.ListCompanyView.as_view(), name='company_list'),
    path('vacancies/<int:pk>', views.VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:pk>/send', views.SentVacancyView.as_view(), name='sent_application'),

    path('login', MyLoginView.as_view(), name='login_page'),
    path('logout', LogoutView.as_view(), name='logout_page'),
    path('register', MySignupView.as_view(), name='register_page'),

    path('mycompany/letsstart', views.MyCompanyLetStart.as_view(), name='lets_start'),
    path('mycompany' , views.MyCompany.as_view(), name='mycompany' ),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = views.custom_handler404
handler500 = views.custom_handler500
