from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views import View
from django.contrib import messages

from .models import Question, QuestionAnswer, QuestionVote, AnswerVote
from .forms import QuestionCreateForm, QuestionAnswerForm
from .utils import filter_question, RankMixin
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

    def get_queryset(self):
        return Question.objects.all()

    def get(self, request, *args, **kwargs):
        context={"object_list" : self.get_queryset()}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        tag = request.POST.get('tag')
        user_search = request.POST.get('user')
        min_date = request.POST.get('min_date')
        print(min_date)
        max_date = request.POST.get('max_date')
        min_rank = request.POST.get('min_rank')
        max_rank = request.POST.get('max_rank')
        questions = filter_question(title,
                                    tag,
                                    user_search,
                                    min_date,
                                    max_date,
                                    min_rank,
                                    max_rank)
        context = {"object_list": questions}

        return render(request, self.template_name, context)


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = self.object.answers.all().filter(parent=None)
        context["form"] = QuestionAnswerForm()
        try:
            question_vote = QuestionVote.objects.get(user=self.request.user,
            voted_parent=self.object)
            context["question_vote"] =  question_vote
        except:
            context["question_vote"] =  'Oy kullanmadınız'
        return context

class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    form_class = QuestionCreateForm

class QuestionRank(RankMixin, View):
    vote_model = QuestionVote

class AnswerCreateView(LoginRequiredMixin, View):

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')

        obj = get_object_or_404(Question, pk=pk)
        return obj

    def post(self, request, *args, **kwargs):
        question = self.get_object()

        form = QuestionAnswerForm(data=request.POST)
        if form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
                #parent_id = int(form.get('parent_id'))
            except:
                parent_id = None

            if parent_id:
                parent_answer = QuestionAnswer.objects.get(id=parent_id)
                if parent_answer:
                    child_answer = form.save(commit=False)
                    child_answer.parent = parent_answer

            question_answer = form.save(commit=False)
            question_answer.question = question
            question_answer.user = self.request.user

            question_answer.save()
            return HttpResponseRedirect(self.get_object().get_absolute_url())
        return reverse("questions:question_detail", kwargs={"pk": question.pk})


class AnswerRank(RankMixin, View):
    vote_model = AnswerVote
