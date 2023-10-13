from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CreateQuestionForm, CreateAnswerForm
from django.views import View
from django.shortcuts import render
from .models import Questions, Answers
from django.contrib.auth.mixins import LoginRequiredMixin



class SignUpView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {'form': CustomUserCreationForm()}
        return render(request, 'registration/signup.html', context)

    def post(self, request, *args, **kwargs):
        print('POST Metod Called : ',request.FILES)
        form = CustomUserCreationForm(request.POST,request.FILES)
        print("Is Form Valid : " ,form.is_valid())
        if form.is_valid():
            book = form.save()
            book.save()
            return HttpResponseRedirect(reverse_lazy("login"))
        return render(request, 'registration/signup.html', {'form': form})


class Question_create(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateQuestionForm()
        return render(request, 'askquestion.html', {'form': form})

    def post(self, request):
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            Q_name = form.cleaned_data["Qname"]
            Q_desc = form.cleaned_data["Qdesc"]
            Q_code = form.cleaned_data["Qcode"]
            user = request.user.username
            rec = Questions.objects.create(question=Q_name, question_desc=Q_desc, code_fld=Q_code,
                                           created_by=user)
            rec.save()
            return render(request, "home.html", {"form": form, 'msg': 'Question Created succc.....'})
        else:
            return render(request, "askquestion.html", {"form": form, 'msg': 'something is wrong'})


def all_question(request):
    obj = Questions.objects.all()
    return render(request, 'all_question.html', {'ques': obj})


def my_question(request):
    userid = request.user.username
    obj = Questions.objects.filter(created_by=userid)
    if obj:
        return render(request, 'my_question.html', {'ques': obj})
    else:
        return render(request, 'home.html', {'msg': 'No question posted'})


class Reply_question(LoginRequiredMixin, View):
    def post(self, request):
        forms = CreateAnswerForm()
        ques = request.POST.get('q_id')
        obj = Questions.objects.get(question_id=ques)
        return render(request, 'ans&upd_question.html', {'qObj': obj, 'form': forms})


class Update_answer(LoginRequiredMixin, View):
    def post(self, request):
        forms = CreateAnswerForm(request.POST)
        if forms.is_valid():
            ans = forms.cleaned_data['Aname']
            desc = forms.cleaned_data['Adesc']
            code = forms.cleaned_data['Acode']
            qid = request.POST.get('q_id')
            auser = request.user.username
            rec = Answers.objects.create(answer=ans, answer_desc=desc, code_fld=code, question_id=qid,
                                         answered_by=auser)
            rec.save()
            qobj = Questions.objects.get(question_id=qid)
            anscnt = qobj.answersCount
            anscnt += 1
            Questions.objects.filter(question_id=qid).update(answersCount=anscnt)
            # form = SendMailForm(request.POST)
            # if form.is_valid():
            #     subject = form.cleaned_data['subject']
            #     msg = form.cleaned_data['message']
            #     mail = form.cleaned_data['mailid']
            #     res = send_mail(subject, msg, "satya.gagan.n@gmail.com", [mail])
            return render(request, "ans&upd_question.html", {"form": forms, 'msg': 'Answer Created succc.....'})
        else:
            return render(request, "ans&upd_question.html", {"form": forms, 'msg': 'something is wrong'})


class ShowAns(LoginRequiredMixin, View):
    def get(self, request, qid):
        #Qid = request.POST.get(qid)
        #print(Qid)
        obj = Answers.objects.filter(question_id=qid)
        return render(request, 'showanswer.html', {'ans': obj})


def updateAns(request):
        aid = request.POST.get('a_id')
        print(aid)
        obj = Answers.objects.get(answer_id=aid)
        #form = CreateAnswerForm(request.POST or None, instance=obj)
        return render(request, 'updateans.html', {'form': obj})
