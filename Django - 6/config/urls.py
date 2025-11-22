from django.contrib import admin
from django.urls import path, include
from blog import views
from member import views as member_views
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, RedirectView
from django.views import View

# class AboutView(TemplateView):
#     template_name = 'about.html'
#
# class TestView(View): # Django의 View 클래스 상속
#     def get(self, request):
#         return render(request, 'test_get.html')
#
#     def post(self, request):
#         return render(request, 'test_post.html')

from blog import cb_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('fb/', include('blog.fbv_urls')),

    # # CBV blog
    # path('', cb_views.BlogListView.as_view(), name='blog_list'),
    # path('<int:pk>/', cb_views.BlogDetailView.as_view(), name='blog_detail'),
    # path('create/', cb_views.BlogCreateView.as_view(), name='blog_create'),
    # path('<int:pk>/update/', cb_views.BlogUpdateView.as_view(), name='blog_update'),
    # path('<int:pk>/delete/', cb_views.BlogDeleteView.as_view(), name='blog_delete'),

    # FBV blog
    # path('', views.blog_list, name='blog_list'),
    # path('<int:pk>/', views.blog_detail, name="blog_detail"),
    # path('create/', views.blog_create, name='blog_create'),
    # path('<int:pk>/update/', views.blog_update, name='blog_update'),
    # path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),

    # auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),

    # path('test/', TestView.as_view(), name='test'),
    # # path('about', TemplateView.as_view(template_name='about.html'), name='about'),
    # path('about', AboutView.as_view(), name='about'),
    # path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
    # path('redirect2/', lambda req: redirect('about')),

]

