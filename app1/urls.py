from django.urls import path

from . import views


app_name = 'app1'

urlpatterns = [
    path('', views.index, name='index'),
    # -------------21.07.12. detail. answer url 부여 -------------------
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name = 'answer_create'),
    #----------------21.07.13. 질문등록 url 부여 ------------------------
    path('question/create/', views.question_create, name='question_create'),
    #----------------21.07.21 수정url --------------------------
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    #------------- 21.07.21 삭제url ---------------------
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),
    #------------21.07.23 답변 수정 url -------------------
    path('answer/modify/<int:answer_id>', views.answer_modify, name='answer_modify'),
    #------------21.07.23 답변 삭제 url--------------------
    path('answer/delete/<int:answer_id>', views.answer_delete, name='answer_delete'),
    #------------- 21.07.26 오픈템플릿 주소 추가 --------------
    path('testpage3/', views.test, name='test'),
]