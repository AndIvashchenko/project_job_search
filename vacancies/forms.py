from django import forms

from .models import Application, Company


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        labels = {
            'written_username': "Ваше имя",
            'written_phone': "Ваш телефон",
            'written_cover_letter': "Сопроводительное писмо",
        }
        error_messages = {
            'written_phone': {'invalid': 'Неверный формат номера телефона. Используйте "+X XXX XXX XX XX"'}
        }


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields =('name', 'location', 'logo', 'employee_count', 'description')
        labels = {
            'name': "Название компании",
            'description': "Информация о компании",
            'location': "Город",
            'employee_count': "Количество человек в компании",
        }