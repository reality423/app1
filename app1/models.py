from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 질문과 답변 테이블 생성(21.7.8 유선미 작성)
# 질문 테이블 : Question
# 질문 제목 : subject
# 질문 내용 : content
# 질문 작성일자 : create_date

#--------------------------질문테이블 -------------------------------------------
class Question(models.Model):
    subject = models.CharField(max_length=100)
    content = models.TextField()
    create_date = models.DateTimeField()
#-------------------21.07.21  글쓴이(author)------------------
    # 추가하는 author 컬럼
    # author = 사용자 ID
    #on_delete=models.CASCADE : User에 있는 값이 삭제되면 해당 값과 연결된
    #                           Question 테이블의 데이터를 삭제하라는 의미
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # modify_date 컬럼 = 수정일자(작성한 질문에 대한)
    # null=True : 해당 컬럼에 null 값 허용
    # blank=True : 폼 데이터 검사시 값이 없어도 된다는 의미.
    modify_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.subject

#---------------------------답변테이블--------------------------------------------
# 답변 테이블 : Answer
# 답변 내용 : answer_content
# 답변 작성일자 : create_date
# 질문 제목 : question(어떤 질문에 대한 답변인지 알아야 하기 때문에)
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)    # 질문이 삭제가 되면 답변도 자동으로 삭제
    answer_content = models.TextField()
    create_date = models.DateTimeField()
    # null=True: 컬럼의 null값 허용
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    modify_date = models.DateTimeField(null=True, blank=True)


