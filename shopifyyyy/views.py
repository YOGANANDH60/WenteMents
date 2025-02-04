from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import *
from django.contrib import messages
from .form import customeuserform
from django.contrib.auth import authenticate,login,logout


# Create your views here.

def home(request):
    products=product.objects.filter(trending=1)
    categories = category.objects.filter(status=0) 
    return render(request, "shop/index.html",{'products': products,'categories': categories})

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
    return render(request, "shop/category.html", {'categories': categories}) 

def productdetails(request,name):
    categories = category.objects.filter(status=0) 
    if(category.objects.filter(name=name,status=0)):
         productdetails = product.objects.filter(category__name=name) 
         return render(request, "shop/productdetails.html", {'productdetails': productdetails,'categories': categories})
    else:
        messages.warning(request,"no such category found")
        return redirect('category')  

def single_productdetails(request,cname,spname):
    categories = category.objects.filter(status=0) 
    if(category.objects.filter(name=cname,status=0)):
        if(product.objects.filter(pname=spname)):
            products = product.objects.get(pname=spname)
            sideimg = productImages.objects.filter(product=products)  # Fetch related images
            context = {
                'products': products,
                'sideimg': sideimg,
                'categories': categories
            }
            return render(request, 'shop/single_productdetails.html', context)
        else:
            messages.error(request,"no such product found")
            return redirect('category')  
    else:
        messages.error(request,"no such catogory")
        return redirect('category')  


def negotiate(request, product_name):
    product_obj = get_object_or_404(product, pname=product_name)
    categories = category.objects.filter(status=0)
    if product_obj.nprice < 1000:  
        messages.warning(request, "Negotiation is only available for products priced above 1000.")
        return redirect('productdetails', name=product_obj.category.name,)

    negotiation_result = None  
    counter_offer = None  

    if request.method == "POST":
        user_offer = float(request.POST.get("user_offer", 0))

        if user_offer >= product_obj.nprice * 0.9:
            negotiation_result = "accepted"
        elif user_offer >= product_obj.nprice * 0.8:
            counter_offer = round(product_obj.nprice * 0.9, 2)
            negotiation_result = "counter"
        else:
            negotiation_result = "rejected"

    return render(request, "shop/negotiate.html", {
        "product": product_obj,
        "negotiation_result": negotiation_result,
        "counter_offer": counter_offer,
        'categories': categories
    })


def blog(request):
    blog = articals.objects.all()
    categories = category.objects.filter(status=0)
    return render(request, "shop/blog.html", {'blog': blog,'categories': categories})


def about(request):
    categories = category.objects.filter(status=0)
    return render(request, "shop/about.html",{'categories': categories})
