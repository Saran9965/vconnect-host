from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.frontpage,name='frontpage'),
    path('signup/', views.signup,name='signup'),
    path('login/', views.loginpage,name='login'),
    path('logout/', views.logoutpage,name='logout'),
    path('header/', views.header,name='header'),
    path('content/', views.content,name='content'),
    path('homes/', views.homepage,name='homepage'),
    path('profile/', views.profile,name='profile'),
    path('service/', views.service_list, name='service_list'),
    path('add/', views.add_service, name='add_service'),
    path('plumber/', views.plumber, name='plumber'),
    path('electrician/', views.electrician, name='electrician'),
    path('carpenter/', views.carpenter, name='carpenter'),
    path('tv/', views.tvtech, name='tvtech'),
    path('carp/', views.carp,name='carp'),
    path('plum/', views.plum, name='plum'),
    path('elect/', views.elect, name='elect'),
    path('tvtech/', views.tvtec, name='tvtec'),
    path('service/<int:service_id>/rate/', views.submit_rating, name='submit_rating'),
    path('service/<int:service_id>/review/', views.submit_review, name='submit_review'),
    path('service/<int:service_id>/reviews/', views.get_reviews, name='get_reviews'),
    path('edit-service/<int:service_id>/', views.edit_service, name='edit_service'),
    path('delete-service/<int:service_id>/', views.delete_service, name='delete_service'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'myapp.views.custom_404'
