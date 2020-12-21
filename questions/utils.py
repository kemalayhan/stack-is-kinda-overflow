from .models import Question, QuestionAnswer, QuestionVote, AnswerVote

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages


def is_valid_queryparam(param):
    return param != '' and param is not None

def filter_question(title=None,
            tag=None,
            user_search=None,
            min_date=None,
            max_date=None,
            min_rank=None,
            max_rank=None):
    qs = Question.objects.all()

    if is_valid_queryparam(title):
        qs = qs.filter(title__icontains=title)
    if is_valid_queryparam(tag):
        qs = qs.filter(tag__title__icontains=tag)
    if is_valid_queryparam(user_search):
        qs = qs.filter(user__username__icontains=user_search)
    if is_valid_queryparam(min_date):
        qs = qs.filter(created_date__gte=min_date)
    if is_valid_queryparam(max_date):
        qs = qs.filter(created_date__lte=max_date)
    if is_valid_queryparam(min_rank):
        qs = qs.filter(question_rank__gte=min_rank)
    if is_valid_queryparam(min_rank):
        qs = qs.filter(question_rank__gte=min_rank)
    if is_valid_queryparam(max_rank):
        qs = qs.filter(question_rank__lte=max_rank)

    return qs


class RankMixin(LoginRequiredMixin):
    vote_model = None # QuestionVote or AnswerVote

    # Use this method to return get_absolute_url
    def voted_question(self):
        question_pk = self.kwargs.get('pk')
        p_object = Question.objects.get(pk=question_pk)
        return p_object

    # This function return a object which is Question model object
    # or QuestionAnswer model object. So we can increase or
    # decrease rank via rank method
    def voted_parent(self):
        voted_model_name = self.vote_model.__name__
        print('voted_model_name::::::::::', voted_model_name)
        if voted_model_name == 'AnswerVote':
            answer_pk = self.kwargs.get('answer_pk')
            print('answer_pk', answer_pk)
            p_object = QuestionAnswer.objects.get(pk=answer_pk)
        else:
            question_pk = self.kwargs.get('pk')
            p_object = Question.objects.get(pk=question_pk)
        return p_object

    # This function return a object which give us
    # info that can be rank doesn't exists or exists and
    # value is draft/increase/decrease
    def vote_object(self):
        obj = self.vote_model.objects.filter(user=self.request.user, voted_parent=self.voted_parent())
        return obj

    def post(self, request, *args, **kwargs):
        voted_question = self.voted_question()
        user_vote = self.request.POST.get('vote') # The new value of user's vote
        print("USER VOTE",user_vote)
        if user_vote is None:
            messages.warning(request, 'You didnt select choice of vote')
            return HttpResponseRedirect(voted_question.get_absolute_url())


        voted_parent = self.voted_parent()
        print('voted_parent', voted_parent)
        vote_object = self.vote_object()
        print('vote_object', vote_object)

        if vote_object.exists():
            vote_object = vote_object.first()
            if vote_object.vote_value == 'draft':
                if user_vote == 'increase':
                    vote_object.vote_value = 'increase'
                    vote_object.save()
                    voted_parent.increase_rank()
                    messages.success(request, 'You vote increase')
                    print('AAAAAAAAAAA')
                elif user_vote == 'decrease':
                    vote_object.vote_value = 'decrease'
                    vote_object.save()
                    voted_parent.decrease_rank()
                    messages.success(request, 'You vote decrease')
                    print('BBBBBBBBBBBBB')
                return HttpResponseRedirect(voted_question.get_absolute_url())

            elif vote_object.vote_value == 'increase' and user_vote == 'decrease':
                vote_object.vote_value = 'draft'
                vote_object.save()
                voted_parent.decrease_rank()
                messages.info(request, 'You canceled your old vote')
                print('CCCCCCCCCCCCC')

            elif vote_object.vote_value == 'decrease' and user_vote == 'increase':
                vote_object.vote_value = 'draft'
                vote_object.save()
                voted_parent.increase_rank()
                messages.info(request, 'You canceled your old vote')
                print('DDDDDDDDDDDDD')

            else:
                messages.info(request, 'Something goes wrong')
                print('EEEEEEEEEEEEEE')

            return HttpResponseRedirect(voted_question.get_absolute_url())

        else:
            vote_object = self.vote_model.objects.create(
                user = self.request.user,
                voted_parent = voted_parent,
                vote_value = user_vote
            )
            messages.success(request, 'You successfully vote')
            print('FFFFFFFFFFFFFFFFFFF')
            return HttpResponseRedirect(voted_question.get_absolute_url())
