from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db.models import Q
from django.views import View


from .models import Question, QuestionAnswer, QuestionVote, AnswerVote
from .forms import QuestionCreateForm, QuestionAnswerForm
from .utils import filter_question, RankMixin


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
        context = {"object_list": self.get_queryset()}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        params = request.POST
        print(params)
        kwargs = {
            '{0}__{1}'.format('title', 'icontains'): params.get('title'),
            '{0}__{1}__{2}'.format('tag', 'title', 'icontains'): params.get('tag'),
            '{0}__{1}__{2}'.format('user', 'username', 'icontains'): params.get('user'),
            '{0}__{1}'.format('created_date', 'gte'): params.get('min_date'),
            '{0}__{1}'.format('created_date', 'lte'): params.get('max_date'),
            '{0}__{1}'.format('rank', 'gte'): params.get('min_rank'),
            '{0}__{1}'.format('rank', 'lte'): params.get('max_rank'),
        }
        questions_raw = Question.objects.all()
        questions = filter_question(questions_raw, **kwargs)
        context = {"object_list": questions}

        return render(request, self.template_name, context)


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["answers"] = self.object.answers.all().filter(parent=None)
        context["form"] = QuestionAnswerForm()
        try:
            question_vote = QuestionVote.objects.get(
                user=self.request.user, voted_parent=self.object
            )
            context["question_vote"] = question_vote
        except BaseException:
            context["question_vote"] = 'Oy kullanmadınız'
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
            try:
                parent_id = int(request.POST.get('parent_id'))
            except BaseException:
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
