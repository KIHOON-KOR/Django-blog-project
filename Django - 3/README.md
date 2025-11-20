## *Chapter 03. [블로그] 쿠키와 세션, Login 기능 만들기*

### 블로그 프로젝트 생성 및 Model 생성

1. blog 폴더를 생성합니다. 파일 위치를 확인해주세요. 터미널에서 `mkdir 폴더명` 명령어를 사용하여 만들 수 있습니다.
    
    ```jsx
    mkdir blog
    ```
    

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/770ef409-da64-42d8-9fd1-3ddd6834c699/Untitled.png)

1. 터미널에서 `pyenv virtualenv 3.12.1 oz_blog` 명령어로 새로운 가상환경을 만들고 `pyenv local oz_blog` 명령어로 oz_blog 가상환경을 활성화합니다.
2. `poetry init` 으로 Poetry를 설정하고 `poetry add django` 명령어로 Django를 설치합니다.
3. `django-admin startproject config .` 명령어로 Django 설정 파일을 만듭니다. config 뒤의 온점(.)은 현재 경로에서 파일을 만들겠다는 의미입니다.
4. 설정에서 Python Interpreter의 설정이 올바르게 되어있는지 확인하고, 
Languages & Frameworks에서 Django도 설정합니다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/b1d6bf8a-61e0-43e4-afb1-799c9c968dbd/Untitled.png)

1. `python manage.py startapp blog` 명령어로 blog App을 생성합니다.
2. 생성한 앱을 `config/settings.py` 에 등록합니다. Django에서 기본적으로 제공하는 App과 생성한 앱을 분리하면 관리에 용이합니다.
3. `poetry add ipython` , `poetry add django-extensions` 을 차례로 입력하여 익스텐션을 설치합니다.

```python
## config/settings.py

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

OWN_APPS = [
    'blog',
]

INSTALLED_APPS = DJANGO_APPS + OWN_APPS
```

9. `python manage.py runserver` 로 페이지가 잘 로드되는지 확인해보세요! 
서버를 종료하고 싶을 땐 터미널에 `ctrl + c` 를 입력합니다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/28843481-aebe-44ad-9c89-af7544876633/Untitled.png)

1. `python manage.py migrate` 명령어로 마이그레이트합니다. 
Django 프로젝트에서 필요한 데이터베이스 테이블을 생성하고, 데이터베이스 구조를 초기화합니다. 

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/7bf67407-824b-4aa0-88ce-c470df5d3533/Untitled.png)

> Model을 작성하기 전에 Blog에 무엇이 필요할지 생각해봅니다.
제목, 본문, 작성자, 작성일자, 수정일자, 카테고리 등이 필요하겠네요🧐
> 
1. 모델을 생성하고 `python manage.py makemigrate` 명령어로 마이그레이션 파일을 만듭니다. 

```python
## models.py

from django.db import models

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

    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('작성일자', auto_now=True)
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/87e17249-1c40-426f-b0bf-11f47ee348c8/Untitled.png)

1. 마이그레이션 파일이 생성되었으면 마이그레이트합니다. (직접 작성해보세요💪)
2. DB Browser for SQLite에서 blog의 db.sqlite3 열면 생성한 모델이 반영된 걸 확인합니다.
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/7cc5b043-195a-4d81-837d-1e3b00daf010/Untitled.png)
    

### 블로그 목록 페이지 만들기

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/4fa978ed-f4f2-47cb-a660-dd7f55d5611f/Untitled.png)

1. 관리를 위한 어드민 페이지를 코드를 간단히 만듭니다. 

```python
## admin.py

from django.contrib import admin
from blog.models import Blog

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    ...
```

1. `python manage.py createsuperuser` 어드민 페이지 접속을 위한 슈퍼유저를 만듭니다.
2. Meta클래스와 LANGUAGE_CODE를 설정하여 사용자 친화적으로 만듭니다. (편의를 위한 선택사항)

```python
## models.py
	
from django.db import models

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

    created_at = models.DateTimeField('작성일자', auto_now_add=True)
    updated_at = models.DateTimeField('작성일자', auto_now=True)
    

		# 제목이 노출되는 형식을 설정합니다. [카테고리] 제목은 최대 10자까지
    def __str__(self):
        return f'[{self.get_category_display()}] {self.title[:10]}'

		# Meta 클래스 코드 추가
    class Meta:
        verbose_name = '블로그'
        verbose_name_plural = '블로그 목록'
```

```python
## settings.py

LANGUAGE_CODE = 'ko-KR' # 수정
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/3eaa31ea-6af0-4387-9abe-8ae05dcfbae6/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/00282083-c0c1-45b6-a065-0067be5bb7bd/Untitled.png)

