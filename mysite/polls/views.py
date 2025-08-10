from django.shortcuts import render,redirect
from django.template import loader
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_GET,require_POST
from django.views import View
from django.contrib.auth.models import User
from .forms import RegisterForm,AddProductForm

from .models import Question
from .models import Product,Cart,CartItem

# Create your views here.
from django.http import HttpResponse

from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {"latest_question_list": latest_question_list}
    return HttpResponse(template.render(context, request))
   
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})
    






# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def registerView(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=User.objects.create_user(username=username,password=password)
            login(request,user)
            return redirect('polls:login')
    else:
            form=RegisterForm()
    return render(request,'accounts/register.html',{'form':form})
        
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    if(request.method == "POST"):
         logout(request)
         return redirect('polls:login')
    else:
        return redirect('polls:home')

@login_required 
def home_view(request):
    return render(request, 'auth1_app/home.html')

class ProtectedView(LoginRequiredMixin, View):
    login_url = 'accounts/login/'  # Redirect to login page if not authenticated
    redirect_field_name = 'redirect_to'  # The name of the query parameter to redirect to after login
    def get(self, request):
        return render(request, 'registration/protected.html')
    
@require_GET
@login_required  
def Product_home(request):
     products_list=[{"id":1,"name":"Product 1","price":100,"description":"Description of Product 1"},
              {"id":2,"name":"Product 2","price":200,"description":"Description of Product 2"},
              {"id":3,"name":"Product 3","price":300,"description":"Description of Product 3"},
              {"id":4,"name":"Product 4","price":400,"description":"Description of Product 4"},
              {"id":5,"name":"Product 5","price":500,"description":"Description of Product 5"},
              {"id":6,"name":"Product 6","price":600,"description":"Description of Product 6"},
              {"id":7,"name":"Product 7","price":700,"description":"Description of Product 7"},
              {"id":8,"name":"Product 8","price":800,"description":"Description of Product 8"},
              {"id":9,"name":"Product 9","price":900,"description":"Description of Product 9"},
              {"id":10,"name":"Product 10","price":1000,"description":"Description of Product 10"}
              ]
     products=Product.objects.all()
     return render(request, 'ecommerce/product_home.html',{'products':products})

@require_GET
@login_required
def view_products(request):
    products_list=[{"id":1,"name":"Product 1","price":100,"description":"Description of Product 1"},
              {"id":2,"name":"Product 2","price":200,"description":"Description of Product 2"},
              {"id":3,"name":"Product 3","price":300,"description":"Description of Product 3"},
              {"id":4,"name":"Product 4","price":400,"description":"Description of Product 4"},
              {"id":5,"name":"Product 5","price":500,"description":"Description of Product 5"},
              {"id":6,"name":"Product 6","price":600,"description":"Description of Product 6"},
              {"id":7,"name":"Product 7","price":700,"description":"Description of Product 7"},
              {"id":8,"name":"Product 8","price":800,"description":"Description of Product 8"},
              {"id":9,"name":"Product 9","price":900,"description":"Description of Product 9"},
              {"id":10,"name":"Product 10","price":1000,"description":"Description of Product 10"}
              ]
    products=Product.objects.all()
    return render(request,'ecommerce/products.html',{'products':products})

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()  # select_related for efficiency
    return render(request, 'ecommerce/cart.html', {'cart_items': cart_items,'total':cart.total_price()})


@require_GET
def view_product_description(request,product_id):
    product=Product.objects.get(id=product_id)
    return render(request,'ecommerce/product_description.html',{'product_description':product.description,'product_id':product_id})

def add_to_cart(request,product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        
        return redirect('polls:products')
    else:
        return HttpResponse("Invalid request method.", status=405)
    
@login_required
def add_product(request):
    if request.method=="POST":
        form=AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user  # set the logged-in user
            product.save()
            return redirect('polls:products')
    else:
         form=AddProductForm()
    return render(request,'ecommerce/add_product.html',{'form':form})


@login_required
def my_products(request):
    products=Product.objects.filter(created_by=request.user)
    return render(request, 'ecommerce/myproducts.html', {'products': products})