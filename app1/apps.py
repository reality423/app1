from django.apps import AppConfig

# setting.py 에 해당항목을 추가시켜야
# app1 을 장고가 인식할 수 있게된다.
# DB관련 작업에 대한 내용.
# 장고는 models.py를 이용해서 DB 테이블을 생성한다.
# 모델은 app에 종속되어있다.
class App1Config(AppConfig):
    name = 'app1'