1. 어드민 페이지에서 블로그 글 데이터를 만듭니다. 첨부된 사이트를 이용해보세요.
    
    [guny.kr](http://guny.kr/stuff/klorem/)
    
2.  `views.py` 를 작성합니다.

```python
## views.py

from django.shortcuts import render
from blog.models import Blog

def blog_list(request):
    blogs = Blog.objects.all()

    context = {'blogs': blogs}

    return render(request, 'blog_list.html', context)
```

1. templates 폴더를 만들고 `blog_list.html` 파일을 작성합니다.

```python
## blog_list.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>블로그 목록</h1>

    {% for blog in blogs %}
        <p>
            <a>{{ blog.title }} - {{ blog.created_at }}</a>
        </p>
    {%  endfor %}
</body>
</html>
```

1. `urls.py` 에서 작성한 view를 url 주소와 연결해줍니다.

```python
## urls.py

from django.contrib import admin
from django.urls import path

from blog import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', views.blog_list),
]
```

1. 템플릿 설정을 수정해줍니다.

```python
## settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'], # 수정
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### 블로그 상세 페이지 만들기

> `/blog/{{ blog.id }}` 같이 정적으로 작성하게 되면 프로젝트 규모가 커지고 코드가 길어졌을 때 해당 urls가 사용되는 모든 코드를 관리하기 어렵기 때문입니다. 
urls를 사용하여 `{ % url ‘blog_detail’ book.id }` 처럼 동적으로 작성하는 것을 권장합니다.
> 

```python
## views.py

from django.shortcuts import get_object_or_404, render

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = { 'blog' : blog }
    return render(request, 'blog_detail.html', context)

```

```python
## templates/blog_detail.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>{{ blog.title }}</h1>
    <p>{{ blog.content }}</p>
    # urls.py를 보면 인자를 따로 받지 않기때문에 입력하는 것이 없습니다.
    <a href="{% url 'blog_list' %}">목록으로 돌아가기</a>
</body>
</html>
```

```python
## templates/blog_list.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>블로그 목록</h1>

    {% for blog in blogs %}
        <p>
		        # 위치인자로 들어가기 때문에 blog.id 등으로 작성해도 무관합니다.
		        # 첫번째 인자로 들어온 숫자를 url에 연결해줍니다.
            <a href="{% url 'blog_detail' blog.pk %}"> 
                {{ blog.title }} - <small>{{ blog.created_at | date:"Y-m-d"}}</small>
            </a>
        </p>
    {%  endfor %}
</body>
</html>
```

```python
# urls.py

from django.contrib import admin
from django.urls import path

from blog import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name="blog_detail"),
]
```

### 쿠키와 세션

사용자 식별, 행동 정보 기억을 위해 필요

매번의 요청은 독립적인 사건이기 때문에 기억해야할 정보를 함께 요청하는 작업이 필요

- 쿠키
    - 유저단에 정보 저장 (**클라이언트**)
    - **텍스트**
    - 브라우저에 저장되기 때문에 외부 유출에 취약
    - 보안등급이 높은 정보는 쿠키에 저장할 수 없음
    - 종료 시점을 설정할 수 있고, 미설정 시 브라우저 종료와 동시에 쿠키도 소멸됨
    - 한 도메인당 20개, 쿠키 하나당 4KB로 총 300개의 용량 제한이 있음

- 세션
    - 보안상 브라우저에서 갖고 있을 수 없는 중요 정보를 저장할 수 있다.
    - **서버**에 저장됨
    - 서버는 쿠키가 가진 key와 매핑된 value를 딕셔너리 형태로 저장. (**Object형**)
    - 브라우저가 쿠키의 key로 요청을 하게되면 서버에서는 key를 가지고 유저의 세션 정보를 파악할 수 있음
    - 정확한 소멸 시점을 알 수 없음
    - 서버가 허용하는 선에서 용량 제한이 없음

Blog App으로 실습해봅시다👊 

```python
## views.py

def blog_list(request):
    blogs = Blog.objects.all()

    # get은 visits값을 key값으로 가져오고 Key값이 None일 경우에 디폴트로 지정해준 0을 사용한다.
    # return 되는 값이 str이기 때문에 int로 변환해준다.
    visits = int(request.COOKIES.get('visits',0)) +1

    context = {'blogs': blogs}

    response = render(request, 'blog_list.html', context)
    response.set_cookie('visits', visits) # visits라는 이름으로 visits값을 담아준다.
    return response
```

코드 작성 후 서버를 실행하고, 개발자 모드를 열어주세요. 쿠키를 확인할 수 있습니다. 새로고침을 하면 `value`값이 증가합니다!

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/6b05b1b9-e724-483c-816e-dfd9e0617674/Untitled.png)

```python
def blog_list(request):
    blogs = Blog.objects.all()
    
    visits = int(request.COOKIES.get('visits',0)) +1

    request.session['count'] = request.session.get('count', 0) + 1 # 추가

    context = {'blogs': blogs}

    response = render(request, 'blog_list.html', context)
    response.set_cookie('visits', visits) # visits라는 이름으로 visits값을 담아준다.
    return response
