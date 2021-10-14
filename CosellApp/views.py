from django.shortcuts import render, redirect
from .forms import UserForm, StudentForm
from .models import Student, Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
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


class PostListView(LoginRequiredMixin,ListView):
    model = Product
    template_name = '../templates/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'
    ordering = ['-DateTime']

class PostDetailView(LoginRequiredMixin,DetailView):
    model = Product
    template_name = '../templates/productdetail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = '../templates/Product_form.html'
    fields = ['Name', 'Description','Price','DateTime','Photo']

    def form_valid(self, form):
        form.instance.SellerInfo = Student.objects.filter(user=self.request.user).first()
        return super().form_valid(form)
        
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Product
    template_name = '../templates/Product_form.html'
    fields = ['Name', 'Description','Price','DateTime','Photo']

    def form_valid(self, form):
        form.instance.SellerInfo = Student.objects.filter(user=self.request.user).first()
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
    template_name = '../templates/user_college_product.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'products'

    def get_queryset(self):
        user1 = get_object_or_404(User, username=self.kwargs.get('username'))
        return Product.objects.filter(SellerInfo__college=Student.objects.filter(user=user1).first().college).order_by('-DateTime')

def error(request):
    return render(request, 'error.html')


@login_required
def logout_user(request):
    logout(request)
    return render(request,'logout.html')

@login_required
def profile(request):
    return render(request,'profile.html')


@login_required
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

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)