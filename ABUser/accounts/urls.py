from django.urls import path, re_path
from .views import SignUpView, Question_create, all_question, my_question, Reply_question,\
    Update_answer, ShowAns,updateAns

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('create/', Question_create.as_view(), name='create_ques'),
    path('all/', all_question, name='all_question'),
    path('my/', my_question, name='my_question'),
    path('reply/', Reply_question.as_view(), name='reply'),
    path('update/', Update_answer.as_view(), name='update'),
    path('showans/<int:qid>/', ShowAns.as_view(), name='ans'),
    path('updatef/', updateAns, name='up_ans'),
]
