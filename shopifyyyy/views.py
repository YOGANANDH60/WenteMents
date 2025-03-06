from django.shortcuts import render,redirect,get_object_or_404,HttpResponse 
from .models import *
from django.contrib import messages
from .form import customeuserform
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


# Create your views here.

def home(request):
    products = product.objects.filter(trending=1)
    categories = category.objects.filter(status=0)

    fav_count = 0
    if request.user.is_authenticated:
        fav_count = fav.objects.filter(User=request.user).count()

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = cart.objects.filter(User=request.user).count()

    return render(request, "shop/index.html", {
        'products': products, 
        'categories': categories, 
        'fav_count': fav_count, 
        'cart_count': cart_count

    })

def login_page(request):
    categories = category.objects.filter(status=0)
    if request.user.is_authenticated:
         return redirect("/home")
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"login successfully")
                return redirect('/home')
            else:
                messages.error(request,"invalid username or pasword")
                return redirect("/login")
        return render(request,"shop/login.html",{'categories': categories})

def register(request):
    categories = category.objects.filter(status=0)
    form = customeuserform()
    if request.method=='POST':
        form=customeuserform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"registration success you can login noe...!")
            return redirect('/login')
    return render(request,"shop/register.html",{'form':form,'categories': categories})

def logout_page(request):
    if request.user.is_authenticated:  
        logout(request)
        messages.success(request, "Logout successful") 
    return redirect('/home')


def categories(request):
    categories = category.objects.filter(status=0)   
    fav_count = 0
    if request.user.is_authenticated:
        fav_count = fav.objects.filter(User=request.user).count()
        
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = cart.objects.filter(User=request.user).count()
    return render(request, "shop/category.html", {'categories': categories , 'fav_count': fav_count, 'cart_count': cart_count})     

def productdetails(request,name):
    categories = category.objects.filter(status=0)
    fav_count = 0
    if request.user.is_authenticated:
        fav_count = fav.objects.filter(User=request.user).count()
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = cart.objects.filter(User=request.user).count()
    if(category.objects.filter(name=name,status=0)):
         productdetails = product.objects.filter(category__name=name) 
         return render(request, "shop/productdetails.html", {'productdetails': productdetails,'categories': categories, 'fav_count': fav_count, 'cart_count': cart_count})
    else:
        messages.warning(request,"no such category found")
        return redirect('category')  

def single_productdetails(request, cname, spname):
    categories = category.objects.filter(status=0)  
    fav_count = 0
    final_price = None  

    if request.user.is_authenticated:
        fav_count = fav.objects.filter(User=request.user).count()

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = cart.objects.filter(User=request.user).count()

    # Check if category exists
    if category.objects.filter(name=cname, status=0).exists():
        products = get_object_or_404(product, pname=spname)
        sideimg = productImages.objects.filter(product=products)

        # Check if the user has a successful negotiated price
        if request.user.is_authenticated:
            negotiation = Negotiation.objects.filter(user=request.user, product=products, is_successful=True).first()
            if negotiation:
                final_price = negotiation.current_offer  # Use negotiated price

        context = {
            'products': products,
            'sideimg': sideimg,
            'categories': categories,
            'fav_count': fav_count,
            'cart_count': cart_count,
            'final_price': final_price if final_price else products.nprice,  # Pass negotiated price if available
        }
        return render(request, 'shop/single_productdetails.html', context)
    else:
        messages.error(request, "No such category found")
        return redirect('category')  


@login_required
def negotiate(request, product_name):
    product_obj = get_object_or_404(product, pname=product_name)
    categories = category.objects.filter(status=0)
    user = request.user

    # Check if user has an existing successful negotiation
    negotiation = Negotiation.objects.filter(user=user, product=product_obj, is_successful=True).first()
    
    if negotiation:
        final_price = negotiation.final_price  # Use the negotiated price
    else:
        final_price = product_obj.nprice  # Default price

    if product_obj.nprice < 1000:
        messages.warning(request, "Negotiation is only available for products priced above 1000.")
        return redirect('productdetails', name=product_obj.category.name)

    negotiation_result = None
    counter_offer = None

    if request.method == "POST":
        user_offer = float(request.POST.get("user_offer", 0))

        if user_offer >= product_obj.nprice * 0.9:
            negotiation_result = "accepted"
            final_price = user_offer

            # Store successful negotiation
            negotiation, created = Negotiation.objects.get_or_create(user=user, product=product_obj)
            negotiation.current_offer = user_offer
            negotiation.final_price = user_offer
            negotiation.is_successful = True
            negotiation.save()

        elif user_offer >= product_obj.nprice * 0.8:
            counter_offer = round(product_obj.nprice * 0.9, 2)
            negotiation_result = "counter"
        else:
            negotiation_result = "rejected"

    return render(request, "shop/negotiate.html", {
        "product": product_obj,
        "final_price": final_price,
        "negotiation_result": negotiation_result,
        "counter_offer": counter_offer,
        'categories': categories
    })

