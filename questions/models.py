from django.db import models

from users.models import User
from django.shortcuts import reverse
from tags.models import Tag




class Question(models.Model):
    user            = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title           = models.CharField(max_length=300)
    content         = models.TextField()
    tag             = models.ManyToManyField(Tag)
    image           = models.ImageField(upload_to="questions_image", blank=True, null=True)
    question_rank   = models.IntegerField(null=True, blank=True, default=0)
    created_date    = models.DateField(auto_now_add=True)
    
    objects = models.Manager()
    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("questions:question_detail", kwargs={"pk": self.pk}) 
    

class QuestionAnswer(models.Model):
    question        = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user            = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question_title  = models.CharField(max_length=50)
    content         = models.TextField()
    image           = models.ImageField(upload_to="answers_image", blank=True, null=True)
    answer_rank     = models.IntegerField(blank=True, null=True, default=0)
    created_date    = models.DateField(auto_now_add=True)