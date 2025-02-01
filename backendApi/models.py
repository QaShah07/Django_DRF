from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    pass

# this is the product Table
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/',blank=True,null=True)

    @property
    def in_stock(self):
        return self.stock>0

    def __str__(self):
        return self.name


# Order Database Table
class Order(models.Model):
    # this is the enum class
    class StatusChoices(models.TextChoices):
        PENDING = 'pending'
        CONIFORMED = 'Coniformed'
        CANCELD = 'Canceld'
    order_id = models.UUIDField(primary_key=True,default=uuid.uuid4)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    products = models.ManyToManyField(Product,through="OrderItem",related_name='orders')
    # method for get the product
    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"
    
# Database table of OrderItem
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    # function to return String
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"