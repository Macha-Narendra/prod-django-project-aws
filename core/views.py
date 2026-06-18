from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegisterForm, ProductForm
from .models import Product


def home(request):
    return redirect('product_list')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome, {username}. Your account is ready.')
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def product_list(request):
    products = Product.objects.active().select_related('created_by')
    context = {
        'products': products,
        'product_count': products.count(),
    }
    return render(request, 'core/product_list.html', context)


def product_detail(request, pk):
    products = Product.objects.select_related('created_by')
    if request.user.is_authenticated:
        products = products.filter(Q(active=True) | Q(created_by=request.user))
    else:
        products = products.active()
    product = get_object_or_404(products, pk=pk)
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
            return redirect(product)
    else:
        form = ProductForm()
    return render(request, 'core/product_form.html', {'form': form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product.objects.owned_by(request.user), pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect(product)
    else:
        form = ProductForm(instance=product)
    return render(request, 'core/product_form.html', {'form': form, 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product.objects.owned_by(request.user), pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('dashboard')
    return render(request, 'core/product_confirm_delete.html', {'product': product})


@login_required
def dashboard(request):
    products = Product.objects.owned_by(request.user).select_related('created_by')
    context = {
        'products': products,
        'total_products': products.count(),
        'active_products': products.active().count(),
        'inactive_products': products.filter(active=False).count(),
    }
    return render(request, 'core/dashboard.html', context)
