from django.contrib import admin
from django.urls import path, include
from blog import views
from member import views as member_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name="blog_detail"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),
]
