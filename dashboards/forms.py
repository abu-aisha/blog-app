from django import forms
from blogs.models import Blog, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from dashboards.models import GroupHierarchy


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


NON_PUBLISHER_STATUS_CHOICES = (
    ("Draft", "Draft"),
    ("Submit", "Submit")
)

PUBLISHER_STATUS_CHOICES = (
    ("Draft", "Draft"),
    ("Published", "Publish"), # (backend, frontend)
)

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
    def __init__(self,*args,user = None ,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['status'].choices = PUBLISHER_STATUS_CHOICES
        user_levels = GroupHierarchy.objects.filter(
            group__user=user
        ).values_list("level", flat=True)
        print('\n',user_levels[0],'\n')
        if not user.is_superuser and user_levels[0] <= 1:
            self.fields.pop('is_featured')
            self.fields['status'].choices = NON_PUBLISHER_STATUS_CHOICES
            print(self.fields['status'].choices)
            print('\n',self.fields,'\n')
            
class AddUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')