```

세션아이디가 추가되었습니다! 

세션아이디는 출력하지 않는 이상 어떤 데이터를 담고있는지 알 수 없기 때문에 보안적으로 용이합니다.

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/bd8f3204-fd46-4bc0-b7ec-75026021d289/Untitled.png)

### 로그인 페이지 만들기

로그인 정보는 보안에 유의해야하기 때문에 세션에 저장합니다. 
Django에 내장되어있는 **Django Authentication**을 이용해보겠습니다. 

[Using the Django authentication system | Django documentation](https://docs.djangoproject.com/en/5.0/topics/auth/default/)

Authentication views 부분 참고

1. `urls.py` 에 코드를 추가합니다.

```python
## urls.py

from django.contrib import admin
from django.urls import path, include # include import

from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name="blog_detail"),

    # Authentication 코드 추가
    # Django에 내장된 url 사용
    path('accounts/', include('django.contrib.auth.urls')), 
]

```

1. templates폴더 안에 `registration/login.html` 파일을 만듭니다.

```python
## registration/login.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form method="POST">
        {% csrf_token %}
        {{  form.as_p }} {#  form에 있는 정보가 p 태그로 들어갑니다 #}
        <button>submit</button>
    </form>
</body>
</html>
```

![http://127.0.0.1:8000/accounts/login/ 에 접속해서 개발자 도구(단축키 command+option+i)를 열어 p 태그를 확인할 수 있습니다.
](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/9adec27a-e09d-4b83-8573-b46e87d65607/Untitled.png)

http://127.0.0.1:8000/accounts/login/ 에 접속해서 개발자 도구(단축키 command+option+i)를 열어 p 태그를 확인할 수 있습니다.

1. `config/settings.py` 에서 로그인 시 리다이렉트 되는 경로를 설정하는 코드를 작성합니다.

```python
## config/settings.py

LOGIN_REDIRECT_URL = '/' # urls.py 파일을 참고해서 확인해보면 이 경로는 blog_list 페이지입니다.
```

1. http://127.0.0.1:8000/accounts/login/ 에서 슈퍼유저 계정으로 로그인하면 블로그 목록 페이지로 이동하는 것을 확인할 수 있습니다.
    
    ### csrf
    
    ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/d62991e6-657c-4d8d-8f87-cee0c3d237f9/Untitled.png)
    
    - 클라이언트와 서버가 공유하는 인증값이 담긴 보안용 토큰
    - settings.py의 MIDDLEWARE에 설정되어있어 모든 Post에서 CSRF 토큰을 검증한다.
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/28d114b5-1541-490c-aea3-65e3f5d8fd65/Untitled.png)
        
    - crsf 토큰을 주지 않으면 검증에 실패하여 Post 요청이 들어가지 않습니다.
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/a23ce3a5-ea55-4f8d-a7f6-086b54e1367a/Untitled.png)
        
    - username을 보여주는 코드를 추가하여 로그인이 잘 되었는지 확인해보세요!
        
        ```python
        ## blog_list.html
        
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Title</title>
        </head>
        <body>
            <h1>블로그 목록</h1>
        	    <h3>{{ request.user.username }}</h3> # 추가
            {% for blog in blogs %}
                <p>
                    <a href="{% url 'blog_detail' blog.pk %}">
                        {{ blog.title }} - <small>{{ blog.created_at | date:"Y-m-d"}}</small>
                    </a>
                </p>
            {%  endfor %}
        </body>
        </html>
        ```
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/464252eb-fd86-4074-9319-cb778dc08968/Untitled.png)
        
        ![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/d6e7f217-9fa6-4538-88fd-d1c2239a5d90/Untitled.png)
        

### 로그아웃 페이지 만들기

1. `blog_list.html` 에 로그아웃 관련 코드를 작성합니다.

```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {# 로그인 및 유저 정보를 우측 최상단으로 이동 #}
    <nav>
        <div style="text-align: right">
            {% if request.user.is_authenticated %} {# if문을 사용해서 로그인 되었을 때만 로그아웃 버튼 활성화 #}

            {#  로그아웃은 Post 요청입니다. form을 활용합니다. #}
                <form action="{%  url 'logout' %}" method="POST" style="display: inline">
                    {% csrf_token %}
                    <button>로그아웃</button>
                </form>
                {{ request.user.username }}

            {% else %}
             <a href="{%  url 'login' %}">로그인</a>

            {% endif %}
        </div>

    </nav>

    <h1>블로그 목록</h1>
    .
    .
    .
```

1. `settings.py` 에서 로그아웃 리다이렉트 url을 설정합니다.

```python
## settings.py

LOGOUT_REDIRECT_URL = '/'
```

![터미널에서 로그아웃 Post 요청이 잘 들어가는 것을 확인할 수 있습니다.](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/2885d6dd-265f-455d-aef0-c21da9f28734/Untitled.png)

터미널에서 로그아웃 Post 요청이 잘 들어가는 것을 확인할 수 있습니다.

### Signup 페이지 만들기

<aside>
🪄 *PyCharm 꿀팁!*
모듈을 자동으로 import하고 싶다면 `option+Enter` 단축키(Mac 기준)를 사용해보세요!

</aside>

1. App은 모듈화가 가능하도록 만들어야하기 때문에 회원가입 관련 App을 별도로 생성합니다. 
터미널에 `python manage.py startapp member` 명령어를 사용합니다.
2. settings.py 에 신규 생성된 member App을 등록합니다.

```python
## settings.py

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

OWN_APPS = [
    'blog',
    'member' # member App 추가
]

THIRD_PARTY_APPS = [
    'django_extensions',
]

INSTALLED_APPS = DJANGO_APPS + OWN_APPS + THIRD_PARTY_APPS

```

1. **뷰**를 작성하고 `signup.html` 파일을 생성해 작성합니다.

```python
## views.py

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

def sign_up(request):
		# get 요청 시에는 None값
    username = request.POST.get('username')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')

    print('username', username)
    print('password1', password1)
    print('password2', password2)
    form = UserCreationForm() # Django에서 기본적으로 제공하는 가입 관련 폼

    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)
```

```python
## signup.html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>회원가입</h1>
    <form method="post">
        {% csrf_token %}
        {{  form.as_p }}
    </form>
</body>
</html>
```

1. url을 설정합니다.

```python
## urls.py

from django.contrib import admin
from django.urls import path, include # include 추가

from blog import views
from member import views as member_views

urlpatterns = [
    path('signup/', member_views.sign_up, name='signup')
]
```

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/815ae8e7-3b40-41ab-ab07-4bcf63fe8e6f/Untitled.png)

![터미널에서 Post 요청이 잘 들어오는 것을 확인할 수 있습니다.](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/6e6ef5d5-0a59-4015-aa6d-f66bf21b3273/Untitled.png)

터미널에서 Post 요청이 잘 들어오는 것을 확인할 수 있습니다.

1. username의 중복확인 작업과 비밀번호 검증을 위해 코드를 추가합니다.

```python
## member/views.py

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect # redirect 추가

def sign_up(request):
		
		# 추가
    if request.method == 'POST': # POST 요청 시
        form = UserCreationForm(request.POST) # 요청된 폼을 form에 받습니다.

				# form에 받은 데이터를 검증합니다
        if form.is_valid(): 
            form.save()
            return redirect('/accounts/login/')

    else: # GET 요청 시 Form 새로 생성
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)
```

![오류메세지를 확인할 수 있습니다.](https://prod-files-secure.s3.us-west-2.amazonaws.com/00feaf78-d356-41ee-90f9-616e7f73fd77/4a03d73e-f9c5-49c3-b0de-6fa73ba19860/Untitled.png)

오류메세지를 확인할 수 있습니다.

1. 코드를 더 단순화 시킬 수 있습니다.
    
    ```python
    ## settings.py
    
    LOGIN_URL = '/accounts/login/' # 추가
    ```
    
    ```python
    ## member/views.py
    
    	# 현재 Django가 실행되는 환경의 config를 찾아서 import
    	# 혹시 config나 settings 파일의 이름이 바뀌어도 자동으로 인식
    from django.conf import settings 
    
    def sign_up(request):
    
    		# form은 POST 요청일 경우, POST 데이터를 사용하여 생성되고
        # 그렇지 않으면 빈 폼을 생성합니다.
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL) 
    
        context = {
            'form': form
        }
        return render(request, 'registration/signup.html', context)
    ```
    

---

## 🔥 Mini Project. Login 기능 직접 만들기

- 완성코드
    
    ```python
    ## member/views.py
    from django.conf import settings
    from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # 추가
    from django.shortcuts import render, redirect
    from django.contrib.auth import login as django_login
    from django.urls import reverse # 추가
    
    def login(request):
        form = AuthenticationForm(request, request.POST or None)
        if form.is_valid():
            django_login(request, form.get_user())
            return redirect(reverse('blog_list')) # url을 찾는 reverse함수와 urls.py에 적은 name을 활용해 동적으로 작성
    
        else:
            form = AuthenticationForm(request)
    
        context = {
            'form': form
        }
    
        return render(request, 'registration/login.html', context)
    ```
    
    ```python
    ## settings.py
    
    LOGIN_URL = '/login/' # 수정
    ```
    
    ```python
    ## urls.py
    
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
        path('login/', member_views.login, name='login'), # 추가
    ]
    
    ```