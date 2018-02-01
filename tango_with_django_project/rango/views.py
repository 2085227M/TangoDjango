from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm

def index(request):
    #context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    category_list = Category.objects.order_by('-likes')[:5]

    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    #context_dict['pages'] = pages
    #context_dict['category'] = category
    response = render(request, 'rango/index.html', context=context_dict)
    return response

def about(request):
    context_dict = {'boldmessage': "Johnny Depp played Rango the Chameleon in the movie, here he is in character"}
    return render(request, 'rango/about.html', context=context_dict)
    #return HttpResponse("Rango says here is the about page. <a href='/rango/'>View Index Page</a>")

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        #Have we been provided a valid form?
        if form.is_valid():
            #Save the new category to the database
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form':form})
