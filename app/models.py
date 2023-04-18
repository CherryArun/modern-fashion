from django.db import models
from django.utils import timezone
STATUS = (
    ('','Select'),
    ('male','Male'),
    ('female', 'Female'),
)

class Product_Category(models.Model):
	category_name = models.CharField(max_length=50)
	description = models.CharField(max_length=1000,null=True)
	def __str__(self):
		return self.category_name
class Product(models.Model):
	product_name = models.CharField(max_length=50)
	price = models.CharField(max_length=50)
	category = models.ForeignKey(Product_Category, on_delete=models.CASCADE)
	description = models.TextField(max_length=2000)
	image = models.FileField('Product Image',upload_to='product/',null=True)
	def __str__(self):
		return self.product_name

class User_Detail(models.Model):
	name = models.CharField(max_length=300)
	password = models.CharField(max_length=40)
	email = models.EmailField(max_length=100,unique=True)
	mobile = models.CharField(max_length=15)
	city = models.CharField(max_length=30)
	pincode = models.CharField(max_length=10)
	address =  models.TextField(max_length=2000)
	def __str__(self):
		return self.name
class Cart_Detail(models.Model):
	user_id = models.ForeignKey(User_Detail, on_delete=models.CASCADE)
	book_id = models.CharField(max_length=30)
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
	status = models.CharField(max_length=50)
	tot = models.IntegerField()
	tot_price = models.CharField(max_length=200)
	date = models.DateField(default=timezone.now())
	def __str__(self):
		return self.product_id.product_name
	def publish(self):
		self.date = timezone.now()
		self.save()

