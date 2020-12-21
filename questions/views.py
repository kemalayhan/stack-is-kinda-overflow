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
    # def post(self, request, *args, **kwargs):
    #     question_pk = self.kwargs.get('pk')
    #     question = Question.objects.get(pk=question_pk) #hangi soru
    #
    #     vote = request.POST.get('question_vote') # increase
    #     if vote is None:
    #         messages.warning(request, 'You didnt select choice of vote')
    #         return HttpResponseRedirect(question.get_absolute_url())
    #
    #     if self.request.user.is_authenticated:
    #         user = self.request.user
    #         question_vote = QuestionVote.objects.filter(question=question, user=user)
    #         if question_vote.exists():
    #             question_vote = question_vote.first()
    #             if question_vote.question_vote == 'draft':
    #                 if vote == 'increase':
    #                     question_vote.question_vote = 'increase'
    #                     question_vote.save()
    #                     question.increase_rank()
    #                     messages.success(request, 'You vote increase')
    #                     return HttpResponseRedirect(question.get_absolute_url())
    #
    #                 if vote == 'decrease':
    #                     question_vote.question_vote = 'decrease'
    #                     question_vote.save()
    #                     question.decrease_rank()
    #                     messages.success(request, 'You vote decrease')
    #                     return HttpResponseRedirect(question.get_absolute_url())
    #
    #             elif question_vote.question_vote == 'increase' and vote == 'decrease':
    #                 question_vote.question_vote = 'draft'
    #                 question_vote.save()
    #                 question.decrease_rank()
    #                 messages.success(request, 'You canceled your old vote')
    #                 return HttpResponseRedirect(question.get_absolute_url())
    #
    #             elif question_vote.question_vote == 'decrease' and vote == 'increase':
    #                 question_vote.question_vote = 'draft'
    #                 question_vote.save()
    #                 question.increase_rank()
    #                 messages.info(request, 'You canceled your old vote')
    #                 return HttpResponseRedirect(question.get_absolute_url())
    #
    #             else:
    #                 messages.warning(request, 'You cant vote')
    #                 return HttpResponseRedirect(question.get_absolute_url())
    #         else:
    #             question_vote = QuestionVote.objects.create(user=user,
    #             question=question,
    #             question_vote=vote)
    #             if vote == 'decrease':
    #                 question.decrease_rank()
    #             else:
    #                 question.increase_rank()
    #             messages.success(request, 'You successfully vote')
    #             return HttpResponseRedirect(question.get_absolute_url())
    #
    #     messages.warning(request, 'You have to login to vote')
    #     return HttpResponseRedirect(question.get_absolute_url())

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
    # def post(self, request, *args, **kwargs):
    #     question_pk = self.kwargs.get('pk')
    #     answer_pk = self.kwargs.get('answer_pk')
    #     question = get_object_or_404(Question, pk=question_pk)
    #     answer = QuestionAnswer.objects.get(id=answer_pk)
    #
    #     vote = request.POST.get('answer_vote')
    #     if vote is None:
    #         messages.warning(request, 'You didnt select choice of vote')
    #         return HttpResponseRedirect(question.get_absolute_url())
    #
    #     if self.request.user.is_authenticated:
    #         user = self.request.user
    #         answer_vote = AnswerVote.objects.filter(answer=answer, user=user)
    #         if answer_vote.exists():
    #             answer_vote = answer_vote.first()
    #             if answer_vote.answer_vote == 'draft':
    #                 if vote == 'increase':
    #                     answer_vote.answer_vote = 'increase'
    #                     answer_vote.save()
    #                     answer.increase_rank()
    #                     messages.success(request, 'You vote increase')
    #                     return HttpResponseRedirect(question.get_absolute_url())
    #
    #                 if vote == 'decrease':
    #                     answer_vote.answer_vote = 'decrease'
    #                     answer_vote.save()
    #                     answer.decrease_rank()
    #                     messages.success(request, 'You vote decrease')
    #                     return HttpResponseRedirect(question.get_absolute_url())
    #
    #             elif answer_vote.answer_vote == 'increase' and vote == 'decrease':
    #                 answer_vote.answer_vote = 'draft'
    #                 answer_vote.save()
    #                 answer.decrease_rank()
    #                 messages.info(request, 'You canceled your old vote')
    #                 return HttpResponseRedirect(question.get_absolute_url())
    #
    #             elif answer_vote.answer_vote == 'decrease' and vote == 'increase':
    #                 answer_vote.question_vote = 'draft'
    #                 answer_vote.save()
    #                 answer.increase_rank()
    #                 messages.warning(request, 'You canceled your old vote')
    #                 return HttpResponseRedirect(question.get_absolute_url())
    #
    #             else:
    #                 messages.warning(request, 'You cant vote')
    #                 return HttpResponseRedirect(question.get_absolute_url())
    #
    #         else:
    #             answer_vote = AnswerVote.objects.create(user=user,
    #             answer=answer,
    #             answer_vote=vote)
    #             if vote == 'decrease':
    #                 answer.decrease_rank()
    #             else:
    #                 answer.increase_rank()
    #             messages.success(request, 'You successfully vote')
    #             return HttpResponseRedirect(question.get_absolute_url())
    #
    #     messages.warning(request, 'You have to login to vote')
    #     return HttpResponseRedirect(question.get_absolute_url())
