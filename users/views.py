from django.shortcuts import render, reverse
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from .models import User
from .forms import RegisterForm, UserUpdateForm
from django.views.generic import CreateView, UpdateView, DetailView, ListView


class RegisterView(CreateView):
    model = User
    form_class = RegisterForm
    
    def form_valid(self, form):
        resp = super().form_valid(form)
        user = authenticate(username=form.cleaned_data['username'] , password=form.cleaned_data['password1'])
        login(self.request, user)
        return resp


class UserDetailView(DetailView):
    model = User


class UserListView(ListView):
    model = User


class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm
    

    def get_object(self, queryset=None):
        return self.request.user
    
    # def get_success_url(self):
    #     return reverse_lazy('users:user_detail',  kwargs={"pk" : self.object.id})
    #     #return reverse_lazy("users:user_list")