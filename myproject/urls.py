
from django.contrib import admin
from django.urls import path,include

#from cart.views import add_to_cart,cart
#from users import views
#from users.views import index,product
#from products.views import product_detail
#from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('users.urls')),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('admin/', admin.site.urls),
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
