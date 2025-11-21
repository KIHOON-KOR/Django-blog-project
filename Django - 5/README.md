## *Chapter 04. [블로그] 상세페이지 만들기*

### 블로그에 작성자 컬럼 만들기 및 오류 해결법

1. 블로그 모델에서 작성자 컬럼을 추가하고 마이그레이트 합니다.

```python
## blog/models.py

from django.contrib.auth import get_user_model # 추가
from django.db import models

## 추가
User = get_user_model() # Django에 설정된 유저를 찾아서 가져오는 함수

class Blog(models.Model):
    CATEGORY_CHOICES = (
        ('free', '자유'),
        ('travle', '여행'),
        ('cat', '고양이'),
        ('dog', '강아지')
    )

    category = models.CharField('카테고리', max_length=10, choices=CATEGORY_CHOICES)
    title = models.CharField('제목', max_length=100)
    content = models.TextField('본문')

    ## 추가
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제가 불가능함 (유저를 삭제하려고할때 블로그가 있으면 유저 삭제가 불가능)
    # models.SET_NULL => null값을 넣습니다. => 유저 삭제시 블로그의 author가 null이 됨, 이 때 null=True 옵션도 함께 설정 필요
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('수정일자', auto_now=True)

    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'

```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/f4d0df51-ad95-49b9-ae0f-6b580ba2e8b2/Untitled.png)

author 컬럼을 추가함에 따라 기존에 있던 데이터들이 author 컬럼에 어떤 값을 가져야 할지를 정해줍니다. author 컬럼은 null값을 허용하는 옵션이 없기 때문에 데이터가 필요합니다. 

해결방법은 두 가지 입니다.
1) 1회성 디폴트 값을 기입
2) 추후 수동 처리
강의에서는 1번을 선택하고 디폴트 값으로 1을 기입했습니다.

1. User 데이터를 함께 넣어봅시다. html 파일을 수정합니다.

```python
{# blog/blog_detail.html #}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{{ blog.title }}</h1>
    <div style="text-align: right">
        {{ blog.author.username }}
    </div>
    <hr>
    <p>{{ blog.content }}</p>
    <a href="{% url 'blog_list' %}">목록으로 돌아가기</a>
</body>
</html>
```

