# Build a To-do List app with Django (Class based view)
---
## Table of contents
1. [Make directory & virtual environment
](#makeDirectory)
2. [Install Django and start project
](#installDjango)
3. [Create an app](#createApp)
4. [Run server](#runServer)
5. [Connect base app to the project](#connectBase)
6. [Link todo_list/urls --> base/urls --> base/views](#linkUrls)
7. [Create a model (database item)](#createModel)
8. [Make migrations and migrate](#migrations)
9. [Create superuser](#createsuperuser)
10. [Create the first class based view](#createClassBaseView)
11. [Create templates](#createTemplates)
12. [Display model in a list](#displayModel)
13. [Change context name of object_list](#changeContextName)
14. [Detail View](#detailView)
15. [Add view button to each task in task_list.html](#addViewButton)
16. [Create form to add item (CreateView)](#createView)
16. [Update View](#updateView)
17. [Delete View](#deleteView)
18. [Add view button to each task in task_list.html](#addViewButton)
19. [Create Form to add item (CreateView)](#createView)
20. [Update View (UpdateView)](#updateView)
21. [Delete Page (DeleteView)](#deleteView)
22. [Display login user & login/login button](#displayLoginUser)
23. [Create Login Page](#createLoginPage)
24. [Logout](#logout)
25. [Retrict data access without login](#retrictDataWithoutLogin)
26. [Retrict each user can only see his own items](#retrictUser)
27. [Remove the select user field in create form](#removeUserField)
28. [Register User](#registerUser)
29. [](#)
30. [](#)
31. [](#)
32. [](#)
33. [](#)
34. [](#)






    1. [Sub paragraph](#subparagraph1)
4. [Another paragraph](#paragraph2)

<a name="makeDirectory"></a>
## Make directory & virtual environment
In terminal:

```
cd desktop
mkdir todo_list
python3 -m venv venv
source venv/bin/activate
```
This will create the "venv" directory if it doesn’t exist


<a name="installDjango"></a>
## Install Django and start project

```
pip install django
django-admin startproject todo_list .
```

The use of . just instructs Django to create a project in the current directory

<a name="createApp"></a>
## Create an app 
```
python manage.py startapp base
```

<a name="runServer"></a>
## Run server
```
python manage.py runserver
```

<a name="connectBase"></a>
## Connect base app to the project
add 'base.apps.BaseConfig',

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base.apps.BaseConfig',
]
```

<a name="linkUrls"></a>
## Link todo_list/urls --> base/urls --> base/views
under `todo_list/urls.py`, add `include` and a path include base.urls

```
...
from django.urls import path, include

urlpatterns = [
    ...
    path('', include('base.urls')),
]
```

since we don't have `base.urls` yet, under base folder, create `urls.py` file, and type this:

```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.taskList, name = 'tasks'),
]
```
under `views.py`, create a very simple function-based view `taskList` which return a HttpReponse.  We will change to class-based view later.

```
...
from django.http import HttpResponse

def taskList(request):
    return HttpResponse('To Do List')
```
>Note: runserver now, it should now show "To Do List" on the site.




<a name="createModel"></a>
## Create a model (database item)
under `base/models.py`, create a `Task` model

```
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
```
> Note:
> 
>models.CASCADE means the user is deleted, the item will also be deleted.

>models.SET_NULL means the user is deleted, the item remains.

>null = True means when submit to database, it is allowed to be empty

>blank = True means when submitting the form, it is allowed to be blank


<a name="migrations"></a>
## Make migrations and migrate 
```
python manage.py makemigrations
python manage.py migrate
```

<a name="createsuperuser"></a>
## Create superuser 
```
python manage.py createsuperuser
```


<a name="runServer"></a>
## Register model to admin 
under `base/admin.py`, add the `Task` model to admin page by:

```
from django.contrib import admin
from . models import Task

admin.site.register(Task)
```






<a name="createClassBaseView"></a>
## Create the first class-based view 
Now let's change `taskList` from function-based view to class-based view.
Under `base/views.py`, change to the following:

* remove HttpReponse
* def --> class
* TaskList (Capital T because its a class now)
* inherit as a ListView

```
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Task

class TaskList(ListView):
    model = Task
```

In `base/urls.py`, update to:

* import TaskList itself instead of the entire views
* use `.as_view()` is how class-based view works

```
from django.urls import path
from .views import TaskList

urlpatterns = [
    path('', TaskList.as_view(), name = 'tasks'),
]
```
>Note: if runserver now, it should show that the template `base/task_list.html` does not exist.  In class-based view, ListView looks for a template with the prefix of the model name (task) and the suffix of _list.html if not otherwise set (task_list.html).  This can be overridden by setting the `template_name` attribute.


<a name="createTemplates"></a>
## Create templates
Under base directory, create a folder `templates`. Then inside `templates` create another folder `base` <- same name as the app.  Then create a file `task_list.html` and simply write a line for now.

```
<h1>My To Do List</h1>

```
>Note: if runserver now, it should show 'My To Do List' on screen.

<a name="displayModel"></a>
## Display model in a list
By default, Django calls the querylist `object_list`.
Let's show it in `task_list.html`:

```
<h1>My To Do List</h1>

<table>
    <tr>
        <th>Items</th>
    </tr>
    {% for task in object_list %}
    <tr>
        <td>{{task.title}}</td>
    </tr>
    {% empty %}
        <h3> No items in list</h3>
    {% endfor%}
</table>

```
>Note: if runserver now, it should show a list of all items in the queryset.

<a name="changeContextName"></a>
## Change context name of object_list
We can replace `object_list` with any name we want. We want it to be `tasks`.In `views.py`, add the line `context_object_name`

```
class TaskList(ListView):
    model = Task
    context_object_name = 'tasks'

```
now in the templates, replace `object_list` with `tasks`

```
<h1>My To Do List</h1>

<table>
    <tr>
        <th>Items</th>
    </tr>
    {% for task in tasks %}
    <tr>
        <td>{{task.title}}</td>
    </tr>
    {% empty %}
        <h3> No items in list</h3>
    {% endfor%}
</table>

```
>Note: if runserver now, it should show exactly the same as before.



<a name="detailView"></a>
## Detail View (DetailView)
To create a task detail page, go to `views.py`, import `DetailView` and define a new class `TaskDetail`.

```
...
from django.views.generic.detail import DetailView
...

class TaskList(ListView):
...

class TaskDetail(DetailView):
    model = Task

```
In `urls.py`, import `TaskDetail`, and add path

```
...
from .views import TaskList, TaskDetail

urlpatterns = [
   ...
    path('task/<int:pk>/', TaskDetail.as_view(), name = 'task'),
]
```


`DetailView` looks for a html with a suffix of `_detail.html`, so let's create `task_detail.html`

```
<h1>Tasks: {{object}} </h1>
```
>Note: if runserver `http://127.0.0.1:8000/task/1` it should show "Tasks: get milk" <- whatever the item is.

We can replace `object` with any name we want. We want it to be `task`. In `views.py`, add the line `context_object_name`

```
class TaskDetail(DetailView):
    model = Task
    contex_object_name = 'task'
```
and replace `object` in `task_detail.html`

```
<h1>Tasks: {{task}} </h1>
```
We can also replace `task_detail.html` with `task.html`, simply add `template_name` and change the html name.

```
class TaskDetail(DetailView):
    ...
    template_name = 'base/task.html'
```


<a name="addViewButton"></a>
## Add view button to each task in task_list.html
To add a `view` buttons to our table, we add 2 lines:

* `<th></th>`
* `<td><a href="{% url 'task' task.id %}">View</a></td>`

```
<h1>My To Do List</h1>

<table>
    <tr>
        <th>Items</th>
        <th></th>
    </tr>
    {% for task in tasks %}
    <tr>
        <td>{{task.title}}</td>
        <td><a href="{% url 'task' task.id %}">View</a></td>
    </tr>
    {% empty %}
        <h3> No items in list</h3>
    {% endfor%}
</table>
```
<a name="createView"></a>
## Create Form to add item (CreateView)
In `views.py` add these:

```
...
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

...

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')
```
In `urls.py` add `TaskCreate` and new path `task-create`

```
...
from .views import TaskList, TaskDetail, TaskCreate

urlpatterns = [
    ...
    path('task-create/', TaskCreate.as_view(), name = 'task-create'),
]

```
Create a new html `task_form.html` since `CreateView` regonizes `_form.html` as the form page.

```
<h3>task form</h3>

<a href="{% url 'tasks' %}">Go back</a>

<form method="post", action="">
	{% csrf_token %}
	{{form.as_p}}
	<input type="submit" value="Submit">
</form>
```
Create a "Add Task" button at the top of the `task_list.html`

```
<h1>My To Do List</h1>
<a href="{% url 'task-create' %}">Add Task</a>
...
```

<a name="updateView"></a>
## Update View (UpdateView)
in `views.py`, import `UpdateView` and add new class `TaskUpdate`

```
...
from django.views.generic.edit import CreateView, UpdateView
...
class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')
```
in `urls.py`, import `TaskUpdate`

```
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate
...
urlpatterns = [
    ...
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name = 'task-update'),
]
```
in `task_list.html`, add another:

* `<th></th>`
* `<td><a href="{% url 'task-update' task.id %}">Edit</a></td>`


```
<h1>My To Do List</h1>
<a href="{% url 'task-create' %}">Add Task</a>

<table>
    <tr>
        <th>Items</th>
        <th></th>
        <th></th>
    </tr>
    {% for task in tasks %}
    <tr>
        <td>{{task.title}}</td>
        <td><a href="{% url 'task' task.id %}">View</a></td>
        <td><a href="{% url 'task-update' task.id %}">Edit</a></td>
    </tr>
    {% empty %}
        <h3> No items in list</h3>
    {% endfor%}
</table>
```


<a name="deleteView"></a>
## Delete Page (DeleteView)
in `views.py`, import `DeleteView` & create class `DeleteView`

```
...
from django.views.generic.edit import CreateView, UpdateView, DeleteView
...
class DeleteView(DeleteView):
    model = Task
    contex_object_name = 'task'
    success_url = reverse_lazy('tasks')
```
in `urls.py` import `DeleteView` & path `task-delete`

```
...
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView

urlpatterns = [
    ...
    path('task-delete/<int:pk>/', DeleteView.as_view(), name = 'task-delete'),
]
```
`DeleteView` search for a html with `_confirm_delete.html`, so we create `task_confirm_delete.html`

```
<a href="{% url 'tasks' %}">Go back</a>
<form method = "POST">
    {% csrf_token %}
    <p>Are you sure you want to delete this task? "{{task}}"</p>
    <input type="submit" value="Delete"/>
</form>
```
at last, add the delete button in `task_list.html`:

* `<th></th>`
* `<td><a href="{% url 'task-delete' task.id %}">Delete</a></td>`

```
<h1>My To Do List</h1>
<a href="{% url 'task-create' %}">Add Task</a>

<table>
    <tr>
        <th>Items</th>
        <th></th>
        <th></th>
        <th></th>
    </tr>
    {% for task in tasks %}
    <tr>
        <td>{{task.title}}</td>
        <td><a href="{% url 'task' task.id %}">View</a></td>
        <td><a href="{% url 'task-update' task.id %}">Edit</a></td>
        <td><a href="{% url 'task-delete' task.id %}">Delete</a></td>
    </tr>
    {% empty %}
        <h3> No items in list</h3>
    {% endfor%}
</table>
```

<a name="displayLoginUser"></a>
## Display login user & login/login button
in `task_list.html`, write a if statement to display username and login button if already logged in.  Else, show login button:

```
{% if request.user.is_authenticated %}
    <p>{{request.user}}</p>
    <a href="">Logout</a>
{% else %}
    <a href="">Login</a>
{% endif %}

<hr>
<h1>My To Do List</h1>
...
```

<a name="createLoginPage"></a>
## Create Login Page
in `views.py` , import `LoginView` & create a class `CustomLoginView`

```
...

from django.contrib.auth.views import LoginView

...

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
```
in `urls.py` import `CustomLoginView` & path

```
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView

...

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    ...
]

```
create a file `login.html`

```
<h1>login</h1>

<form method = "POST">
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="Login">
</form>
```
now add back the login link in the `task_list.html`

```
{% if request.user.is_authenticated %}
    <p>{{request.user}}</p>
    <a href="">Logout</a>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}
```


<a name="logout"></a>
## Logout
for logout, we can directly import and use the LogoutView function, so we import it to `urls.py` to use, instead of importing it in `views.py` this time. In `url.py`:


```
...
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
   ...]

```
update the `task_list.html` again:

```
{% if request.user.is_authenticated %}
    <p>{{request.user}}</p>
    <a href="{% url 'logout' %}">Logout</a>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}

```


<a name="retrictDataWithoutLogin"></a>
## Retrict data access without login
To make sure each page cannot be accessed by typing in the url path directly without logging in, we use the `LoginRequiredMixin`.  In `views.py`, import it and use in all classes we want to retrict:

```
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

...

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    contex_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    contex_object_name = 'task'
    success_url = reverse_lazy('tasks')
    
```
Now if you try to access those pages without logging in, it will say "page not found".

We need to let the user know where to redirect the user if the user is not authenicated. so in `settings.py`, at the bottom above `STATIC_URL`, add:

```
LOGIN_URL = 'login'

...

STATIC_URL = 'static/'

```

<a name="retrictUser"></a>
## Retrict each user can only see his own items
We want to make sure dennis can only see dennis's item, and john can only see john's item. in `views.py`, add a `def` under `TaskList`

```
class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context
```
now each user can only see his/her own list.

<a name="removeUserField"></a>
## Remove the select user field in create form
Right now in the create form, users can still be selected.  We want to remove that and make sure the item is added to the logged in user.
in `views.py`, add a `def` and change the fields from `__all__` to `'title', 'description', 'complete'` (exclude the user)

```
class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
```
in `TaskUpdate` we also want to remove the user field

```
class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
```


<a name="registerUser"></a>
## Register User
Let's create a register page where new account can be created.
go to `login.html`, add the register link

```
<h1>login</h1>

<form method = "POST">
...
</form>

<p>Don't have an account? <a href="">Register</a></p>
```

Create a new file `register.html`, copy and paste everything from the `login.html` and change a few things.

```
<h1>Register</h1>

<form method = "POST">
    {% csrf_token %}
    {{form.as_p}}
    <input type="submit" value="Register">
</form>

<p>Already have an account? <a href="{% url 'login' %}">Login</a></p>
```
in `views.py` import `FormView` `UserCreationForm` `login`

```
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
```
add a new class `RegisterPage`

```
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
```

in `urls.py`

```
...
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
...
urlpatterns = [
    ...
    path('register/', RegisterPage.as_view(), name='register'),
    ...]

```
add back the register link in `login.html`

```
<p>Don't have an account? <a href="{% url 'register' %}">Register</a></p>
```
New user can now be created.  There is just 1 more thing, login user can still be able to access `register.html` by typing in the url. we want to block that and redirect user to `task_list.html` when they try. 

* Import `redirect` 
* and add 1 more `def` to `RegisterPage`.

```
from django.shortcuts import render, redirect
...
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

```

<a name=""></a>
## Search Item
to create a search box, in `task_list.html`, and a GET form

```
...
<h1>My To Do List</h1>
<a href="{% url 'task-create' %}">Add Task</a>

<form method="GET">
    <input type='text' name='search-area' value="{{search_input}}">
    <input type="submit" value='Search'>
</form>

<table>
...
```
in `views.py` add the following lines to the `TaskList``def`section

```
class TaskList(LoginRequiredMixin,ListView):
    ...

    def get_context_data(self, **kwargs):
        ...

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            
        context['search_input'] = search_input
        return context

```

<a name=""></a>
## Remove the View button in the list
in `task_list.html` remove the line:
` <td><a href="{% url 'task' task.id %}">View</a></td>`


<a name=""></a>
## Create a base html, to let all html inherite from 
Create a new html `main.html`, add a div and a block, also a background color for testing.

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>To Do Items</title>

    <style>
      body{
        background-color: aqua;
      }
    </style>
</head>
<body>
  <div class="container">
    {% block content %}

    {% endblock content %}
  </div>

</body>
</html>
```
at the very top of `task_list.html`, add 

```
{% extends 'base/main.html' %}
{% block content %}

{% endblock content %}
```
then cut and paste everything into this block.  runserver to see the background is now change to aqua. Now you can do the same to all other pages (login / register / task_confirm_delete / task_form ) No need to do task.html since we won't use that page.


<a name=""></a>
## Style the fonts
google 'google fonts', lets use 'nunito' font, select 'ExtraLight200', copy and paste the link inside `<head>` in our `main.html`.
Also we want to add some CSS styling inside `<head>`:

```
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@200&display=swap" rel="stylesheet">
    
<style>
      body{
        background-color: #FAFAFA;
        font-family: 'Nunito', sans-serif;
        padding-top: 50px;
        -webkit-box-shadow: 2px 2px 13px -4px rgba(0,0,0,0.21);
        box-shadow: 2px 2px 13px -4px rbga(0,0,0,0.21);
      }

      h1,h2,h3,h4,h5,h6,{
        font-family: 'Raleway', sans-serif;
      }

      a,p{
        color: #4b5156
      }

      .container{
        max-width: 550px;
        margin: auto;
        background-color: #fff;
      }
    </style>
```
    

<a name=""></a>
## Count uncompleted tasks
in `task_list.html`, create a div:

```
<div class="header-bar">
    <div>
        <h1>Hello {{request.user|title}}</h1>
        <h3 style="margin:0">You have <i>{{count}}</i> incomplete task{{count|pluralize:"s"}}</h3>
    </div>
</div>
```
`|title` gives the first letter capital, `|pluralize` to add "s" if it is plural.

Move login/logout button inside the div and remove the dupublicated `request.user`

```
<div class="header-bar">
    <div>
        <h1>Hello {{request.user|title}}</h1>
        <h3 style="margin:0">You have <i>{{count}}</i> incomplete task{{count|pluralize:"s"}}</h3>
    </div>
    {% if request.user.is_authenticated %}
    <a href="{% url 'logout' %}">Logout</a>
    {% else %}
    <a href="{% url 'login' %}">Login</a>
    {% endif %}
</div>
```

<a name=""></a>
## Style "header-bar" with CSS
add this to the css in `main.html` to style the div class above.

```
      .header-bar {
        display: flex;
        justify-content: space-between;
        color: #fff;
        padding: 10px;
        border-radius: 5px 5px 0 0;
        background: linear-gradient(90deg, #EEA390 0%, #EB796F 43%, #EB796F 100%);
      }
      
      .header-bar a{
        color: rgb(247,247,247);
        text-decoration: none;
      }
```

<a name=""></a>
## Style the table
still in `task_list.html`, first comment out the search bar, then remove this

```
<hr>
<h1>My To Do List</h1>
```
replace the table with the following:

```
<div class=""task-items-wrapper">
    {% for task in tasks %}
        <div class="task-wrapper">
            {% if task.complete %}
                <div class="task-title">
                    <div class="task-complete-icon"></div>
                    <i><s><a href="{% url 'task-update' task.id %}">{{task}}</a></s></i>
                </div>
                <a class="delete-link" href="{% url 'task-delete' task.id %}">&#215;</a>
            {% else %}
                <div class="task-title">
                    <div class="task-incomplete-icon"></div>
                   <a href="{% url 'task-update' task.id %}">{{task}}</a>
                </div>
                <a class="delete-link" href="{% url 'task-delete' task.id %}">&#215;</a>
            {% endif %}

        </div>
    {% empty %}
        <h3> No items in list</h3>
    {% endfor%}
</div>
```
`&#215;` is html code for x symobol, can google "html symbols" for more referrence.

for the table's CSS part, add these:

```

      .task-wrapper {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px;
        background-color: #fff;
        border-top: 1px solid rgb(226,226,226);
      }

      .task-title {
        display: flex;
      }

      .task-title a {
        text-decoration: none;
        color: #4b5156;
        margin-left: 10px;
      }

      .task-complete-icon {
        height: 20px;
        width: 20px;
        background-color: rgb(105,192,105);
        border-radius: 50%;
      }

      .task-incomplete-icon {
        height: 20px;
        width: 20px;
        background-color: rgb(218,218,218);
        border-radius: 50%;
      }

      .delete-link {
        text-decoration: none;
        font-weight: 900;
        color: #cf4949;
        font-size: 22px;
        line-height: 0;
      }
```

<a name=""></a>
## Style the search bar
replace the search bar with:

```
<div id="search-add-wrapper">
    <form method="GET" style="margin-top: 20px; display: flex;">
        <input type='text' name='search-area' value="{{search_input}}">
        <input class="button' type="submit" value='Search'>
    </form>
    <a id="add-link" href="{% url 'task-create' %}">&#x2b;</a>
</div>
```
the CSS with be:

```

      #search-add-wrapper{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
      }

      #add-link {
        color: #EB796F;
        text-decoration: none;
        font-size: 42px;
        text-shadow: 1px 1px #81413b;
      }

      input[type=text],
      input[type=password],
      textarea {
        border: 1px solid #EB796F;
        border-radius: 5px;
        padding: 10px;
        width: 90%
      }

      label {
        padding-top: 10px !important;
        display: block;
      }

      .button {
        border: 1px solid #EB796F;
        background-color: #FAFAFA;
        color: #EB796F;
        padding: 10px;
        font-size: 14px;
        border-radius: 5px;
        cursor: pointer;
        text-decoration: none;
      }
```
<a name=""></a>
## Style task_form.html
put everything in `task_form.html` into div

```
<div class="header-bar">
   <a href="{% url 'tasks' %}">&#8592; Back</a>
</div>

<div class="card-body">
    <form method="post", action="">
    {% csrf_token %}
    {{form.as_p}}
    <input class="button" type="submit" value="Submit">
    </form>
</div>

```
CSS:

```
.card-body {
        padding: 20px;
      }
```
<a name=""></a>
## Style task_confirm_delete.html
do the same, put everything in div `header-bar` and `card-body`. Add `class="button"` to button

```
<div class="header-bar">
   <a href="{% url 'tasks' %}">&#8592; Back</a>
</div>

<div class="card-body">
    <form method = "POST">
    {% csrf_token %}
    <p>Are you sure you want to delete this task? "{{task}}"</p>
    <input class="button" type="submit" value="Delete"/>
    </form>
</div>

```

<a name=""></a>
## Style login.html
same

```
<div class="header-bar">
<h1>login</h1>
</div>

<div class="card-body">
    <form method = "POST">
    {% csrf_token %}
    {{form.as_p}}
    <input class="button" type="submit" value="Login">
    </form>
    <p>Don't have an account? <a href="{% url 'register' %}">Register</a></p>
</div>
```

<a name=""></a>
## style register.html
same

```
<div class="header-bar">
<h1>Register</h1>
</div>

<div class="card-body">
    <form method = "POST">
        {% csrf_token %}
        {{form.as_p}}
        <input class="button" type="submit" value="Register">
    </form>
    <p>Already have an account? <a href="{% url 'login' %}">Login</a></p>
</div>
```
to make the fields look better, we can replace `form.as_p` with :

```
{% extends 'base/main.html' %}
{% block content %}

<div class="header-bar">
<h1>Register</h1>
</div>

<div class="card-body">
    <form method = "POST">
        {% csrf_token %}

        <label>{{form.username.label}}</label>
        {{form.username}}

         <label>{{form.password1.label}}</label>
        {{form.password1}}

         <label>{{form.password2.label}}</label>
        {{form.password2}}


<!--        {{form.as_p}}-->
        <input style ="margin-top: 10px" class="button" type="submit" value="Register">
    </form>
    <p>Already have an account? <a href="{% url 'login' %}">Login</a></p>
</div>

{% endblock content %}

```
added a little margin above the button too.






<a name=""></a>
## The END
--

