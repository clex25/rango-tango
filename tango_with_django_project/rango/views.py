from django.shortcuts import render

from django.http import HttpResponse
from rango.models import Category, Page


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
        
    except Category.DoesNotExist:
        #no category Found, display default Message
        pass
    
    return render(request, 'rango/category.html', context_dict)