```python
{# blog/blog_list.html #}

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
		.
		.
		.

    <h1>블로그 목록</h1>
    {% for blog in blogs %}
        <p>
            <a href="{% url 'blog_detail' blog.pk %}">
                {{ blog.title }} <span>({{ blog.author.username }})</span> - <small>{{ blog.created_at | date:"Y-m-d"}}</small> # 수정
            </a>
        </p>
    {%  endfor %}
</body>
</html>
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/93e7fbeb-7bbd-4d9d-8c98-150f2705e31e/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/4a5c14fe-2e79-4abf-807c-f295cf5abf86/Untitled.png)

### Base.html로 템플릿 extends 시키기

> **Template Engine extends**
전체페이지, 네비게이션 같은 공통된 템플릿을 공유
> 
1. `templates/base.html` 파일을 생성합니다.
    
    ```html
    {# templates/base.html #}
    
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8
        <title>블로그 프로젝트</title>
    </head>
    <body>
        <nav style="display: flex; justify-content: space-between">
            {# 홈으로 가는 버튼 추가 #}
            <div>
                <a href="{% url "blog_list" %}">홈</a>
            </div>
            <div style="text-align: right">
                {% if request.user.is_authenticated %}
                    <form action="{%  url 'logout' %}" method="POST" style="display: inline">
                        {% csrf_token %}
                        <button>로그아웃</button>
                    </form>
                    {{ request.user.username }}
                {% else %}
    	            <a href="{%  url 'signup' %}">회원가입</a>
    	            <a href="{%  url 'login' %}">로그인</a>
                {% endif %}
            </div>
        </nav>
        {# 공통적으로 갖는 상단 네비바를 제외하고 자유롭게 변형할 수 있도록 설정 #}
        {%  block content %}{% endblock %}
    </body>
    </html>
    ```
    
    1. html 파일들을 수정하여 `base.html` 을 공유하도록 합니다.
    
    ```html
    {# blog/blog_list.html #}
    
    {% extends 'base.html' %}
    {% block content %}
        <h1>블로그 목록</h1>
        {% for blog in blogs %}
            <p>
                <a href="{% url 'blog_detail' blog.pk %}">
                    {{ blog.title }} - <small>{{ blog.created_at | date:"Y-m-d"}}</small>
                </a>
            </p>
        {%  endfor %}
    {% endblock %}
    ```
    
    ```html
    {# blog/blog_detail.html #}
    
    {% extends 'base.html' %}
    {% block content %}
        <h1>{{ blog.title }}</h1>
        <div style="text-align: right">
            {{ blog.author.username }}
        </div>
        <hr>
        <p>{{ blog.content }}</p>
        <a href="{% url 'blog_list' %}">목록으로 돌아가기</a>
    {% endblock %}
    ```
    
    ```html
    {# registration/login.html #}
    
    {% extends 'base.html' %}
    {%  block content %}
    		<h1>로그인</h1>
        <form method="POST">
            {% csrf_token %}
            {{  form.as_p }}
            <button>submit</button>
        </form>
    {% endblock %}
    ```
    
    ```html
    {# registration/signup.html #}
    
    {% extends 'base.html' %}
    {% block content %}
        <h1>회원가입</h1>
        <form method="post">
            {% csrf_token %}
            {{  form.as_p }}
            <button>회원가입</button>
        </form>
    {% endblock %}
    ```
    

### 블로그 Form

<aside>
💡 **Django Forms의 기능**
1. HTML에 input 그려주기 
2. validation (검증)
3. 저장 및 업데이트

</aside>

1. blog App에 `forms.py` 파일을 생성합니다.

```python
## forms.py

from django import forms
from blog.models import Blog

class BlogForm(forms.ModelForm): # Model을 가지고 만들어서 ModelForm 상속
    class Meta:
        model = Blog
        fields = ('title', 'content', ) # 전체를 적용하려면 '__all__'

```

2. `blog/views.py` 에 `forms.py`를 적용합니다. 

```python
## blog/views.py

from django.shortcuts import redirect, reverse

from blog.forms import BlogForm
from blog.models import Blog
from django.shortcuts import get_object_or_404, render

def blog_create(request):

    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False) # 블로그 모델만 생성, commit=False 왜 사용? -> form에는 없는 사용자의 정보를 입력하기 위함
        blog.author = request.user # author는 현재 로그인 된 유저
        blog.save()
        # kwargs는 reverse 함수에서 URL을 생성할 때, URL 패턴에서 요구하는 동적 경로 매개변수에 값을 전달하기 위해 사용
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))

    context = {'form': form}
    return render(request, 'blog_create.html', context)
```

```python
## config/urls.py

from django.contrib import admin
from django.urls import path, include

from blog import views
from member import views as member_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name="blog_detail"),
    path('create/', views.blog_create, name='blog_create'), # 추가

    # auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),
]

```

1. `blog_create.html` 파일도 만들어줍니다.

```python
{# templates/blog_create.html #}

{% extends 'base.html' %}
{%  block content %}
<form method="POST">
    {% csrf_token %}
    {{  form.as_p }}
    <button>생성</button>
</form>
{% endblock %}
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/acd76c69-9ee2-4d6a-8e5f-6bf4895d2ed7/Untitled.png)

1. 로그인하지 않은 유저가 글을 작성할 경우에는 로그인 페이지로 이동하는 코드를 작성합니다.

```python
## blog/views.py

from django.contrib.auth.decorators import login_required

@login_required() # 인증된 유저가 아닐 경우 settings.py에 설정된 LOGIN_URL로 이동하는 데코레이터
def blog_create(request):
    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False) # 블로그 모델만 생성
        blog.author = request.user # author는 현재 로그인 된 유저
        blog.save()
        # kwargs는 reverse 함수에서 URL을 생성할 때, URL 패턴에서 요구하는 동적 경로 매개변수에 값을 전달하기 위해 사용
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))

    context = {'form': form}
    return render(request, 'blog_create.html', context)
```

```python
## member/views.py

def login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        django_login(request, form.get_user())
				
				# 추가
        next = request.GET.get('next')
        if next:
            return redirect(next)
        
        return redirect(reverse('blog_list'))

    else:
        form = AuthenticationForm(request)

    context = {
        'form': form
    }

    return render(request, 'registration/login.html', context)
```

1. 최근 글이 가장 위로 올라오도록 코드를 수정합니다.

```python
## blog/views.py

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at') # 수정

    context = {'blogs': blogs}

    return render(request, 'blog_list.html', context)
```

1. 블로그 목록 페이지에서 바로 글을 작성할 수 있는 버튼을 추가합니다. 
비로그인 상태에서 누르면 로그인 페이지로 이동합니다.

```python
{# blog/blog_list.html #}

{% extends 'base.html' %}
{% block content %}
    <h1>블로그 목록</h1>
    
    {# 생성 버튼 #}
    <p style="text-align: right">
    <a href="{% url 'blog_create' %}">생성</a>
    </p>
    
    {% for blog in blogs %}
        <p>
            <a href="{% url 'blog_detail' blog.pk %}">
                {{ blog.title }} - <small>{{ blog.created_at | date:"Y-m-d"}}</small>
            </a>
        </p>
    {%  endfor %}
{% endblock %}
```

### 블로그 수정 페이지

수정버튼은 로그인 유저와 글을 작성한 유저가 동일할 때만 보여야 합니다.

1. `blog_update.html` 파일을 생성합니다.

```python
{# templates/blog_update.html #}

{% extends 'base.html' %}
{%  block content %}
    <h1>블로그 수정</h1>
    <form method="POST">
        {% csrf_token %}
        {{  form.as_p }}
        <button>수정</button>
        
    </form>
{% endblock %}
```

1. 기본적인 뷰를 작성합니다.

```python
## blog/views.py

@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)

    context = {'blog': blog}
    return render(request, 'blog_update.html', context)
```

1. url을 연결합니다.

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name="blog_detail"),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/update/', views.blog_update, name='blog_update'), # 추가

    # auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),
]
```

![작성자와 로그인한 유저가 동일해야 수정 버튼이 활성화됩니다.](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/69c2db3d-5b6d-4016-b59e-ad0f0cb009b8/Untitled.png)

작성자와 로그인한 유저가 동일해야 수정 버튼이 활성화됩니다.

1. 블로그 상세페이지에도 수정 버튼을 추가했습니다.

```python
{# blog/blog_detail.html #}

{% extends 'base.html' %}
{% block content %}
    <h1>{{ blog.title }}</h1>
    {% if request.user == blog.author %}
        <div style="text-align: right">
            <a href="{% url 'blog_update' blog.pk %}">수정</a>
            {{ blog.author.username }}
        </div>
    {% endif %}
    <hr>
    <p>{{ blog.content }}</p>
    <a href="{% url 'blog_list' %}">목록으로 돌아가기</a>
{% endblock %}
```

1. blog_update 뷰를 이어서 작성합니다.

```python
## blog/views.py

@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)

    form = BlogForm(request.POST or None, instance=blog) # instance로 기초데이터 세팅
    if form.is_valid():
        blog = form.save()
        return redirect(reverse('blog_detail', kwargs={'pk': blog.pk}))

    context = {'blog': blog,
               'form' : form,
               }

    return render(request, 'blog_update.html', context)
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/29573eaa-dcf7-4652-bd89-55129f2a3175/Untitled.png)

