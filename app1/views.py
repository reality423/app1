from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Question, Answer                #.models : views.py가 속한 경로에서 moels.py를 찾아라
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from app1.forms import QuestionForm, AnswerForm
# 21.07.19 페이징 처리 관련 모듈 import
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required      # 로그인이 안되어 있을 때 로그인 페이지로
from django.contrib import messages



def test(request):
    return render(request, 'app1/template2.html')

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

# 21.07.23 수정전 백업
# def answer_create(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     question.answer_set.create(answer_content=request.POST.get('answer_content'), create_date = timezone.now())
#
#
#     return redirect('app1:detail', question_id=question.id)   # 답변이 달리면 해당 질문으로 보내줌.id값의 확인 일치여부를 위해해

#21.07.23 answer_create 수정(유선미)
# 기존 answer_create 기능 중 로그인한지 않은 사용자도 답변을 달 수 있다라는 문제점이 발견되어 수정
# author  컬럼이 추가됨에 따라 답변 작성자를 저장하기 위한 코드 수정.

@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # 답변 수정은 답변 작성자만 수정 가능하게끔 처리하는 코드

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('app1:detail', question_id = question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    # form에 있는 내용도 받아와야하지만, question에 있는 키값을 받아야하기 떄문에
    return render(request, 'app1/question_detail.html', context)



# 질문 등록함수 21.07.13 (유선미)/ 07.14 수정
# login_required 데코레이터를 추가함으로써
# 만약 질문등록하기 페이지 이동시 로그인이 안되어있다면
# 로그인페이지로 먼저 이동시킨다.
@login_required(login_url='common:login')
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
            question.author = request.user
            question.save()
            return redirect('app1:index')
    else:
        form = QuestionForm()
    return render(request, 'app1/question_form.html', {'form': form})



#21.07.21 질문 수정 함수 추가
@login_required(login_url='common:login')
def question_modify(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    # 본인이 쓴글은 본인만 수정 가능하게

    if request.user != question.author:      # 글쓴이와 현재 접속한 유저 비교
        messages.error(request, '수정권한이 없습니다.')
        return redirect('app1:detail', question_id=question.id)

    # 전송방식이 POST인지를 확인 (question_form으로 접속만한건지
    #                          아니면 데이터를 전송받아왔는지 체크)
    if request.method == "POST":
        # instance = question
        # 인스턴스 파라미터에 question 테이블을 지정해 기존의 값을
        # form에 채워 넣음.
        # 만약 전달받은 데이터가 있다면 전달받은 입력값을 덮어써서
        # QuestionForm을 재생성.
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            # 수정된 내용 저장을 완료후 question_detail 페이지로 이동
            # 주의사항 : 일반적인 방식으로 redirect 리턴한타면
            #           key값(id값)을 찾을수가 없다.
            #           그러한 상황을 방지하기위해 question_id에 기존 컬럼의 key값을
            #           return
            return redirect('app1:detail', question_id=question.id)
            #                                  (key값 리턴 추가)

    form = QuestionForm(instance=question)
    return render(request, 'app1/question_form.html', {'form': form})

#----------------------21.07.21 질문 삭제 함수 등록.
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다 작성자를 확인해주세요.')
        return redirect('app1:detail', question_id=question.id)
    question.delete()
    return redirect('app1:index')

#----------------------21.07.23 답변 수정 함수
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    # answer = get_object_or_404(Answer, pk=answer_id)
    #
    # if request.user == answer.author:
    #     return redirect('app1:detail', answer_id=answer.id)
    #
    # if request.method == "POST":
    #     form = AnswerForm(request.POST)
    #
    #     if form.is_valid():
    #         answer=form.save(commit=False)
    #         answer.author = request.user
    #         answer.modify_date = timezone.now()
    #         answer.save()
    #         return redirect('app1:detail', answer_id=answer.id)
    #
    # form = AnswerForm()
    # return render(request, 'app1/answer_form.html', {'form': form})

    answer = get_object_or_404(Answer, pk=answer_id)
    # 답변 수정은 답변 작성자만 수정 가능하게끔 처리하는 코드
    # 답변 작성자와 로긍니한 유저가 같은지 확인
    if request.user != answer.author:
        # 다르다면 에러 메세지를 템플릿단에 전송
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('app1:detail', question_id = answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('app1:detail', question_id=answer.question.id)
    else:
        form = AnswerForm()
    context = {'form': form }
    return render(request, 'app1/answer_form.html', context)

#-------------21.07.23 답변 삭제 함수 등록
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다 작성자를 확인해주세요.')
        return redirect('app1:detail', answer_id=answer.id)
    answer.delete()
    return redirect('app1:detail')

# def question_create(request):  (백업용/21.07.14)
#     form = QuestionForm()
#     return render(request, 'app1/question_form.html', {'form': form})
