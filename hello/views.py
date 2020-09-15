from django.shortcuts import render,redirect,get_object_or_404
from .models import Blog,BlogComment
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    posts=Blog.objects.all().order_by('id')
    paginator=Paginator(posts,3)
    page=request.GET.get('page')
    page_posts=paginator.get_page(page)
    return render(request,'home.html',{'page_posts':page_posts})


def postnew(request):
    return render(request,'postnew.html')

def postcreate(request):
    if(request.method=='POST'):
        newblog=Blog()
        newblog.title=request.POST['title']
        newblog.body=request.POST['body']
        newblog.save()
    return redirect('home')

def detail(request,post_id):
    onepost=get_object_or_404(Blog,pk=post_id)
    comments=onepost.blogcomment_set.all()
    return render(request,'detail.html',{'onepost':onepost, 'comments':comments})

def postedit(request,post_id):
    onepost=get_object_or_404(Blog,pk=post_id)
    return render(request,'postedit.html',{'onepost':onepost})

def postupdate(request,post_id):
    editpost=get_object_or_404(Blog,pk=post_id)
    editpost.title=request.POST['title']
    editpost.body=request.POST['body']
    editpost.save()
    return redirect('/blog/detail/'+str(post_id))

def postdelete(request,post_id):
    deletepost=get_object_or_404(Blog,pk=post_id)
    deletepost.delete()
    return redirect('home')

def blogcommentcreate(req,post_id):
    if(req.method=='POST'):
        post=get_object_or_404(Blog,id=post_id)
        post.blogcomment_set.create(title=req.POST['comment_content'])
    return redirect('/blog/detail/'+str(post_id))

def blogcommentdelete(req,post_id,comment_id):
    comment=get_object_or_404(BlogComment,id=comment_id,blog_id=post_id)
    comment.delete()
    return redirect('/blog/detail/'+str(post_id))