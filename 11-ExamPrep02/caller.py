import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Product, Order
from django.db.models import Q, F, Count

# print(Profile.objects.get_regular_customers())

def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ''
    
    profiles = Profile.objects.annotate(
        orders_count = Count('orders')
    ).filter(
        Q(full_name__icontains=search_string) |
        Q(email__icontains=search_string) |
        Q(phone_number__icontains=search_string)
    ).order_by(
        'full_name'
    )

    return '\n'.join(
        [f"Profile: {p.full_name}, email: {p.email}, "\
         f"phone number: {p.phone_number}, orders: {p.orders_count}" 
        for p in profiles]
    )

def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if not profiles:
        return ''

    return '\n'.join(
        f'Profile: {p.full_name}, orders: {p.orders_count}'
        for p in profiles
    )


def get_last_sold_products() -> str:
    order = Order.objects.last()

    if not order:
        return ''

    products = order.products.order_by('name')

    return f'Last sold products: {", ".join(p.name for p in products)}'


def get_top_products() -> str:
    products = Product.objects.annotate(
        product_orders_cnt = Count('products_orders')
    ).filter(
        product_orders_cnt__gt=0
    ).order_by(
        '-product_orders_cnt', 'name'
    )[:5]

    if not products:
        return ''
    
    res = '\n'.join(f"{p.name}, sold {p.product_orders_cnt} times" for p in products)
    
    return f'Top products:\n{res}'


def apply_discounts() -> str:
    orders = Order.objects.annotate(
        products_count = Count('products')
    ).filter(
        products_count__gt=2,
        is_completed=False
    ).update(
        total_price=F('total_price') * 0.9
    )

    return f'Discount applied to {orders} orders.'


def complete_order() -> str:
    order = Order.objects.filter(
        is_completed=False
    ).first()

    if not order:
        return ''

    order.is_completed=True
    order.save()

    for product in order.products.all():
        product.in_stock -= 1

        if product.in_stock == 0:
            product.is_available = False
        product.save()    

    return 'Order has been completed!'
