from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    address=models.TextField()

    def __str__(self):
        return self.name
    

class Measurement(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    chest = models.FloatField()
    waist = models.FloatField()
    hip = models.FloatField()
    shoulder = models.FloatField()
    sleeve_length = models.FloatField()
    dress_type = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.customer.name} - {self.dress_type}"


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('stitching', 'In Stitching'),
        ('ready', 'Ready'),
        ('delivered', 'Delivered'),
    ]

    PAYMENT_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dress_type = models.CharField(max_length=100)
    price = models.IntegerField()
    order_date = models.DateField()
    delivery_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"{self.customer.name} - {self.dress_type}"


    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dress_type = models.CharField(max_length=100)
    price = models.IntegerField()
    order_date = models.DateField()
    delivery_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.customer.name} - {self.dress_type}"

class History(models.Model):
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    dress_type = models.CharField(max_length=100)
    price = models.IntegerField()
    delivery_date = models.DateField()
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name

