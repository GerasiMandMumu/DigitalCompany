from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from firstapp.models import Document, Application, News, Step, UserQuestion
from .forms import ContactForm

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import PasswordResetView

from django.contrib.auth import get_user_model
from django_email_verification import send_email

from django.db.models import Q
from django.views.generic import ListView

# ВОССТАНОВЛЕНИЕ ПАРОЛЯ
# забыл пароль
def forgot_password(request):
    if request.method == 'POST':
        return PasswordResetView(request)
        #return PasswordResetView(request, from_email=request.POST.get('email'))
        #return password_reset(request, from_email=request.POST.get('email'))
    else:
        return render(request, "forgot_password.html")
        

# ПОДТВЕРЖДЕНИЕ ПОЧТЫ
def generate_code():
    random.seed()
    return str(random.randint(10000,99999))

def register(request):
    if not request.user.is_authenticated:
        if request.POST:
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                email = form.cleaned_data.get('email')
                my_password1 = form.cleaned_data.get('password1')
                u_f = User.objects.get(username=username, email=email, is_active=False)
                code = generate_code()
                if Profile.objects.filter(code=code):
                    code = generate_code()

                message = code
                user = authenticate(username=username, password=my_password1)
                now = datetime.datetime.now()

                Profile.objects.create(user=u_f, code=code, date=now)

                send_mail('код подтверждения', message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False)
                if user and user.is_active:
                    login(request, user)
                    return redirect('/personalArea/')
                else: 
                    #тут добавить редирект на страницу с формой для ввода кода.
                    form.add_error(None, 'Аккаунт не активирован')
                    return redirect('/activation_code_form/')
                    # return render(request, 'registration/register.html', {'form': form})

            else:
                return render(request, 'registration/register.html', {'form': form})
        else:
            return render(request, 'registration/register.html', {'form':
            RegistrationForm()})
    else:
        return redirect('/personalArea/')

def endreg(request):
    if  request.user.is_authenticated:
        return redirect('/personalArea/')
    else:
        if request.method == 'POST':
            form = MyActivationCodeForm(request.POST)
            if form.is_valid():
                code_use = form.cleaned_data.get("code")
                if Profile.objects.filter(code=code_use):
                    profile = Profile.objects.get(code=code_use)
                else:
                    form.add_error(None, "Код подтверждения не совпадает.")
                    return render(request, 'registration/activation_code_form.html', {'form': form})
                if profile.user.is_active == False:
                    profile.user.is_active = True
                    profile.user.save()
                    # user = authenticate(username=profile.user.username, password=profile.user.password)
                    login(request, profile.user)
                    profile.delete()
                    return redirect('/personalArea/')
                else:
                    form.add_error(None, '1Unknown or disabled account')
                    return render(request, 'registration/activation_code_form.html', {'form': form})
            else:
                return render(request, 'registration/activation_code_form.html', {'form': form})
        else:
            form = MyActivationCodeForm()
            return render(request, 'registration/activation_code_form.html', {'form': form})

def signup(request):
    User = get_user_model()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if Yourmodel.objects.filter(email__iexact=email).count() == 1:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('email_template.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                to_email = form.cleaned_data.get('email')
                send_mail(mail_subject, message, 'youremail', [to_email])
                return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'regform.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Сейчас вы можете подтвердить свою запись')
    else:
        return HttpResponse('Ссылка на активацию недействительна!')

######################################

# главная страница
def index(request):
    return redirect(main)

