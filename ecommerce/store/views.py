from django.shortcuts import render, redirect
from .models import Product, Category, Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator


def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories
        
    }

    return render(request, 'store/home.html', context)
@login_required
def cart(request):
    order, created = Order.objects.get_or_create(
        user=request.user, complete=False)
    items = order.orderitem_set.all()

    context = {
        'items': items,
        'order': order
    }

    return render(request, 'store/cart.html', context)


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        user=request.user, complete=False)
    order_item, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    cart_items_count = order.orderitem_set.count()

    if not created:
        order_item.quantity += 1
        order_item.save()

    return redirect('cart') 

@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    order = Order.objects.get(user=request.user, complete=False)
    order_item = OrderItem.objects.get(order=order, product=product)

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()

    return redirect('cart')

from django.db.models import Avg

from .models import Review

def product_detail(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )

    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating
    }

    return render(request, 'store/product_detail.html', context)
from django.contrib import messages

@login_required
def checkout(request):
    order = Order.objects.get(user=request.user, complete=False)

    if request.method == "POST":
        order.complete = True
        order.save()
        messages.success(request, "Order placed successfully!")
        return redirect('home')

    return render(request, 'store/checkout.html', {'order': order})