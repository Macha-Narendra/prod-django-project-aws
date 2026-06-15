from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import UserRegisterForm, ProductForm
from .models import Product


def home(request):
    return redirect('product_list')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def product_list(request):
    products = Product.objects.filter(active=True).order_by('-created_at')
    return render(request, 'core/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, active=True)
    return render(request, 'core/product_detail.html', {'product': product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, 'Product created successfully.')
            return redirect(reverse('product_detail', args=[product.pk]))
    else:
        form = ProductForm()
    return render(request, 'core/product_form.html', {'form': form})


@login_required
def dashboard(request):
    products = Product.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'core/dashboard.html', {'products': products})
