from django.shortcuts import render, redirect
from .forms import UserForm, StudentForm
from .models import FAQ, Student, Product, Payment, Message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import razorpay
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db.models import Q
from .serializers import MessageSerializer, UserSerializer
from rest_framework.parsers import JSONParser


def index(request):
    return render(request, 'index.html')


def register_user(request):

    userform = UserForm()
    studentform = StudentForm()

    context = {
        'userform': userform,
        'studentform': studentform
    }

    if request.method == 'POST':
        userform = UserForm(request.POST)
        studentform = StudentForm(request.POST)

        if userform.is_valid() and studentform.is_valid():
            user = userform.save()
            user.set_password(user.password)
            user.save()
            user_info = studentform.save(commit=False)
            user_info.user = user
            user_info.save()
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('home')

        else:
            context = {'userform': userform,
                       'studentform': studentform, 'user_form.errors': userform.errors,
                       'user_info_form.errors': studentform.errors}
            return render(request, 'register.html', context)

    return render(request, 'register.html', context=context)


def login_user(request):

    context = {
        'check': False
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

        else:
            context = {
                'check': True
            }

    return render(request, 'login.html', context)


# class PostListView(LoginRequiredMixin, ListView):
#     model = Product
#     template_name = '../templates/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'products'
#     paginate_by = 3

#     def get_queryset(self):
#         user = self.request.user
#         sd = Student.objects.get(user=user)
#         collage = sd.college
#         return Product.objects.filter(~Q(payment=None), SellerInfo__college=collage).order_by('-DateTime')

@login_required(login_url='error')
def home(request):

    a = request.GET.get('filter')

    if a == None or a == '0':
        paginate_by = 3
        user = request.user
        sd = Student.objects.get(user=user)
        collage = sd.college
        products = Product.objects.filter(
            ~Q(payment=None), SellerInfo__college=collage).order_by('-DateTime')

        context = {
            'products': products,
            'a': 1
        }
        return render(request, 'home.html', context)

    else:
        b = a.split('-')

        low = b[0]
        high = b[1]

        user = request.user
        sd = Student.objects.get(user=user)
        collage = sd.college
        products = Product.objects.filter(
            ~Q(payment=None), SellerInfo__college=collage, Price__gte=low, Price__lte=high).order_by('-DateTime')

        context = {
            'products': products, 'a': 1
        }

        return render(request, 'home.html', context)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = '../templates/productdetail.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = '../templates/Product_form.html'
    fields = ['Name', 'Description', 'Price', 'DateTime', 'Photo']

    def form_valid(self, form):
        form.instance.SellerInfo = Student.objects.filter(
            user=self.request.user).first()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = '../templates/Product_form.html'
    fields = ['Name', 'Description', 'Price', 'DateTime', 'Photo']

    def form_valid(self, form):
        form.instance.SellerInfo = Student.objects.filter(
            user=self.request.user).first()
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        if self.request.user == product.SellerInfo.user:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = '../templates/Product_confirm_delete.html'
    success_url = '/home'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.SellerInfo.user:
            return True
        return False


class UserPostListView(ListView):
    model = Product
    # <app>/<model>_<viewtype>.html
    template_name = '../templates/user_college_product.html'
    context_object_name = 'products'

    def get_queryset(self):
        user1 = get_object_or_404(User, username=self.kwargs.get('username'))
        return Product.objects.filter(SellerInfo__college=Student.objects.filter(user=user1).first().college).order_by('-DateTime')


def error(request):
    return render(request, 'error.html')


@login_required(login_url='error')
def logout_user(request):
    logout(request)
    return render(request, 'logout.html')


# @login_required(login_url='error')
# def profile(request):
#     return render(request, 'profile.html')


@login_required(login_url='error')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        products = Product.objects.all().filter(
            SellerInfo=Student.objects.get(user=request.user)).order_by('-DateTime')
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'products': products
    }

    return render(request, 'profile.html', context)


@login_required(login_url='error')
def payment(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        client = razorpay.Client(
            auth=("rzp_test_9bGYWCeBA8FVtd", "YdFIwXt49ZQdXdxkZGRvlTmN"))

        current_Product = Product.objects.get(
            Id=request.POST.get('Product_id'))
        Product_price = current_Product.Price

        Total_amount = 0.07*Product_price

        payment_obj = Payment()
        payment_obj.transection_id = str(
            current_Product.DateTime) + request.user.username
        payment_obj.Amount_paid = round(Total_amount, 2)
        payment_obj.Date = current_Product.DateTime
        payment_obj.Student_Info = Student.objects.get(user=request.user)
        payment_obj.save()

        current_Product.payment = payment_obj
        current_Product.save()

        return redirect('success_take')

    current_Product = Product.objects.get(Id=request.GET.get('ProductId'))

    Total_amount = 0.07*current_Product.Price

    context = {'Product_id': request.GET.get('ProductId'), 'Product_name': current_Product.Name, 'Product_desc': current_Product.Description,
               'Product_date': current_Product.DateTime, 'Product_price': current_Product.Price, 'Total_amount': round(Total_amount, 2), 'Product_image': current_Product.Photo}

    return render(request, 'payment.html', context)


@csrf_exempt
def success_take(request):
    return redirect('home')


@login_required(login_url='error')
def faq_ask(request):
    if request.method == "POST":
        Query = request.POST.get('Query')
        # context = {
        #     'Query': Query
        # }
        faq = FAQ()
        faq.UserName = request.user
        faq.Query = Query
        faq.save()
        return redirect('faq')
    return render(request, 'faq_ask.html')
    # return render(request, 'faq_ask.html')
    # faq_obj = FAQ()
    # faq_obj.Id = request.POST.get('username')
    # faq_obj.Answer


def faq(request):
    faqs = FAQ.objects.all()
    # User_Info = FAQ.objects.all()
    # Answer = User_Info.Answer
    context = {
        'faqs': faqs,
    }
    return render(request, 'faq.html', context)


def about(request):
    return render(request, 'about.html')


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(
            sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(
            messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('home')

    return render(request, "messages.html",
                  {'users': User.objects.exclude(username=request.user.username),
                   'receiver': User.objects.get(id=receiver),
                   'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})


def recivedMessages(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == "GET":
        user = User.objects.exclude(username=request.user.username)
        Msg = Message.objects.all()
        for m in Msg:
            print("-----------------------------------------------------")
            print(m.message)
        return render(request, 'chat2.html',
                      {'users': user})
