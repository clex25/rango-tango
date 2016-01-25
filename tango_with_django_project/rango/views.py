from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import urlparse
from datetime import datetime #for cookies last_visit

def index(request):
    #Query DB for all categories. Show top 5 by likes in desc order
    #construct dictionary to pass to template
    context_dict = {}
    category_list = Category.objects.order_by('-likes')[:5]
    
    context_dict['categories'] = category_list
    
    #use cookies to get the number of visits to the site
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False
    
    #get top 5 pages
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
    
    #check if last visit cookie exists, if not, create it
    last_visit = request.session.get('last_visit')
    if last_visit:
        # Cast the value to a Python date/time object.
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        # If it's been more than a day since the last visit...
        if (datetime.now() - last_visit_time).days > 0:
            visits = visits + 1
            # ...and flag that the cookie last visit needs to be updated
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so flag that it should be set.
        reset_last_visit_time = True   
        #Obtain our Response object early so we can add cookie information.
        

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
        
    context_dict['visits'] = visits
    
    response = render(request, 'rango/index.html', context_dict)
    return response
   

def about(request):
    #construct dictionary to pass to template
    context_dict = {'boldmessage': "cool"}
    
    visits = request.session.get('visits')
    if not visits:
        visits = 1
        
    context_dict['visits'] = visits
    #return a rendered response to send to client, using our index template
    return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):
    #rendering engine context dict
    context_dict = {}
    
    try:
        #try to find a category name slug
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        
        #get all the pages for that category
        pages = Page.objects.filter(category=category)
        
        context_dict['pages'] = pages
        
        context_dict['category'] = category
        
        context_dict['category_name_slug'] = category_name_slug
        
    except Category.DoesNotExist:
        #no category Found, display default Message
        pass
    
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
                form.save(commit=True) 
                return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    
    return render(request, 'rango/add_category.html',{'form':form})
  
@login_required
def add_page(request, category_name_slug):
    
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None
    
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()
    
    context_dict = {'form':form, 'category':cat, 'category_name_slug':category_name_slug}
    
    return render(request, 'rango/add_page.html', context_dict)


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})




    