def main(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        return render(request, "main.html", {'user':user})
    except:
        user = 0
        return render(request, "main.html", {'user':user})
def news(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        news = News.objects.all()
        return render(request, "news.html", {'news': news, 'user':user})
    except:
        user = 0
        news = News.objects.all()
        return render(request, "news.html", {'news': news, 'user':user})
def about(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        return render(request, "about.html", {'user':user})
    except:
        user = 0
        return render(request, "about.html", {'user':user})
def contacts(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        return render(request, "contacts.html", {'user':user})
    except:
        user = 0
        return render(request, 'contacts.html', {'user':user})
def unit_news(request, id):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        news_u = News.objects.get(id=id)
        return render(request, 'unit_news.html', {'news_u': news_u, 'user':user})
    except:
        user = 0
        news_u = News.objects.get(id=id)
        return render(request, 'unit_news.html', {'news_u': news_u, 'user':user})
def education(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        return render(request, "content.html", {'user': user}) 
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})

# задать вопрос
def ask_question(request):
    try:
        if request.method == 'POST':
            common_question = CommonQuestion()
            common_question.question = request.POST['question']
            common_question.answer = ''
            common_question.save()
    except:
        msg = 'Неизвестная ошибка'
        return render(request, 'error.html', {'msg': msg})

# ПОИСК
class SearchResultsView(ListView):
    model = News
    template_name = 'search_result.html'
    def get_queryset(self): # новый
        query = self.request.GET.get('quary')
        object_list = News.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
        print(object_list)
        return object_list      


# вход\выход
# регистрация
def register_view(request):
    #try:
        if request.method == "POST":	
            # регистрация пользователя
            user = User()	
            user.first_name = request.POST.get("name")
            user.last_name = request.POST.get("surname")
            user.username = request.POST.get("email")
            user.password = request.POST.get("password")
            user.email = request.POST.get("email")
            user.is_active = False  # Example
            send_email(user)
            user.save()
            # запись в сессию
            #user = authenticate(email=user.email, password=user.password)
            #login(request, user)
            request.session["email"] = user.email
            request.session["password"] = user.password    
            return redirect(account)
    #except:
        #return render(request, 'error.html')
# авторизация
def aut(request):
    try:
        if request.method == "POST":
            input_password = request.POST["password"]
            input_email = request.POST["email"]
            user = User.objects.get(email=request.POST.get("email"))
            base_email = user.email
            base_password = user.password
            if base_email == input_email and base_password == input_password:
                request.session["email"] = base_email
                request.session["password"] = base_password
                #user = User.objects.get(email=base_email)
                return redirect(account)
            else:
                return render(request, 'error.html')
    except:
        return render(request, 'error.html')
# выход
def exit(request):
    #del request.session['email']
    #del request.session['password']
    logout(request)
    return redirect(index)
# проверка авторизации
def read_data(request):
    flag = False
    if "login" in request.session and "password" in request.session:
	    flag = True
    return flag

# ACCOUNT
# отрисовка
def account(request):        
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        return render(request, "account.html", {"user":user})
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})

# каталог услуг
def services(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        return render(request, "services.html", {'user': user})
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})

# консультация
def consult_view(request):
    s = request.session["email"]
    user = User.objects.get(email=s)
    q = UserQuestion.objects.filter(user=user).exists()
    questions = {}
    if q:
        questions = UserQuestion.objects.filter(user=user)
    return render(request, 'consultation.html', {'questions':questions, 'user':user})

def get_consultation(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        if request.method == 'POST':
            user_question = UserQuestion()
            user_question.user = user
            user_question.question = request.POST['question']
            user_question.answer = ''
            user_question.save()
            q = UserQuestion.objects.filter(user=user).exists()
            questions = {}
            if q:
                questions = UserQuestion.objects.filter(user=user)
            return redirect(consult_view)
            #return render(request, 'consultation.html', {'questions':questions, 'user':user})
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})

# ПОЛИГРАФИЧЕСКИЕ УСЛУГИ
# загрузка документа для печати
def polygraph_service(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        if request.method == 'POST':
            doc = Document(document=request.FILES['document'])
            doc.title = request.FILES['document']
            doc.quantity = request.POST['quantity'] 
            doc.address = request.POST['address']
            doc.user = user
            doc.status = 'на рассмотрении'
            print(doc)
            #doc.save()
            return redirect(polygraph_service)
        return render(request, 'polygraph_service.html', {'user': user})
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})

