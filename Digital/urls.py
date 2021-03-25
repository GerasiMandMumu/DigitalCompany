from django.urls import path
from firstapp import views
from django.contrib import admin

from firstapp.forms import ContactForm

from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as email_urls

from django.contrib.auth import views as auth_views

urlpatterns = [

    #path('change-password/', auth_views.PasswordChangeView.as_view()),

    path('admin/', admin.site.urls),
    path('forgot_password', views.forgot_password, name=''),
    path('email/', include(email_urls)),

    # главная страница
    path('', views.index),
    path('main', views.main),
    path('news', views.news),
    path('about', views.about),
    path('contacts', views.contacts),
    path('education', views.education),
    path('unit_news/<int:id>', views.unit_news),

    # поиск
    path('search/', views.SearchResultsView.as_view(), name='search_result'),


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

]