def blog(request):
    blog = articals.objects.all()
    categories = category.objects.filter(status=0)
    fav_count = 0
    if request.user.is_authenticated:
        fav_count = fav.objects.filter(User=request.user).count()
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = cart.objects.filter(User=request.user).count()
    return render(request, "shop/blog.html", {'blog': blog,'categories': categories, 'fav_count': fav_count, 'cart_count': cart_count})


def about(request):
    categories = category.objects.filter(status=0)
    fav_count = 0
    if request.user.is_authenticated:
        fav_count = fav.objects.filter(User=request.user).count()
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = cart.objects.filter(User=request.user).count()
    return render(request, "shop/about.html",{'categories': categories, 'fav_count': fav_count, 'cart_count': cart_count})


def search_view(request):

    categories = category.objects.filter(status=0)
    query = request.GET.get('search')
    if query:
        productdetails = product.objects.filter(pname__icontains=query)
        if productdetails:
            return render(request, 'shop/productdetails.html', {'productdetails': productdetails,'categories': categories})
        else:
            messages.error(request, "No such product found")
            return redirect('home')
    else:
        return redirect('home')


def logout(request):
    return redirect('home')


def add_to_cart(request):
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            
            try:
                body = request.body.decode('utf-8')
                print("Raw Request Body:", body)  # Debugging: Print request body

                data = json.loads(body)
                print("Parsed Data:", data)  # Debugging: Print parsed data

                # ✅ Ensure correct key names
                if 'pid' not in data or 'product_qty' not in data:
                    return JsonResponse({'status': 'missing required fields'}, status=400)

                product_id = data['pid']
                product_qty = data['product_qty']

                product_instance = get_object_or_404(product, id=product_id) 

                if cart.objects.filter(User=request.user, product=product_instance).exists():
                    return JsonResponse({'status': 'already added'}, status=200)

                if product_instance.quantity >= product_qty:
                    cart.objects.create(User=request.user, product=product_instance, product_quantity=product_qty)
                    return JsonResponse({'status': 'added success'}, status=200)
                else:
                    return JsonResponse({'status': 'stock not available'}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'invalid JSON data'}, status=400)
            except KeyError as e:
                return JsonResponse({'status': f'error: Missing key {str(e)}'}, status=400)
            except Exception as e:
                return JsonResponse({'status': f'error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'status': 'login required'}, status=401)
    else:
        return JsonResponse({'status': 'invalid access'}, status=403)

def checkout(request):
    return render(request,"shop/checkout.html")

def cart_page(request):
    fav_count = 0
    cart_count = 0
       
    if request.user.is_authenticated:
        fav_count = fav.objects.filter(User=request.user).count()
        categories = category.objects.filter(status=0)
        Cart = cart.objects.filter(User=request.user)
        cart_count = cart.objects.filter(User=request.user).count()

        # Update cart items with negotiated price (if available)
        for item in Cart:
            negotiation = Negotiation.objects.filter(user=request.user, product=item.product, is_successful=True).first()
            item.negotiated_price = negotiation.current_offer if negotiation else item.product.nprice

        return render(request, 'shop/cart.html', {'cart': Cart, 'categories': categories, 'fav_count': fav_count, 'cart_count': cart_count})
    else:
        return redirect('login')

def remove_cart(request, cid):
    cartitems = cart.objects.get(id=cid)
    cartitems.delete()
    return redirect('cart')


def fav_page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                body = request.body.decode('utf-8')
                print("Raw Request Body:", body)  # Debugging: Print request body

                data = json.loads(body)
                print("Parsed Data:", data)  # Debugging: Print parsed data

                # ✅ Ensure correct key names
                if 'pid' not in data:
                    return JsonResponse({'status': 'missing required fields'}, status=400)

                product_id = data['pid']
                product_instance = get_object_or_404(product, id=product_id) 

                if fav.objects.filter(User=request.user, product=product_instance).exists():
                    return JsonResponse({'status': 'already added'}, status=200)

                fav.objects.create(User=request.user, product=product_instance)
                return JsonResponse({'status': 'added success'}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'invalid JSON data'}, status=400)
            except KeyError as e:
                return JsonResponse({'status': f'error: Missing key {str(e)}'}, status=400)
            except Exception as e:
                return JsonResponse({'status': f'error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'status': 'login required'}, status=401)

    else:
        return JsonResponse({'status': 'invalid access'}, status=403)


def fav_view_page(request):
    fav_count = 0
    cart_count = 0
    
    if request.user.is_authenticated:
        categories = category.objects.filter(status=0)
        Fav = fav.objects.filter(User=request.user)
        cart_count = cart.objects.filter(User=request.user).count()
        fav_count = fav.objects.filter(User=request.user).count()
        return render(request, 'shop/fav.html', {'fav': Fav,'categories': categories, 'fav_count': fav_count, 'cart_count': cart_count})
    else:
        return redirect('login')
 
   
def remove_fav(request, cid):
    favitems = fav.objects.get(id=cid)
    favitems.delete()
    return redirect('favviewpage')



