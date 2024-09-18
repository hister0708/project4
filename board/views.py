from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Rating
from .forms import CommentForm
import json
from django.core.paginator import Paginator
from .forms import PostForm


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
            return redirect('board:post_detail', post_id=post.id)
        elif 'rating' in request.POST:
            rating_value = int(request.POST.get('rating'))
            Rating.objects.create(post=post, rating=rating_value)
            return redirect('board:post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()

    return render(request, 'board/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'average_rating': post.get_average_rating()
    })

@login_required
def rate_post(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating_value = data.get('rating')
        if rating_value is not None:
            Rating.objects.create(post_id=post_id, rating=int(rating_value))
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('board:post_list')  # 게시글 목록 페이지로 리디렉션
    else:
        form = PostForm()

    return render(request, 'board/create_post.html', {'form': form})
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:  # 작성자만 삭제 가능
        post.delete()
    return redirect('board:post_list')  # 게시글 목록으로 리디렉션

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('board:post_detail', post_id=comment.post.id)


def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # 페이지당 10개의 게시글
    page_number = request.GET.get('page')  # 페이지 번호를 쿼리 파라미터에서 가져옵니다.
    page_obj = paginator.get_page(page_number)

    return render(request, 'board/post_list.html', {
        'page_obj': page_obj
    })
