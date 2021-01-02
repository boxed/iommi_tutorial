from django.http import (
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from iommi import (
    Action,
    Field,
    Form,
    Table,
)

from polls.models import Question


def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'polls/index.html', context)

    # OR

    # class IndexView(generic.ListView):
    #     template_name = 'polls/index.html'
    #     context_object_name = 'latest_question_list'
    #
    #     def get_queryset(self):
    #         """Return the last five published questions."""
    #         return Question.objects.order_by('-pub_date')[:5]

    # {% if latest_question_list %}
    #     <ul>
    #     {% for question in latest_question_list %}
    #         <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    #     {% endfor %}
    #     </ul>
    # {% else %}
    #     <p>No polls are available.</p>
    # {% endif %}
    return Table(
        auto__rows=Question.objects.order_by('-pub_date')[:5],
        columns__question_text__cell__url=lambda row, **_: row.get_absolute_url(),
    )


def detail(request, question_id):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})

    # OR

    # class DetailView(generic.DetailView):
    #     model = Question
    #     template_name = 'polls/detail.html'

    # <h1>{{ question.question_text }}</h1>
    # <ul>
    # {% for choice in question.choice_set.all %}
    #     <li>{{ choice.choice_text }}</li>
    # {% endfor %}
    # </ul>
    return Form(
        auto__instance=get_object_or_404(Question, pk=question_id),
        editable=False,
    )


def results(request, question_id):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/results.html', {'question': question})

    # OR

    # class ResultsView(generic.DetailView):
    #     model = Question
    #     template_name = 'polls/results.html'


    # <h1>{{ question.question_text }}</h1>
    #
    # <ul>
    # {% for choice in question.choice_set.all %}
    #     <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
    # {% endfor %}
    # </ul>
    #
    # <a href="{% url 'polls:detail' question.id %}">Vote again?</a>

    question = get_object_or_404(Question, pk=question_id)
    return Table(
        title=str(question),
        auto__rows=question.choice_set.all(),
        auto__exclude=['question'],
        actions__vote_again=Action(display_name='Vote again?', attrs__href=reverse('polls:vote', args=(question_id,))),
        actions_below=True,
    )


def vote(request, question_id):
    # question = get_object_or_404(Question, pk=question_id)
    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'polls/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    # <h1>{{ question.question_text }}</h1>
    #
    # {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
    #
    # <form action="{% url 'polls:vote' question.id %}" method="post">
    # {% csrf_token %}
    # {% for choice in question.choice_set.all %}
    #     <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
    #     <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
    # {% endfor %}
    # <input type="submit" value="Vote">
    # </form>

    question = get_object_or_404(Question, pk=question_id)

    def post_handler(form, **_):
        if form.is_valid():
            choice = form.fields.choice.value
            choice.votes += 1
            choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    return Form(
        title=str(question),
        fields__choice=Field.choice_queryset(question.choice_set.all()),
        actions__submit__post_handler=post_handler,
    )
