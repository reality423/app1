from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Question                #.models : views.py가 속한 경로에서 moels.py를 찾아라
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from app1.forms import QuestionForm

def index(request):
    #21.07.09 질문 목록가져오기
    question_list = Question.objects.order_by('-create_date')   # 질문 제목을 모두 불러와서 ('-')내림차순으로 정렬
    context = {'question_list': question_list}
    return render(request, 'app1/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'app1/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(answer_content=request.POST.get('answer_content'), create_date = timezone.now())

    # redirect : 함수에 전달된 값을 참고해 페이지 이동을 수행하는 함수
    return redirect('app1:detail', question_id=question.id)   # 답변이 달리면 해당 질문으로 보내줌.id값의 확인 일치여부를 위해해

# 질문 등록함수 21.07.13 (유선미)/ 07.14 수정
def question_create(request):
    # 수정 내용 : GET, POST 방식에 대한 처리
    # question_form으로 들어올 때
    # 질문을 등록할 때
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('app1:index')
    else:
        form = QuestionForm()
    return render(request, 'app1/question_form.html', {'form': form})

# def question_create(request):  (백업용/21.07.14)
#     form = QuestionForm()
#     return render(request, 'app1/question_form.html', {'form': form})
