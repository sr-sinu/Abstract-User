'''import Required modules'''
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from accounts.models import Questions, Answers
from .forms import CustomUserCreationForm, CreateQuestionForm, CreateAnswerForm, LoginForm


'''creating Signup class'''
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


'''Creating Questipon class'''
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


'''Creating function for feting all questions'''
def all_question(request):
    obj = Questions.objects.all()
    return render(request, 'all_question.html', {'ques': obj})


'''Creating Function for fetching user quetions'''
def my_question(request):
    userid = request.user.username
    obj = Questions.objects.filter(created_by=userid)
    if obj:
        return render(request, 'my_question.html', {'ques': obj})
    else:
        return render(request, 'home.html', {'msg': 'No question posted'})


'''Creating function for answring the questions'''
class Reply_question(LoginRequiredMixin, View):
    #for posting answers
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
            obj = Answers.objects.filter(question_id=qid)
            return render(request, 'showanswer.html', {'ans': obj})
            # return render(request, "ans&upd_question.html", {'qObj': qobj, "form": CreateAnswerForm(), 'msg': 'Answer Created succc.....'})
        else:
            return render(request, "ans&upd_question.html", {"form": forms, 'msg': 'something is wrong'})


class ShowAns(LoginRequiredMixin, View):
    def get(self, request, qid):
        obj = Answers.objects.filter(question_id=qid)
        return render(request, 'showanswer.html', {'ans': obj})


def updateAns(request):
    aid = request.POST.get('a_id')
    obj = Answers.objects.get(answer_id=aid)
    return render(request, 'updateans.html', {'form': obj})


def login_view(request):
    if request.method == 'GET':
        form = LoginForm(request.POST)
        return render(request, 'registration/login.html',{'form':form})  
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Your login logic here
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                #handling login massage
                message = 'You are sucessfully login'
                # Redirect to the home page
                return render(request, 'home.html', {'msg': message})
            else:
                # Handle invalid login credentials
                error_message = "Invalid username or password."
                return render(request, 'registration/login.html', {'form': form, 'message': error_message})
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    # Redirect to a specific page after logout (e.g., home page)
    return redirect('home')  # Replace 'home' with the name of your home URL pattern