# ПАТЕНТНЫЕ УСЛУГИ
# заполнение заявки на патент
def patent_service(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        if request.method == 'POST':   
            #inv = Application(image=request.FILES['image'])
            inv = Application()
            inv.user = user
            inv.title = request.POST["title"] 
            inv.email = request.POST["email"]
            inv.applicants_address = request.POST["applicants_address"]
            inv.authors_address = request.POST["authors_address"]
            inv.information = request.POST["information"]
            inv.image = request.FILES['image']
            inv.agreement = request.FILES['agreement']
            inv.essay = request.FILES['essay']
            inv.statement = request.FILES['statement']       
            inv.save()
            return redirect(patent_service)
        return render(request, 'patent_service.html', {'user': user})
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})

 # консультация
# для загрузки согласия
def documents(request):
    pass
# форма обратной связи
def contactView(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		#Если форма заполнена корректно, сохраняем все введённые пользователем значения
		if form.is_valid():
			subject = form.cleaned_data['subject']
			sender = form.cleaned_data['sender']
			message = form.cleaned_data['message']
			copy = form.cleaned_data['copy']

			recipients = ['konst.02@yandex.ru']
			#Если пользователь захотел получить копию себе, добавляем его в список получателей
			if copy:
				recipients.append(sender)
			try:
				send_mail(subject, message, 'smtp.gmail.com', recipients)
			except BadHeaderError: #Защита от уязвимости
				return HttpResponse('Invalid header found')
			#Переходим на другую страницу, если сообщение отправлено
			return render(request, 'thanks.html')
	else:
		#Заполняем форму
		form = ContactForm()
	#Отправляем форму на страницу
	return render(request, 'contact_form.html', {'form': form})

# ЛИЧНЫЕ ДАННЫЕ
def settings(request):
    try:
        s = request.session["email"]
        user = User.objects.get(email=s)
        return render(request, "settings.html", {"user": user})
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})
# изменение данных профиля
def edit(request, id):
    try:
        #s = request.session["email"]
        #user = User.objects.get(email=s)
        user = User.objects.get(id=id)
        if request.method == "POST":
            user.first_name = request.POST.get("first_name")
            user.last_name = request.POST.get("last_name")
            user.email = request.POST.get("email")
            request.session["email"] = user.email
            user.save()
            return redirect(account)
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})	
        

# ЗАЯВЛЕНИЯ
def view_declarations(request):
    try:
        s = request.session["email"]
        usr = User.objects.get(email=s)
        polygraph_s = {}
        patent_s = {}
        poly = Document.objects.filter(user=usr).exists()
        if poly:
            polygraph_s = Document.objects.filter(user=usr)
        patent = Application.objects.filter(user=usr).exists()
        if patent:
            patent_s = Application.objects.filter(user=usr)
        return render(request, "view_declarations.html", {'user': usr, 'polygraph_s': polygraph_s, 'patent_s': patent_s})
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg}) 




# ОБРАЗОВАТЕЛЬНЫЙ КУРС
# страница с тестом
def step(request, id):
    try:
        steps = Step.objects.get(id=id)
        answers = steps.answers.split(';')
        s = request.session["email"]
        usr = User.objects.get(email=s)
        return render(request, "lesson.html", {'steps': steps, 'user': usr, 'answers': answers})
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})

# проверка ответа
def test(request, id):
    try:
        steps = Step.objects.get(id=id)
        answers = steps.answers.split(';')
        s = request.session["email"]
        usr = User.objects.get(email=s)

        if steps.type == 0:
            user_answer = request.POST["user_answer"]
            right_answer = Step.objects.get(id=id).right_answer
        
        elif steps.type == 1:
            user_answer = request.POST.getlist('user_answer') 
            right_answer = Step.objects.get(id=id).right_answer.split(';')
            user_answer.sort()
            right_answer.sort()
        
        elif steps.type == 2:
            user_answer = request.POST["user_answer"]
            right_answer = Step.objects.get(id=id).right_answer
        
        if user_answer == right_answer:
            msg = 'Верно!'
            return render(request, 'lesson.html', {'steps': steps, 'user': usr, 'answers': answers, 'msg': msg})
        else:
            msg = 'Вы ошиблись'
            return render(request, 'lesson.html', {'steps': steps, 'user': usr, 'answers': answers, 'msg': msg})
    except:
        msg = 'Вы не авторизовались'
        return render(request, 'error.html', {'msg': msg})



