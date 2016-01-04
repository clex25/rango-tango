from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import urlparse


def index(request):
    #Query DB for all categories. Show top 5 by likes in desc order
    #construct dictionary to pass to template
    context_dict = {}
    category_list = Category.objects.order_by('-likes')[:5]
    
    context_dict['categories'] = category_list
    
    #get top 5 pages
    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list
         
    #return a rendered response to send to client, using our index template
    return render(request, 'rango/index.html', context_dict)
    
def about(request):
    #construct dictionary to pass to template
    context_dict = {'boldmessage': "cool"}
    
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

def register(request):
    
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            
            registered = True
            
        else:
            print user_form.errors, profile_form.errors
    # not a post, so display the form   
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render( request, 'rango/register.html',
                   {'user_form' : user_form, 'profile_form' : profile_form, 'registered' : registered} )
    
def user_login(request):
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request,user)
                
                #check if it is an absolute url, or empty. don't redirect to other sites.
                next = request.POST.get('next','')
                print('next' + next)             
                if bool(urlparse.urlparse(next).netloc) or next.startswith('www') or next == '':
                    next = '/rango/'
                
                return HttpResponseRedirect(next)
            
            #disabled account
            else:
                return HttpResponse("Your account is currently disabled.")
        # not valid password
        else:
            print "Invalid username or password"
            return HttpResponse("Invalid username or password")
    #not a post
    else:
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/rango/')


    
