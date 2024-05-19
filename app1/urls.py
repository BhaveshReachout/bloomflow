from django.urls import path
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('index/', views.home, name='index'),
    path('', RedirectView.as_view(url='index')),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_view, name='register'),
    path('product_page/<int:id>/', views.product_page, name='detail'),
    path('plants/', views.plants_view, name='plants'),
    path('plants/detail/<int:id>/', views.plants_detail_view, name='plants_detail'),
    path('order/', views.order_view, name='order'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:id>/', views.tempo_view, name='cart_add'),
    path('cart/remove/<int:id>/', views.cart_remove_view, name='remove_cart'),
    path('checkout/', views.checkout_view, name='placeorder'),
    path('callback/', views.callback, name='callback'),
    path('search/', views.SearchProductView.as_view(), name='search'),
    path('pdf/', views.GeneratePDF.as_view(), name='PdfView'),
    path('caretools/', views.caretools_view, name='caretools'),
    path('caretools_product/', views.caretools_product_view,
         name='caretools_product'),
    path('learn/', views.learn_view, name='learn'),
    path('gifts/', views.gifts_view, name='gifts'),
    path('gifts_product/', views.gifts_product_view, name='gifts_product'),
    path('profile/', views.profile_final_view, name='profile_final'),
    path('profile/edit/', views.profile_final_edit_view, name='profile_edit_final'),
    path('contact_us/', views.contact_us_view, name='contact_us'),
    path('about_us/', views.about_us_view, name='about_us'),
]
