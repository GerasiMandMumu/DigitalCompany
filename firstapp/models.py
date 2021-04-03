from django.db import models
from django.contrib.auth.models import User

# Двухфакторная аутентификация пользователя
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', default=None, on_delete=models.CASCADE) # привязка к пользователю
    code = models.CharField(max_length=50,blank=True, null=True, default=None) # код восстановления
    date = models.DateField(blank=True, null=True) # дата

# Готовый документ
class ReadyDocument(models.Model):
    title = models.CharField(max_length=255) # название документа
    document = models.FileField(upload_to='documents/polygraph/') # загрузка документа


# Документ для полиграфических услуг
class Document(models.Model):
    title = models.CharField(max_length=255) # название документа
    document = models.FileField(upload_to='documents/polygraph/') # загрузка документа
    quantity = models.IntegerField() # количество
    address = models.CharField(max_length=255) # адрес доставки
    uploaded_at = models.DateTimeField(auto_now_add=True)  # время загрузки
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING) # привязка к пользователю
    status = models.CharField(max_length=100) # статус
    paid = models.BooleanField(default=False) # оплата печати

# Документ для патентных услуг
class Application(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True) # время загрузки
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING) # привязка к пользователю
    status = models.CharField(max_length=100) # статус
    title = models.CharField(max_length=255) # название изобретения
    email = models.EmailField(max_length=255) # email
    image = models.ImageField(upload_to='documents/patent/image/') # загрузка графического изображения
    agreement = models.FileField(upload_to='documents/patent/agreement/') # загрузка согласия
    information = models.CharField(max_length=500) # Описание изобретения
    applicants_address = models.CharField(max_length=255) # адрес заявителя
    authors_address = models.CharField(max_length=255) # адрес автора
    essay = models.FileField(upload_to='documents/patent/essay/') # реферат
    statement = models.FileField(upload_to='documents/patent/statement/') # загрузка заявления о выдаче патента
    paid_first = models.BooleanField(default=False) # оплата первой пошлины
    paid_second = models.BooleanField(default=False) # оплата второй пошлины

# Новость
class News(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)

# Шаг курса
class Step(models.Model):
    type = models.IntegerField()
    title = models.TextField() 
    question = models.TextField()
    answers = models.TextField()
    right_answer = models.TextField()

class UserQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING) # привязка к пользователю
    question = models.TextField() # пользовательский запрос
    answer = models.TextField() # ответ администратора

class CommonQuestion(models.Model):
    question = models.TextField() # пользовательский запрос
    answer = models.TextField() # ответ администратора

