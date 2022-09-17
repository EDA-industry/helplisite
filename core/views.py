
from cgi import print_directory
from itertools import product
from turtle import title
from urllib import request
from django.conf import settings
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect, get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Category, Product, Order, Cart, Tag
class HomeView(View):
    def get(self, request):
        if request.method == 'GET':
            sort_by = request.GET.get("sort", "1")
            search = request.GET.get("search", "")
            products = Product.objects.filter(title__icontains=search)
            if (sort_by == 1):
                products = Product.objects.all().order_by("-shelf_life")
            elif(sort_by == 2):
                products = Product.objects.all().order_by("-price")
            categories = Category.objects.all()
            filters = request.GET.get("filter", "")
            if (filters!=""):
                products = Product.objects.filter(category__name=filters)
            return render(request, 'core/home.html',{'products':products, 'categories':categories})

@api_view()
def cart(request):
    try:
        cart = Cart.objects.get(user_id=request.user.id)
    except:
        cart = Cart.objects.create(user_id=request.user.id)
    
    print(cart)
    context = {
        'cart':cart,
        'products':cart.products.all(),
    }
    return render(request, 'core/cart.html', context)

def add_product(request, product_id):
    if request.method == "GET":
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except:
            cart = Cart.objects.create(user_id=request.user.id)
    
        product = Product.objects.get(id=int(product_id))
        product.quantity-=1
        product.save()
        cart.products.add(product)
        print(product.quantity)
        cart.save()
        messages.success(
            request, 'Your product has been added successfully.')
        return redirect("core:cart")

def clear_cart(request):
    if request.method =='GET':
        cart = Cart.objects.get(user_id=request.user.id).delete()
        # prod = Product.objects.filter(p)
        # for item in cart.products:
        #     for product in 
        return redirect("core:cart")

class ProductView(DetailView):
    model = Product
    template_name = 'core/product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        slug = self.kwargs['slug']

        product = get_object_or_404(Product, pk=pk, slug=slug)
        context['product'] = product
        return context




class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ["title", "quantity", "adress", "shelf_life" ,"description", "image", "category", "tags", "price"]

    def get_success_url(self):
        messages.success(
            self.request, 'Your product has been created successfully.')
        return reverse_lazy("core:home")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        obj.slug = slugify(form.cleaned_data['title'])
        obj.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ["title", "quantity", "adress", "shelf_time", "description", "image", "category", "tags", "price"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update

        return context

    def get_success_url(self):
        messages.success(
            self.request, 'Your product has been updated successfully.')
        return reverse_lazy("core:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product

    def get_success_url(self):
        messages.success(
            self.request, 'Your product has been deleted successfully.')
        return reverse_lazy("core:home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class OrderView(DetailView):
    model = Order

    def get_success_url(self):
        messages.success(
            self.request, 'Your order has been created successfully.')
        return reverse_lazy("core:home")

    def create_order(self):
        user = self.request.user


