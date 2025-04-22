from django.db.models import Q
from django.shortcuts import render, redirect
from products.models import Product,Category
from django.contrib.auth import authenticate, login as login_auth
from .forms import RegisterForm
from users.models import Member
import random

#class IndexView(TemplateView):
    #template_name = 'users/index.html'

def index(request):
    # 只獲取 is_show=True 且 parent=None 的產品，然後隨機取8個
    all_products = list(Product.objects.filter(is_show=True, parent=None))
    random_products = random.sample(all_products, min(8, len(all_products)))
    return render(request, 'users/index.html', {'products': random_products})

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        address = form.cleaned_data.get('address', '')  # 假設表單有 address 字段
        Member.objects.create(user=user, email=user.email, address = address)
        login_auth(request, user)
        return redirect('index')
    
    #context = { 'form': form}

    return render(request, 'users/signup.html',  {'form': form})

#def login(request):
    #if request.method == "POST":
        #username = request.POST.get("username")
        #password = request.POST.get("password")
        #user = authenticate(request, username=username, password=password)
        #if user is not None:
            #login_auth(request, user)
            #return redirect('index')
    #return render(request, "users/login.html")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login_auth(request, user)
            
            # 根据用户选择信任浏览器与否动态设置会话
            if request.POST.get('trust_browser', False):
                # 信任浏览器：长期保持（例如30天）
                request.session.set_expiry(30 * 24 * 60 * 60)  # 30天
                request.session['trusted_browser'] = True
            else:
                # 不信任：15分钟无操作后过期 + 关闭浏览器失效
                request.session.set_expiry(900)  # 15分钟
                request.session['trusted_browser'] = False
            
            return redirect('index')
    return render(request, 'users/login.html')

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
