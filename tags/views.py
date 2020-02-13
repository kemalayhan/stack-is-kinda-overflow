from .models import Tag


from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DetailView, ListView


class TagListView(ListView):
    model = Tag


class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = self.object.question_set.all()
        return context
    
