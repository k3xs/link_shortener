import logging
import random
import string
from base64 import b64decode, b64encode

from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, FormView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ShortenLinkForm, RegisterUserForm, LoginUserForm, UserShortenLinkForm, FeedbackForm
from .models import Links

log = logging.getLogger(__name__)


def url_redirect(request, slugs, is_free=False):
    if is_free:
        original_url = b64decode(slugs.encode()).decode()
    else:
        data = Links.objects.get(shorten_url=slugs)
        original_url = data.original_url
        return redirect(original_url)
    return redirect(original_url)


class IndexHome(FormView):
    form_class = ShortenLinkForm
    template_name = 'shortener/index.html'
    success_url = reverse_lazy('home')
    title = 'Project URL Shortener'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        data: Links = form.save(commit=False)

        if self.request.user.is_anonymous:
            slug = 'u/' + b64encode(data.original_url.encode()).decode()
            shorten_url = reverse('redirect', args=[slug])
        else:
            data.shorten_url = ''.join(random.choice(string.ascii_letters) for x in range(10))
            data.user = self.request.user
            data.save()
            shorten_url = data.get_absolute_url()

        context = self.get_context_data()
        context['new_url'] = shorten_url
        return render(self.request, self.template_name, context)


def about(request):
    return render(request, 'shortener/about.html', {'title': 'About site!'})


class CreateShortLink(LoginRequiredMixin, IndexHome):
    login_url = 'login'
    redirect_field_name = login_url

    form_class = UserShortenLinkForm
    template_name = 'shortener/create_short_link.html'
    title = 'Creating short link...'

    def form_valid(self, form):
        data: Links = form.save(commit=False)
        data.user = self.request.user
        data.save()

        context = self.get_context_data()
        context['new_url'] = data.get_absolute_url()
        return render(self.request, self.template_name, context)

class EditShortLink(LoginRequiredMixin, UpdateView):
    model = Links
    fields = ['shorten_url']
    title = 'Edit link...'
    success_url = reverse_lazy('my_links')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class DeleteShortLink(LoginRequiredMixin, DeleteView):
    model = Links
    context_object_name = 'link'
    title = 'Delete link...'
    success_url = reverse_lazy('my_links')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


class FeedbackFormView(FormView):
    title = 'Feedback page...'
    template_name = 'shortener/feedback.html'
    form_class = FeedbackForm
    success_url = reverse_lazy('feedback_thanks')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


def feedback_thanks(request):
    return render(request, 'shortener/feedback_thanks.html', {'title': 'Thank you!'})


class RegisterUser(CreateView):
    title = 'Registration'
    form_class = RegisterUserForm
    template_name = 'shortener/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        log.info('The user has registered %s', user.username)
        return redirect('home')

    def form_invalid(self, form):
        log.warning('The user was unable to register %s', form.errors.as_data())
        return super().form_invalid(form)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'shortener/login.html'
    title = 'Login'

    def get_success_url(self):
        return reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        log.info('The user has logged in %s', form.cleaned_data['username'])
        return super().form_valid(form)

    def form_invalid(self, form):
        log.warning('The user was unable to log in %s', form.cleaned_data['username'])
        return super().form_invalid(form)


def logout_user(request):
    logout(request)
    return redirect('login')


class MyLinks(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = login_url

    model = Links
    paginate_by = 4
    template_name = 'shortener/my_links.html'
    context_object_name = 'links'
    title = 'My links'

    def get_queryset(self):
        my_links = Links.objects.filter(user=self.request.user)
        return my_links

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found!</h1>')
