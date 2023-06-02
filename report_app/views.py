import pandas as pd
from django.db.models import Sum, Avg
from django.http import JsonResponse

from report_app.models import Order, OrderLine, Product, Promotion, ProductPromotion, VendorCommissions

def generate_report(request):
    date = request.GET.get('date')

    # Read data from spreadsheets using pandas
    orders_df = pd.read_csv('data/orders.csv')
    order_lines_df = pd.read_csv('data/order_lines.csv')
    products_df = pd.read_csv('data/products.csv')
    promotions_df = pd.read_csv('data/promotions.csv')
    product_promotions_df = pd.read_csv('data/product_promotions.csv')
    vendor_commissions_df = pd.read_csv('data/commissions.csv')

    # Convert pandas DataFrames to Django models or querysets
    orders = [
        Order(id=row['id'], created_at=row['created_at'], vendor_id=row['vendor_id'], customer_id=row['customer_id'])
        for _, row in orders_df.iterrows()
    ]
    Order.objects.bulk_create(orders)

    order_lines = [
        OrderLine(
            order_id=row['order_id'], product_id=row['product_id'], product_description=row['product_description'],
            product_price=row['product_price'], product_vat_rate=row['product_vat_rate'],
            discount_rate=row['discount_rate'], quantity=row['quantity'], full_price_amount=row['full_price_amount'],
            discounted_amount=row['discounted_amount'], vat_amount=row['vat_amount'], total_amount=row['total_amount']
        )
        for _, row in order_lines_df.iterrows()
    ]
    OrderLine.objects.bulk_create(order_lines)

    products = [
        Product(id=row['id'], description=row['description'])
        for _, row in products_df.iterrows()
    ]
    Product.objects.bulk_create(products)

    promotions = [
        Promotion(id=row['id'], description=row['description'])
        for _, row in promotions_df.iterrows()
    ]
    Promotion.objects.bulk_create(promotions)

    product_promotions = [
        ProductPromotion(date=row['date'], product_id=row['product_id'], promotion_id=row['promotion_id'])
        for _, row in product_promotions_df.iterrows()
    ]
    ProductPromotion.objects.bulk_create(product_promotions)

    vendor_commissions = [
        VendorCommissions(date=row['date'], vendor_id=row['vendor_id'], rate=row['rate'])
        for _, row in vendor_commissions_df.iterrows()
    ]
    VendorCommissions.objects.bulk_create(vendor_commissions)


    # Perform the report calculations using Django ORM aggregations
    total_items_sold = OrderLine.objects.filter(order__created_at__date=date).aggregate(total_items=Sum('quantity'))['total_items']
    total_customers = Order.objects.filter(created_at__date=date).count()
    total_discount = OrderLine.objects.filter(order__created_at__date=date).aggregate(total_discount=Sum('discounted_amount'))['total_discount']
    avg_discount_rate = OrderLine.objects.filter(order__created_at__date=date).aggregate(avg_discount_rate=Avg('discount_rate'))['avg_discount_rate']
    avg_order_total = Order.objects.filter(created_at__date=date).aggregate(avg_order_total=Avg('orderline__total_amount'))['avg_order_total']
    total_commissions = VendorCommissions.objects.filter(date=date).aggregate(total_commissions=Sum('rate'))['total_commissions']
    avg_commissions_per_order = total_commissions / total_customers

    # Construct the report as a dictionary
    report = {
        'total_items_sold': total_items_sold,
        'total_customers': total_customers,
        'total_discount': total_discount,
        'avg_discount_rate': avg_discount_rate,
        'avg_order_total': avg_order_total,
        'total_commissions': total_commissions,
        'avg_commissions_per_order': avg_commissions_per_order,
    }

    # Return the report as a JSON response
    return JsonResponse(report)