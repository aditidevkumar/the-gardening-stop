from django.shortcuts import render,redirect,get_object_or_404
from django.views import View 
from .models import Product,Customer,Cart,Order,OrderItem,Wishlist,VisitHistory
from django.http import JsonResponse
from .forms import ContactForm,CustomerRegistrationForm, CustomerProfileForm,SearchForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
import difflib

from random import sample
# Create your views here.

def home(request):
    totalitem =0 
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    return render(request,'home.html',locals())
   
def about(request):
    totalitem =0 
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    return render(request,'about.html',locals())


class CategoryView(View):
    
    def get(self, request, val=None):
        totalitem =0 
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            product = Product.objects.filter(category=val).values('title', 'discounted_price', 'selling_price', 'product_image')
            product_list = list(product)
            return JsonResponse({'product': product_list})
        else:
            product = Product.objects.filter(category=val)
            title = Product.objects.filter(category=val).values('title')
            return render(request, 'category.html', locals())
        
class CategoryTitle(View):
    def get(self,request,val):
        totalitem =0 
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request,'category.html',locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        if isinstance(request.user, AnonymousUser):
            return redirect('login')
        else:
            product = Product.objects.get(pk=pk)
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))

        totalitem =0 
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        return render(request,'productdetail.html',locals()) 
    
def all_plants_view(request):
    totalitem =0 
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    products = Product.objects.all()
    categories = Product._meta.get_field('category').choices  
    return render(request, 'all_plants.html', {'product': products, 'categories': categories})

def contact_view(request):
    totalitem =0 
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    
    return render(request, 'contact.html',locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created!{username}!')
            return redirect('register')  
        else:
            messages.warning(request, 'Invalid Input Data')
        
        return render(request, 'register.html', {'form': form})

class ProfileView(View):
    def get(self,request):
        totalitem =0 
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        form=CustomerProfileForm()
        return render(request,'profile.html',locals())
    def post(self,request):
        form =CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            pincode=form.cleaned_data['pincode']
            reg= Customer(user=user,name=name,city=city,state=state,pincode=pincode,mobile=mobile)
            reg.save()
            messages.success(request,"Congratulations! Profile successfully updated")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'profile.html',locals())
    
def address(request):
    totalitem =0 
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    add = Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())

class updateAddress(View):
    def get(self,request,pk):
        totalitem =0 
        if request.user.is_authenticated:
            totalitem= len(Cart.objects.filter(user=request.user))
        add = Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add)
        return render(request,'updateAddress.html',locals())
    
    def post(self,request,pk):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name=form.cleaned_data['name']
            add.city=form.cleaned_data['city']
            add.mobile=form.cleaned_data['mobile']
            add.state=form.cleaned_data['state']
            add.pincode=form.cleaned_data['pincode']
            add.save()
            messages.success(request,"Congratulations! Profile successfully updated")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect('address')  
          
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')  
    return redirect('home')   
    

def add_to_cart(request):
        user = request.user
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        
        Cart(user=user,product=product).save()
        return redirect('/cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        
        if p.product.category in ['Soil', 'Tool', 'Seed', 'AG']:
           
            value = p.quantity * (p.product.selling_price or 0)
        else:
            
            value = p.quantity * (p.product.discounted_price or 0)
        
        amount += value
    totalamount = amount + 40
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(cart)
    return render(request, 'addtocart.html', locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        print(prod_id)
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value =p.quantity * p.product.discounted_price
            amount=amount + value
        totalamount=amount + 40
        data={ 'quantity':c.quantity,
              'amount':amount,
              'totalamount':totalamount,
        }
    return JsonResponse(data)

def remove_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount=amount + value
        totalamount=amount + 40
        data={ 
              'amount':amount,
              'totalamount':totalamount
        }
    return JsonResponse(data)
   
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        user = request.user
        
        try:
            # Get the cart item for the specific user and product
            cart_item = Cart.objects.get(Q(product=prod_id) & Q(user=user))
            
            # Only decrease quantity if it's greater than 1
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            
            # Calculate cart total and amount
            cart = Cart.objects.filter(user=user)
            amount = sum(p.quantity * p.product.discounted_price for p in cart)
            totalamount = amount + 40  # Including a flat shipping fee
            
            data = {
                'quantity': cart_item.quantity,  # Sending the updated quantity
                'amount': amount,
                'totalamount': totalamount,
            }
            return JsonResponse(data)

        except Cart.DoesNotExist:
            return JsonResponse({'error': 'Item not found in cart'}, status=404) 


class checkout(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)  # Fetch customer addresses
        cart_items = Cart.objects.filter(user=user)  # Fetch cart items
        famount = 0
        
        for p in cart_items:
            if p.product.category in ['Soil', 'Tool', 'Seed', 'AG']:
                value = p.quantity * (p.product.selling_price or 0)
            else:
                value = p.quantity * (p.product.discounted_price or 0)
            famount += value
        
        totalamount = famount + 40  # Adding delivery charge
        return render(request, 'checkout.html', {
            'add': add,
            'cart_items': cart_items,
            'totalamount': totalamount,
            'totalitem': totalitem
        })
    
    def post(self, request):
        user = request.user
        totalamount = request.POST.get('totalamount')  # Retrieve total amount from hidden field
        
        # Create the order (no address check)
        order = Order.objects.create(
            user=user,
            total_price=totalamount,
            status='Pending',
        )
        
        # Transfer items from cart to order
        cart_items = Cart.objects.filter(user=user)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
        
        # Clear the cart after order is placed
        cart_items.delete()
        
        # Redirect to an order success page (or payment page)
        return redirect('checkout_success')

     

def checkout_success(request):
    return render(request,'checkout_success.html',locals())

@login_required
def orders(request):
    totalitem =0 
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders.html', locals())

@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        user = request.user

        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
        
        if created:
            return JsonResponse({'message': 'Added to Wishlist Successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Item already in Wishlist'}, status=200)

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = get_object_or_404(Product, id=prod_id)
        user = request.user

        wishlist_item = Wishlist.objects.filter(user=user, product=product)
        if wishlist_item.exists():
            wishlist_item.delete()
            return JsonResponse({'message': 'Removed from Wishlist Successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Item not found in Wishlist'}, status=404)
        
def wishlist_view(request):
    user = request.user
    totalitem =0 
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    wishlist_items = Wishlist.objects.filter(user=user)  
    return render(request, 'wishlist.html',locals())

def product_search(request):
    totalitem =0 
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))
    query = request.GET.get('query', '').strip()
    products = []
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(botanical_name__icontains=query) | Q(category__icontains=query) | Q(selling_price__icontains=query)
        )

        if not products.exists():
            all_titles = Product.objects.values_list('title', flat=True)  # Get all product titles
            close_matches = difflib.get_close_matches(query, all_titles, n=5, cutoff=0.6)  
            products = Product.objects.filter(title__in=close_matches)
        
        if request.user.is_authenticated and products.exists():
            
            first_product = products.first() 
            SearchHistory.objects.create(user=request.user, query=query, product=first_product)

    return render(request, 'product_search.html',{'products': products, 'query': query})

