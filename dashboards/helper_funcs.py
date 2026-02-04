from .models import GroupHierarchy
from blogs.models import Blog, Category
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied

def user_has_higher_group(user, other_user):
    if user.is_superuser:
        return True
    elif other_user.is_superuser:
        return False
    else:
        user_levels = GroupHierarchy.objects.filter(
            group__user=user
        ).values_list("level", flat=True)

        other_levels = GroupHierarchy.objects.filter(
            group__user=other_user
        ).values_list("level", flat=True)

        if max(user_levels, default=0) > max(other_levels, default=0):
            return True
        elif max(user_levels, default=0) < max(other_levels, default=0) :
            return False
        elif  max(user_levels, default=0) == max(other_levels, default=0):
            'equal'
       

def blog_permission_level(func):
    def wrapper(*args,**kwargs):
        print(args)
        print(kwargs)
        request = args[0]
        pk = kwargs['pk']
        
        user = request.user
        other_user =  get_object_or_404(Blog, pk=pk).author
        flag = None

        if user.is_superuser:
            flag =  True
        elif other_user.is_superuser:
            flag = False
        else:
            user_levels = GroupHierarchy.objects.filter(
                group__user=user
            ).values_list("level", flat=True)

            other_levels = GroupHierarchy.objects.filter(
                group__user=other_user
            ).values_list("level", flat=True)

            if max(user_levels, default=0) > max(other_levels, default=0) or user == other_user:
                flag = True
            elif max(user_levels, default=0) < max(other_levels, default=0) or max(user_levels, default=0) == max(other_levels, default=0) :
                flag = False
            
        if flag:
            return func(*args,**kwargs)
        else:
            raise PermissionDenied

    return wrapper

