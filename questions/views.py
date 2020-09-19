from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import View

from .models import Question, QuestionAnswer
from .forms import QuestionCreateForm
from users.models import User


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionCreateForm

    def form_valid(self, form):
        question = form.save(commit=False)
        question.user = self.request.user
        question.save()
        return super().form_valid(form)


class QuestionListView(View):
    template_name = "questions/question_list.html"
    queryset = Question.objects.all()

    def get_queryset(self):
        return self.queryset
    
    def get(self, request, *args, **kwargs):
        context={"object_list":self.get_queryset()}
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.title = self.request.POST.get('title')
        self.tag = self.request.POST.get('tag')
        self.user_search = self.request.POST.get('user')

        questions = Question.objects.filter(Q(title__icontains=self.title) & Q(
            tag__title__icontains=self.tag) & Q(user__username__icontains=self.user_search))

        context = {"object_list": questions}

        return render(request, self.template_name, context)


# class QuestionListView(ListView):
#     model = Question

#     def post(self, request, *args, **kwargs):
#         self.title = self.request.POST.get('title')
#         self.tag = self.request.POST.get('tag')
#         self.user_search = self.request.POST.get('user')
#         print(self.title, self.tag, self.user_search)
#         questions = Question.objects.filter(Q(title__icontains=self.title) & Q(
#             tag__title__icontains=self.tag) & Q(user__username__icontains=self.user_search))
#         print(len(questions))
#         print(questions)
#         return redirect(reverse("questions:question_list"))


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = self.object.answers.all()
        return context


class QuestinUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionCreateForm


class AnswerCreateView(LoginRequiredMixin, CreateView):

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')

        obj = get_object_or_404(Question, pk=pk)
        return obj

    def post(self, *args, **kwargs):
        question = self.get_object()
        question_answer = self.request.POST.get("answer")

        newAnswer = QuestionAnswer(
            question_title=question_answer, user=self.request.user)
        newAnswer.question = question
        newAnswer.save()
        return redirect(reverse("questions:question_detail", kwargs={"pk": question.pk}))