'''from django.shortcuts import render
from .models import Wishlist, Product, VisitHistory, SearchHistory, Cart
from random import sample

def recommendation(request):
    user = request.user
    totalitem = 0 

    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=user))

        # Fetch products from the user's wishlist
        wishlist_items = Wishlist.objects.filter(user=user).values_list('product', flat=True)

        # Fetch products from the user's visit history
        visited_items = VisitHistory.objects.filter(user=user).values_list('product', flat=True)

        # Fetch products from the user's search history
        search_history = SearchHistory.objects.filter(user=user).values_list('product', flat=True)

        # Create a combined queryset for recommended products
        recommended_products = Product.objects.none()

        # Add recently searched products first
        if search_history.exists():
            search_history_products = Product.objects.filter(id__in=search_history)
            recommended_products = recommended_products | search_history_products

        # Add recently visited products next
        if visited_items.exists():
            visited_products = Product.objects.filter(id__in=visited_items)
            recommended_products = recommended_products | visited_products

        # Add products from the wishlist
        if wishlist_items.exists():
            wishlist_products = Product.objects.filter(id__in=wishlist_items)
            recommended_products = recommended_products | wishlist_products

        # Fetch random products from the cart
        cart_items = Cart.objects.filter(user=user).values_list('product', flat=True)
        cart_items_random = list(cart_items)
        
        if cart_items_random:
            random_cart_items = sample(cart_items_random, min(2, len(cart_items_random)))
        else:
            random_cart_items = []

        # Combine cart items with other combined items
        combined_items = set(recommended_products.values_list('id', flat=True)) | set(random_cart_items)

        # Fetch product details, ensuring uniqueness, and order by descending
        recommended_products = Product.objects.filter(id__in=combined_items).distinct().order_by('-id')[:12]  # Limit to 12 products

        # Update the visit history to include the current product
        current_product_id = request.GET.get('product_id')  # Assuming the product ID is passed in the request
        if current_product_id and current_product_id not in visited_items:
            # Record the visit if it's a new product
            VisitHistory.objects.create(user=user, product_id=current_product_id)

        context = {
            'recommended_products': recommended_products,
            'totalitem': totalitem
        }

        return render(request, 'recommendation.html', context)

    # Handle unauthenticated users
    return render(request, 'recommendation.html', {'recommended_products': [], 'totalitem': totalitem})
'''

from django.shortcuts import render
from .models import Wishlist, Product, VisitHistory, SearchHistory, Cart
from random import sample

def recommendation(request):
    user = request.user
    totalitem = 0

    if user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=user))

        # Fetch recent items from Wishlist, VisitHistory, and SearchHistory based on 'timestamp'
        wishlist_items = Wishlist.objects.filter(user=user).order_by('-timestamp').values_list('product', flat=True)
        visited_items = VisitHistory.objects.filter(user=user).order_by('-timestamp').values_list('product', flat=True)
        search_history = SearchHistory.objects.filter(user=user).order_by('-timestamp').values_list('product', flat=True)

        # Combine unique product IDs, prioritizing the most recent interactions
        combined_product_ids = list(set(list(wishlist_items) + list(visited_items) + list(search_history)))

        # Limit combined list to ensure only five items are recommended
        if len(combined_product_ids) > 5:
            combined_product_ids = sample(combined_product_ids, 5)
        else:
            # If fewer than 5 items, use as many as available
            combined_product_ids = combined_product_ids[:5]

        # Fetch product details for the recommended items
        recommended_products = Product.objects.filter(id__in=combined_product_ids)

        # Optionally update VisitHistory with currently viewed product
        current_product_id = request.GET.get('product_id')
        if current_product_id and int(current_product_id) not in visited_items:
            VisitHistory.objects.create(user=user, product_id=current_product_id)

        context = {
            'recommended_products': recommended_products,
            'totalitem': totalitem
        }

        return render(request, 'recommendation.html', context)

    # Handle unauthenticated users
    return render(request, 'recommendation.html', {'recommended_products': [], 'totalitem': totalitem})
