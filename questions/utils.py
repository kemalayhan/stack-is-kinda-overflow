from .models import Question

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