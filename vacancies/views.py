from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from .models import Company, Vacancy, Specialty


class MainView(TemplateView):
    template_name = 'vacancies/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        context['specialties'] = Specialty.objects.all()
        return context


class ListVacanciesView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Все вакансии"
        return context


class ListSpecialtyView(ListView):
    model = Vacancy
    template_name = 'vacancies/vacancies.html'
    context_object_name = 'vacancies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        spec = get_object_or_404(Specialty, code=self.kwargs['specialty'])
        context['title'] = spec.title
        context['vacancies'] = Vacancy.objects.filter(specialty=spec)
        return context


class ListCompanyView(ListView):
    model = Vacancy
    template_name = 'vacancies/company.html'
    context_object_name = 'vacancies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = get_object_or_404(Company, id=self.kwargs['company_id'])
        context['company'] = company
        context['vacancies'] = Vacancy.objects.filter(company=company)
        return context


class VacancyView(DetailView):
    model = Vacancy
    template_name = 'vacancies/vacancy.html'
    context_object_name = 'vacancy'


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
