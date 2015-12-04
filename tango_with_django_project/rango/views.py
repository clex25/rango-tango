from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    #construct dictionary to pass to template
    context_dict = {'boldmessage': "I am bold from the context"}
    
    #return a rendered response to send to client, using our index template
    return render(request, 'rango/index.html', context_dict)
    
def about(request):
    #construct dictionary to pass to template
    context_dict = {'boldmessage': "cool"}
    
    #return a rendered response to send to client, using our index template
    return render(request, 'rango/about.html', context_dict)
