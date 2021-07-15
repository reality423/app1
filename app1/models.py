from django.db import models

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


