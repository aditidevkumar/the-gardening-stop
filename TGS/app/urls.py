from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import LogoutView

from .forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MySetPasswordForm

urlpatterns =[
    path('',views.home,name='home'),

    path('home',views.home,name='home'),

    path('about',views.about,name='about'),

    path('contact/', views.contact_view, name='contact'),

    path('register/',views.CustomerRegistrationView.as_view(),name='register'),

    path('login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),

    path('profile/',views.ProfileView.as_view(),name='profile'),

    path('address/',views.address,name='address'),

    path('updateAddress/<int:pk>',views.updateAddress.as_view(),name='updateAddress'),

#change password

    path('passwordchange/', auth_view.PasswordChangeView.as_view(
        template_name='changepassword.html',
        form_class=MyPasswordChangeForm,
        success_url=reverse_lazy('passwordchangedone')  
    ), name='passwordchange'),

    path('passwordchange/done/', auth_view.PasswordChangeDoneView.as_view(
        template_name='passwordchangedone.html'
    ), name='passwordchangedone'),

    path('password-reset/', auth_view.PasswordResetView.as_view(
        template_name='password_reset.html',
        form_class=MyPasswordResetForm
    ), name='password_reset'),


    path('logout/', views.logout_view, name='logout'),

    # #reset password
    path('password-reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),

    path('password-reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    


   path('product-detail/<int:pk>',views.ProductDetail.as_view(),name='product-detail'),

    path('category-title/<val>/',views.CategoryTitle.as_view(),name='category-title'),
    
    path('category/<slug:val>/',views.CategoryView.as_view(),name='category'),
    
    path('plants/', views.all_plants_view, name='all-plants'),

    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),

    path('cart/',views.show_cart,name='show_cart'),

    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart',views.remove_cart),

    # path('minuswishlist/',views.minus_wishlist),
    # path('pluswishlist/',views.plus_wishlist),
    path('wishlist/add/', views.plus_wishlist, name='plus_wishlist'),
    path('wishlist/remove/', views.minus_wishlist, name='minus_wishlist'),

    path('wishlist/', views.wishlist_view, name='wishlist'),

    path('checkout/', views.checkout.as_view(),name='checkout'),
    path('checkout_success/', views.checkout_success, name='checkout_success'),
    path('orders/', views.orders, name='orders'),
    
    path('search/', views.product_search, name='product_search'),
    path('recommendation/', views.recommendation, name='recommendation'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