### 블로그 페이지네이션

1. 페이지네이션 구현 전, 데이터를 먼저 여러개 만들어줍니다.

```bash
# 쉘을 실행합니다.
>> python [manage.py](http://manage.py) shell_plus

# 기존의 블로그 글을 blog_list에 담습니다.
>> blog_list = Blog.objects.all()

# 새로운 블로그 글이 담길 빈 리스트를 생성합니다.
>> new_blog_list = []

# 반복문으로 기존 글을 new_blog_list에 추가합니다.
# id = None 으로 새로운 데이터로 인식하게합니다.
>>  for i in range(10):
   ...:     for blog in blog_list:
   ...:         blog.id = None
   ...:         new_blog_list.append(blog)
   
>> Blog.objects.bulk_create(new_blog_list)
```

1. blog_list 함수에 페이지네이션 코드를 추가합니다.

```python
## blog/views.py

from django.core.paginator import Paginator

def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

    # 한 페이지당 10개씩 보이도록
    paginator = Paginator(blogs, 10)

    # request.GET은 쿼리스트링을 가져옵니다.
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    context = {
        # 'blogs': blogs,
        'page_object': page_object,
    }

    return render(request, 'blog_list.html', context)
```

1. `blog.id` 를 제목 앞에 추가하고 페이지네이션 코드를 작성합니다. 
http://127.0.0.1:8000/?page=2 와 같이 물음표 뒤의 쿼리문으로 페이지를 이동할 수 있습니다. page=0은 마지막 페이지로 이동합니다.

```python
{# blog/blog_list.html #}

{% extends 'base.html' %}
{% block content %}
    <h1>블로그 목록</h1>

    <p style="text-align: right">
    <a href="{% url 'blog_create' %}">생성</a>
    </p>

		{# 수정 #}
    {% for blog in page_object %}
        <p>
            <a href="{% url 'blog_detail' blog.pk %}">
                ({{ blog.id }}){{ blog.title }} - <small>{{ blog.created_at | date:"Y-m-d"}}</small>
            </a>
        </p>
    {%  endfor %}
{% endblock %}
```

