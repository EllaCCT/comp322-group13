from django.db.models import Q
from django.shortcuts import render, redirect
from products.models import Product,Category
from django.contrib.auth import authenticate, login as login_auth
from .forms import RegisterForm
from users.models import Member

#class IndexView(TemplateView):
    #template_name = 'users/index.html'

def index(request): 
    products=Product.objects.all()[0:8]
    return render(request, 'users/index.html', {'products':products})

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        address = form.cleaned_data.get('address', '')  # 假設表單有 address 字段
        Member.objects.create(user=user, email=user.email, address=address)
        login(request, user)
        return redirect('index')
    
    #context = { 'form': form}

    return render(request, 'users/signup.html',  {'form': form})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login_auth(request, user)
            return redirect('index')
    return render(request, "users/login.html")
    

def product(request):
    categories=Category.objects.all()
    products=Product.objects.all()

    ###該分類內的玩具
    active_category = request.GET.get('category', '')
    if active_category:
        products = products.filter(category__slug=active_category)

    query=request.GET.get('query','')
    
    if query: ##搜尋可以透過搜尋商品名稱或描述
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query)| Q(price__icontains=query))
            
        
    ###

    content = {
        'categories':categories,
        'products':products
    }

    return render(request, 'users/product.html', content)
