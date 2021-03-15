from django.urls import path
from firstapp import views
from django.contrib import admin

from firstapp.forms import ContactForm


urlpatterns = [
    path('admin/', admin.site.urls),


    path('personalArea/', views.personalArea, name='personalArea'),
    path('register/', views.register, name="register"),
    path('activation_code_form/', views.endreg, name="endreg"),
    path('',views.activation, name='activation'),


    # главная страница
    path('', views.index),
    path('main', views.main),
    path('news', views.news),
    path('about', views.about),
    path('contacts', views.contacts),
    path('education', views.education),

    # вход\выход
    path('register_view', views.register_view),
    path('aut', views.aut),
    path('exit', views.exit),

    # личный кабинет
    path('account', views.account),
    path('services', views.services),
    path('polygraph_service', views.polygraph_service),
    path('patent_service', views.patent_service),
    # загрузка согласия
    path('documents',views.documents),
    # личные данные
	path('settings', views.settings),
	# изменение
	path('edit/<int:id>/', views.edit),
    # заявления
    path('view_declarations', views.view_declarations),

    # обратная связь
    path('contactView', views.contactView),

    # Переход к тесту
	path('step/<int:id>/', views.step),
    path('test/<int:id>', views.test),

    # платежная система



    # Изменение пароля
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change-password.html',success_url = '/'),name='change_password'),

    # Забыл пароль
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html',
             subject_template_name='password_reset_subject.txt',
             email_template_name='password_reset_email.html',
             success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
