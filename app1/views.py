from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Question                #.models : views.py가 속한 경로에서 moels.py를 찾아라
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from app1.forms import QuestionForm
# 21.07.19 페이징 처리 관련 모듈 import
from django.core.paginator import Paginator

def index(request):
    # request: 외부 사용자의 요청을 받아오는 것.
    # render : 템플릿을 로딩할 때 사용.
    # redirect : url로 이동시 사용용    # 사용자가 localhost:8000/app1 페이지 접속이라는 요청을 보냈다.
    # view -> urls에 어떤 함수를 실행해야 하는지를 확인.
    # 21.07.09 질문 목록가져오기
    # view에서 model단에 요청
    # 요청의 내용 : 조회 (Question 테이블/모델 create_date 컬럼을 기준으로
    #               정렬해서 가져옴) -> 그 결과를 question_list 변수에 저장.

    page = request.GET.get('page', '1')

    question_list = Question.objects.order_by('-create_date')   # 질문 제목을 모두 불러와서 ('-')내림차순으로 정렬
    # context라는 변수에 딕셔너리 형태로 question_list key와 value를 저장.
    # 템플릿단에서 해당 데이터를 쉽게 조회하기 위해.
    # 페이징 처리 내용 : 가져온 데이터를 10개씩 보여달라.
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)


    context = {'question_list': page_obj}
    # 받은 요청에 대해(request)
    # app1/question.list.html 템플릿을 열어주고
    # 해당 템플릿에 context 변수의 값을 전송.

    return render(request, 'app1/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'app1/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(answer_content=request.POST.get('answer_content'), create_date = timezone.now())


    return redirect('app1:detail', question_id=question.id)   # 답변이 달리면 해당 질문으로 보내줌.id값의 확인 일치여부를 위해해

# 질문 등록함수 21.07.13 (유선미)/ 07.14 수정
def question_create(request):
    # 수정 내용 : GET, POST 방식에 대한 처리
    # question_form으로 들어올 때
    # 질문을 등록할 때
    # POST 방식인지 GET 방식인지 확인
    # why? 단순히 질문등록 페이지를 오픈한 것인지 아니면 질문등록 페이지에 데이터를 입력해서 저장한 것인지를 구분.
    if request.method == "POST":
        # forms.py에 설정한 QuestionForm 클래스를 호출
        # request.POST :사용자가 입력한 데이터를  받아온다.
        form = QuestionForm(request.POST)
        # 변수 form에 들어온 값이 올바른값(정상적인 값)인지를 확인
        if form.is_valid():
            # 저장을 하기전 잠시 유보.
            # question 변수에 form에서 받아온 데이터는 넣어뒀지만
            # 아직 DB로 저장하지는 않았다.
            question = form.save(commit=False)
            # create_date 컬럼을 따로 입력받지 않은 이유는?
            # 질문등록의 날짜 시간의 경구 현재 시간으로 입력받기 위해
            # view에서 처리.
            question.create_date = timezone.now()
            question.save()
            return redirect('app1:index')
    else:
        form = QuestionForm()
    return render(request, 'app1/question_form.html', {'form': form})

# def question_create(request):  (백업용/21.07.14)
#     form = QuestionForm()
#     return render(request, 'app1/question_form.html', {'form': form})
