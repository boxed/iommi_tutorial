from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from iommi import (
    Table,
    Form,
)

from polls.models import Question


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'polls/index.html', context)
    return Table(
        auto__rows=Question.objects.order_by('-pub_date')[:5],
        columns__question_text__cell__url=lambda row, **_: row.get_absolute_url(),
    )


def detail(request, question_id):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})
    return Form(
        auto__instance=get_object_or_404(Question, pk=question_id),
        editable=False,
    )


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
