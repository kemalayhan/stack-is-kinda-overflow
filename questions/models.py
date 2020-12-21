from django.db import models

from users.models import User
from django.shortcuts import reverse
from tags.models import Tag




class Question(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title           = models.CharField(max_length=300)
    content         = models.TextField()
    tag             = models.ManyToManyField(Tag)
    image           = models.ImageField(upload_to="questions_image", blank=True, null=True)
    rank            = models.IntegerField(null=True, blank=True, default=0)
    created_date    = models.DateField(auto_now_add=True)

    objects = models.Manager()
    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("questions:question_detail", kwargs={"pk": self.pk})

    def increase_rank(self): # f object race condition
        self.rank += 1
        self.save()

    def decrease_rank(self):
        self.rank -= 1
        self.save()



class QuestionAnswer(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    parent          = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,related_name='replies')
    content         = models.TextField(max_length=300)
    image           = models.ImageField(upload_to="answers_image", blank=True, null=True)
    rank            = models.IntegerField(blank=True, null=True, default=0)
    created_date    = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

    def increase_rank(self):
        self.rank += 1
        self.save()

    def decrease_rank(self):
        self.rank -= 1
        self.save()


class QuestionVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_parent = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL)
    vote_value = models.CharField(max_length=10, null=True, blank=True, default='draft')


class AnswerVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voted_parent = models.ForeignKey(QuestionAnswer, null=True, blank=True, on_delete=models.SET_NULL)
    vote_value = models.CharField(max_length=10, null=True, blank=True, default='draft')
