from django.db import models


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField()
    vendor_id = models.IntegerField()
    customer_id = models.IntegerField()


class OrderLine(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_description = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_vat_rate = models.DecimalField(max_digits=5, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    full_price_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)


class Promotion(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)


class ProductPromotion(models.Model):
    date = models.DateField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)


class VendorCommissions(models.Model):
    date = models.DateField()
    vendor_id = models.IntegerField()
    rate = models.DecimalField(max_digits=5, decimal_places=2)