1. 페이지 하단에 페이지번호 링크를 추가하는 코드를 작성합니다.

```python
{# blog/blog_list.html #}

{% extends 'base.html' %}
{% block content %}
    <h1>블로그 목록</h1>
    <p style="text-align: right">
    <a href="{% url 'blog_create' %}">생성</a>
    </p>

    {% for blog in page_object %}
        <p>
            <a href="{% url 'blog_detail' blog.pk %}">
                ({{ blog.id }}){{ blog.title }} - <small>{{ blog.created_at | date:"Y-m-d"}}</small>
            </a>
        </p>
    {%  endfor %}
    
    {# 추가 #}
    <div>
        {% if page_object.has_previous %} {# 이전 페이지가 존재할 때 #}
            <a href="?page=1">&laquo; 첫번째</a>
            <a href="?page={{ page_object.previous_page_number }}">이전</a>
        {% endif %}
        <span>
            Page {{ page_object.number }} of {{ page_object.paginator.num_pages }}
        </span>
    {% if page_object.has_next %}
            <a href="?page={{ page.object.next_page_number }}">다음</a>
            <a href="?page={{ page.object.paginator.num_pages }}">마지막</a>

    {% endif %}
    </div>
{% endblock %}
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/0d7d2cfe-6e5e-4808-96d5-c6d03a4baafa/Untitled.png)

1. 특정 페이지로 이동하는 코드를 추가합니다.

```python
{# blog/blog_list.html #}

{% extends 'base.html' %}
{% block content %}
    <h1>블로그 목록</h1>
    <p style="text-align: right">
    <a href="{% url 'blog_create' %}">생성</a>
    </p>

    {% for blog in page_object %}
        <p>
            <a href="{% url 'blog_detail' blog.pk %}">
                ({{ blog.id }}){{ blog.title }} - <small>{{ blog.created_at | date:"Y-m-d"}}</small>
            </a>
        </p>
    {%  endfor %}
    
    <div>
		    {# 수정 #}
        {#    page_object.number = 현재페이지#}
        {#    page_object.paginator.num_pages = 최대페이지#}

        {# 이전 페이지가 있는 경우, 첫 번째 페이지와 이전 페이지로 이동할 수 있는 링크를 보여줍니다. #}
        {% if page_object.has_previous %}
            <a href="?page=1">&laquo; 첫번째</a>
            <a href="?page={{ page_object.previous_page_number }}">이전</a>
        {% endif %}

        {# 현재 페이지 번호 근처의 페이지 번호 링크를 출력합니다. #}
        {% if page_object.number|add:-2 > 1 %}
            <a href="?page={{ page_object.number|add:-3 }}">&hellip;</a>
        {% endif %}

        {# 각 페이지 번호에 대한 링크를 출력합니다. 현재 페이지는 (현재페이지)로 표시됩니다. #}
        {% for i in page_object.paginator.page_range %}
            {% if page_object.number == i %}
                <span>(현재페이지)</span>
            {% elif i > page_object.number|add:-3 and i < page_object.number|add:3 %}
                <a href="?page={{ i }}">{{ i }}</a>
            {% endif %}
        {% endfor %}{

        {# 마지막 페이지로 이동하는 링크와 현재 페이지 기준으로 앞뒤의 ... 표시를 추가합니다. #}
        {% if page_object.paginator.num_pages > page_object.number|add:2 %}
            <a href="?page={{ page_object.number|add:3 }}">&hellip;</a>
        {% endif %}

        {# 다음 페이지가 있는 경우, 다음 페이지와 마지막 페이지로 이동할 수 있는 링크를 보여줍니다. #}
        {% if page_object.has_next %}
                <a href="?page={{ page.object.next_page_number }}">다음</a>
                <a href="?page={{ page.object.paginator.num_pages }}">마지막 &raquo;</a>
        {% endif %}
    </div>
{% endblock %}
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/015dafeb-56d9-4a2a-ad96-711e6e79c37f/Untitled.png)

### 블로그 검색

1. 검색 버튼을 추가합니다.

```python
{# blog/blog_list.html #}

{% extends 'base.html' %}
{% block content %}
    <h1>블로그 목록</h1>

    {# 생성 버튼 #}
    <p style="text-align: right">
    <a href="{% url 'blog_create' %}">생성</a>
    </p>

    {% for blog in page_object %}
        <p>
            <a href="{% url 'blog_detail' blog.pk %}">
                ({{ blog.id }}){{ blog.title }} - <small>{{ blog.created_at | date:"Y-m-d"}}</small>
            </a>
        </p>
    {%  endfor %}

    {# 검색버튼 추가 #}
    <form method="get" style="margin-bottom: 10px;">
        <input name="q" type="text" placeholder="검색어를 입력하세요." value="{% if request.GET.q %}{{ request.GET.q }}{% endif %}">> {# 검색어 보여주기 #}
        <button>검색</button>
    </form>

    <div>
      .
      .
      .
```

```python
## blog/views.py

from django.urls import reverse
def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

		# 추가
		# 제목과 본문 모두 검색 대상으로 설정
    q = request.GET.get('q')
	  if q:
		    blogs = blogs.filter(
		        Q(title__icontains=q) |
		        Q(content__icontains=q)
		    )

    paginator = Paginator(blogs, 10)
	
   .
   .
   
```

![검색어를 입력하면 터미널에서 쿼리문이 받아지는 것을 확인할 수 있습니다](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/d02c328d-b065-465e-9e17-6e6996ab35f5/Untitled.png)

검색어를 입력하면 터미널에서 쿼리문이 받아지는 것을 확인할 수 있습니다

1. 검색 후, 다른 페이지 번호를 눌렀을 때 전체 블로그 글이 보여지는 부분을 수정합니다.

```python
{# blog/blog_list.html #}

.
.
.

    <div>       
            <a href="?page=1{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">&laquo; 첫번째</a> # 수정
            <a href="?page={{ page_object.previous_page_number }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">이전</a> # 수정
        {% endif %}

        {% if page_object.number|add:2 > 1 %}
            <a href="?page={{ page_object.number|add:-3 }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">&hellip;</a> # 수정
        {% endif %}

        {% for i in page_object.paginator.page_range %}
            {% if page_object.number == i %}
                <span>(현재페이지)</span>
            {% elif i > page_object.number|add:-3 and i < page_object.number|add:3 %}
                <a href="?page={{ i }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">{{ i }}</a> # 수정
            {% endif %}
        {% endfor %}

        {% if page_object.paginator.num_pages > page_object.number|add:2 %}
            <a href="?page={{ page_object.number|add:3 }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">&hellip;</a> # 수정
        {% endif %}

       
        {% if page_object.has_next %}
                <a href="?page={{ page.object.next_page_number }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">다음</a> # 수정
                <a href="?page={{ page.object.paginator.num_pages }}{% if request.GET.q %}&q={{ request.GET.q }}{% endif %}">마지막 &raquo;</a> # 수정
        {% endif %}
    </div>
{% endblock %}
```

---

## 🔥 Mini Project. 블로그 삭제 기능 만들기

- 완성코드
    
    ```python
    ## views.py
    
    from django.views.decorators.http import require_http_methods # 추가
    
    @login_required()
    # 특정 요청만 허락하는 데코레이터. 삭제나 수정은 POST 요청으로 받아야합니다.
    @require_http_methods(['POST']) 
    def blog_delete(request, pk):
        blog = get_object_or_404(Blog, pk=pk, author=request.user)
        blog.delete()
    
        return redirect(reverse('blog_list'))
    ```
    
    ```python
    {# blog_detail.html #}
    
    {% extends 'base.html' %}
    {% block content %}
      <h1>{{ blog.title }}</h1>
    
      {% if request.user == blog.author %}
        <div style="text-align: right">
          <a href="{% url 'blog_update' blog.pk %}">수정</a>
    
          <form action="{% url 'blog_delete' blog.pk %}" method="POST" style="display: inline">
            {% csrf_token %}
            <button>삭제</button>
          </form>
        </div>
      {% endif %}
    
      <div style="text-align: right">
        {{ blog.author.username }}
      </div>
      <hr>
      <p>{{ blog.content }}</p>
    
      <a href="{% url 'blog_list' %}">목록으로 돌아가기</a>
    {% endblock %}
    ```
    
    ```python
    ## urls.py
    
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', views.blog_list, name="blog_list"),
        path('<int:pk>/', views.blog_detail, name="blog_detail"),
        path('create/', views.blog_create, name='blog_create'),
        path('<int:pk>/update/', views.blog_update, name='blog_update'),
        path('<int:pk>/delete/', views.blog_delete, name='blog_delete'), # 추가
    
        # auth
        path('accounts/', include("django.contrib.auth.urls")),
        path('signup/', member_views.sign_up, name='signup'),
        path('login/', member_views.login, name='login'),
    ]
    ```
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/bb9fc4c8-5cba-4467-9c2e-ebd7abee5f8a/Untitled.png)