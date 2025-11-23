from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import CarPost, Category, Comment


def post_list(request):
    """Список всех постов"""
    posts = CarPost.objects.filter(is_published=True)
    
    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Фильтрация по категории
    category_slug = request.GET.get('category', '')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Пагинация
    paginator = Paginator(posts, 6)  # 6 постов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'posts': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_slug,
    }
    
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Детальная страница поста"""
    post = get_object_or_404(CarPost, slug=slug, is_published=True)
    
    # Увеличиваем счетчик просмотров
    post.views += 1
    post.save(update_fields=['views'])
    
    # Получаем одобренные комментарии
    comments = post.comments.filter(is_approved=True)
    
    # Похожие посты
    similar_posts = CarPost.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'similar_posts': similar_posts,
    }
    
    return render(request, 'blog/post_detail.html', context)


def category_detail(request, slug):
    """Посты по категории"""
    category = get_object_or_404(Category, slug=slug)
    posts = CarPost.objects.filter(category=category, is_published=True)
    
    # Пагинация
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'posts': page_obj,
        'categories': categories,
        'selected_category': slug,
    }
    
    return render(request, 'blog/category_detail.html', context)

