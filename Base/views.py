from typing import List
from django.db.models import fields
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.urls import reverse_lazy

from .models import Task


def home(request):
    return render(request, 'Base/Home.html', {})

class CustomLoginView(LoginView):
    template_name = "Base/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("task-list")


class UserRegistrationPage(FormView):
    template_name = "Base/register.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(UserRegistrationPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')

        return super(UserRegistrationPage, self).get(*args, **kwargs)



class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            print('init')
            context['tasks'] =  context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input
        # print('above it')
        addNewTask = self.request.GET.get('new-task') or ''
        print(self.request.GET)
        if addNewTask:
            print(f'init task wla {addNewTask}')
            new_task = Task(user=self.request.user, title=addNewTask, complete=False)
            new_task.save()
            addNewTask = None
        # context['tasks'] = context['tasks'].filter(user=self.request.user)
        return context


    def get(self, request, *args, **kwargs):
        temp = super().get(request, *args, **kwargs)
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        # print(context['tasks'])
        return temp


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "tasks"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'complete']
    success_url = reverse_lazy("task-list")
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title','complete']
    success_url = reverse_lazy("task-list")

    def get(self, request, *args, **kwargs):
        object = super().get(request, *args, **kwargs)
        self.object.complete = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())



class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "tasks"
    success_url = reverse_lazy("task-list")
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
    