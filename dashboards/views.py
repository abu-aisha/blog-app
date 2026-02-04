from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from blogs.models import Blog, Category
from django.contrib.auth.decorators import login_required,permission_required

from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .helper_funcs import user_has_higher_group,blog_permission_level




@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()

    context = {
        'category_count': category_count,
        'blogs_count': blogs_count,
    }
    return render(request, 'dashboards/dashboard.html', context)


###### CATEGORY OPERATIONS
@login_required(login_url='login')
@permission_required('blogs.view_category',login_url = 'login',raise_exception = True)
def categories(request):
    return render(request, 'dashboards/categories.html')

@login_required(login_url='login')
@permission_required('blogs.add_category',login_url = 'login',raise_exception = True)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboards:categories')
    form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboards/add_category.html', context)

@login_required(login_url='login')
@permission_required('blogs.change_category',login_url = 'login',raise_exception = True)
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('dashboards:categories')
    form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'dashboards/edit_category.html', context)

@login_required(login_url='login')
@permission_required('blogs.delete_category',login_url = 'login',raise_exception = True)
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('dashboards:categories')

###### BLOG/POST OPERATIONS

@login_required(login_url='login')
@permission_required('blogs.view_blog',login_url = 'login',raise_exception = True)
def posts(request):
    posts = Blog.objects.filter(author = request.user)

    context = {
        'posts': posts,
    }
    return render(request, 'dashboards/posts.html', context)



@login_required(login_url='login')
@permission_required('blogs.add_blog',login_url = 'login',raise_exception = True)
def add_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES,user = request.user)
        if form.is_valid():
            post = form.save(commit=False) # temporarily saving the form
            post.author = request.user
            post.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            return redirect('dashboards:posts')
        else:
            print('form is invalid')
            print(form.errors)
    form = BlogPostForm(request.POST or None, user = request.user)
    context = {
        'form': form,
    }
    return render(request, 'dashboards/add_post.html', context)

@login_required(login_url='login')
@permission_required('blogs.change_blog',login_url = 'login',raise_exception = True)
@blog_permission_level
def edit_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post,user = request.user)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-'+str(post.id)
            post.save()
            if post.status == "Published":
                if post.author == request.user:
                    return redirect('dashboards:posts')
                else:
                    return redirect('dashboards:all_pub_posts')
            elif post.status == "Submit":
                return redirect('dashboards:posts_review')
            else:
                return redirect('dashboards:posts')


           
    form = BlogPostForm(user = request.user,instance=post)
    context = {
        'form': form,
        'post': post
    }

    return render(request, 'dashboards/edit_post.html', context)
   
@login_required(login_url='login')
@permission_required('blogs.delete_blog',login_url = 'login',raise_exception = True)
@blog_permission_level
def delete_post(request, pk):
    post = get_object_or_404(Blog, pk=pk)
    post.delete()
    return redirect('dashboards:posts')

@login_required(login_url='login')
@permission_required('blogs.change_category',login_url = 'login',raise_exception = True)
def all_pub_posts(request):
    """
    Docstring for all_pub_posts
    
    :param request: Description
    1. renders 'dashboards/all_pub_posts.html'.
    2. returns all published posts by all only visible to editors upwards(status = "Published").
    3. Ensure that editors can not edit or delete mate or senior posts
    4. Ensure it does not display draft posts
    """
    posts = Blog.objects.filter(status = "Published")

    context = {
        'posts': posts,
    }
    return render(request, 'dashboards/all_pub_posts.html', context)


@login_required(login_url='login')
@permission_required('blogs.change_category',login_url = 'login',raise_exception = True)
# @blog_permission_level
def posts_review(request):
    """
    Docstring for posts_review
    
    :param request: Description
    1. renders 'dashboards/posts_review.html'.
    2. returns all submitted posts by authors for review (status = "Submit").
    3. Ensure it does not edit same level nor senior level post.
    4. Ensure it does not display draft posts
    """

    posts = Blog.objects.filter(status = "Submit")

    context = {
        'posts': posts,
    }
    return render(request, 'dashboards/posts_review.html', context)
    

@login_required(login_url='login')
def apply_to_write(request):
    """
    Docstring for apply_to_write
    
    :param request: Description
    1. renders 'dashboards/apply_form.html'.
    2. Apply to be an author.
    3. Re authenticate that the user is not already an author---
    4. check if user does not have permission to write already.
    """
    
    pass


##### ADMIN OPERATIONS ON USERS
@login_required(login_url='login')
@permission_required('blogs.delete_blog',login_url = 'login',raise_exception = True)
def users(request):
    users = User.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'dashboards/users.html', context)



@login_required(login_url='login')
@permission_required('blogs.add_user',login_url = 'login',raise_exception = True)
def add_user(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboards:users')
        else:
            print(form.errors)
    form = AddUserForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboards/add_user.html', context)

@login_required(login_url='login')
@permission_required('blogs.edit_user',login_url = 'login',raise_exception = True)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboards:users')
    form = EditUserForm(instance=user)
    context = {
        'form': form,
    }
    return render(request, 'dashboards/edit_user.html', context)

@login_required(login_url='login')
@permission_required('delete.add_user',login_url = 'login',raise_exception = True)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('dashboards:users')