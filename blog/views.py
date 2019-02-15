from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .forms import BlogPost

def blog(request):
    blogs = Blog.objects 
    #모든 블로그 글들을 대상으로 
    blog_list = Blog.objects.all()
    #블로그 객체 세 개를 한 페이지로 자르기
    paginator = Paginator(blog_list, 3)
    #request된 페이지가 뭔지를알아내고 request page를 변수에 담기
    page = request.GET.get('page')
    #request된 페이지(번호)를 얻어온뒤 return 해준다
    posts = paginator.get_page(page)

    return render(request, 'blog.html', {'blogs': blogs,'posts':posts})
# 쿼리셋 ex) Blog의 object들
# 메소드 : 쿼리셋을 활용해서 보여줌
# 쿼리셋과 메소드의 형식
# 모델.쿼리셋(objects).method

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog':blog_detail})

# home에서는 하나밖에 없지만 
# detail은 여러 개니까 특정 번호의 객체를 담을 수 있어야한다.
# => get_object_or_404(class, 검색조건(몇 번 데이터, pk))
# pk : primary key 객체들의 이름표, 구분자, 데이터의 대푯값

def new(request): #new.html을 띄워주는 함수
    return render(request, 'new.html')

def create(request):#입력받은 내용을 db에 넣어주는 함수
    blog= Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save() #blog.delete가능
    return redirect('/blog/'+str(blog.id))#url은 str이므로 int였던 id를 str로 바꿔줘야함

#redirect와 render의 차이
#redirect는 url을 받음 http://google.com 가능
#render는 3번째 인수를 가지고 프로젝트내에서 사용함

def blogpost(request):
    # 1. 입력된 내용을 처리하는 기능 -> (method로 구분) POST
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #model을 반환하데 저장하지 않고 반환해줌 commit=False
            post.pub_date = timezone.now()
            #title,body만 form으로 post로 반환해주고 시간은 아님
            post.save()
            return redirect('blog')
    # 2. 빈 페이지를 띄워주는 기능 -> GET
    else :
        form = BlogPost()
        return render(request, 'new.html', {'form':form})
