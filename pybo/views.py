from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

def index(request):
    page = request.GET.get('page','1') # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10) # 한 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    # question = Question.objects.get(id = question_id)
    question = get_object_or_404(Question, pk = question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.') # 오직 POST 메소드만 사용 가능
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

    # 아래 코드 2개 모두 동작함
    # form 형식으로 바꾸기 위해 주석 처리
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    """
    answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    answer.save()
    """
    # return redirect('pybo:detail', question_id=question.id)

def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit = False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)