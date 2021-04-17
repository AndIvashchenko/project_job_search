from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .models import Company, Vacancy, Specialty, User
from .forms import ApplicationForm, CompanyForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ApplicationForm
        return context

    @method_decorator(login_required)
    def post(self, request, pk):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user_id = request.user.pk
            application.vacancy_id = pk
            application.save()
            return redirect(reverse('sent_application', kwargs={'pk': pk}))
        self.object = self.get_object()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class SentVacancyView(TemplateView):
    template_name = 'vacancies/sent.html'


class MyCompanyLetStart(LoginRequiredMixin, TemplateView):
    template_name = 'vacancies/company-create.html'

    def get(self, request, *args, **kwargs):
        if Company.objects.filter(owner__pk=request.user.pk):
            return redirect(reverse('mycompany'))
        return super().get(request, *args, **kwargs)


class MyCompanyCreate(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if Company.objects.filter(owner__pk=request.user.pk).first():
            return redirect(reverse('mycompany'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = CompanyForm()
        return render(request, 'vacancies/company-edit.html', {"form": form})

    def post(self, request):
        form = CompanyForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = get_object_or_404(User, pk=request.user.pk)
            company.save()
            messages.success(request, 'Компания создана')
            return redirect(reverse('mycompany'))
        else:
            return render(request, 'vacancies/company-edit.html', {"form": form})


class MyCompanyEdit(LoginRequiredMixin, View):

    def get(self, request):
        company = Company.objects.filter(owner__pk=request.user.pk).first()
        if not company:
            return redirect(reverse('lets_start'))
        form = CompanyForm(instance=company)
        return render(request, 'vacancies/company-edit.html', {"form": form})

    def post(self, request):
        company = Company.objects.filter(owner__pk=request.user.pk).first()
        form = CompanyForm(request.POST, request.FILES, request.user, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.owner = get_object_or_404(User, pk=request.user.pk)
            company.save()
            messages.success(request, 'Информация о компании обновлена')
            return redirect(reverse('mycompany'))
        else:
            return render(request, 'vacancies/company-edit.html', {"form": form})


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ресурс не найден!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера!')
