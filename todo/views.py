from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView,FormView
from .models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.


class CustomLoginviews(LoginView):
    template_name = 'todo/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterView(FormView):
    template_name = 'todo/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterView,self).form_valid(form)



class taskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'Cop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Cop"] = context['Cop'].filter(user=self.request.user)
        context["count"] = context['Cop'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search') or  ''
        if search_input:
            context['Cop'] = context['Cop'].filter(title__icontains=search_input)
        return context
    

class taskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = 'Task'
    template_name = 'todo/task_cop.html'

class taskCreate(LoginRequiredMixin,CreateView):
    model =Task
    fields = ['title', 'descriptions','complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(taskCreate,self).form_valid(form)



class taskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'descriptions', 'complete']
    success_url = reverse_lazy('tasks')


class taskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'Task'
    success_url = reverse_lazy('tasks')

