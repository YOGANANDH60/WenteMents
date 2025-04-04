from django.db import models
from django.contrib.auth.models import User
import datetime
import os

def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%y%m%d%h:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)
class category(models.Model):
    name = models.CharField(max_length=50,null=False,blank=False)
    image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
class product(models.Model):
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    pname = models.CharField(max_length=200,null=False,blank=False)
    pimage = models.ImageField(upload_to=getFileName,null=True,blank=True)
    quantity = models.IntegerField(null=False,blank=False)
    oprice = models.FloatField(null=False,blank=False)
    nprice = models.FloatField(null=False,blank=False)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0-show,1-Hidden")
    trending = models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.pname
class productImages(models.Model):
    images = models.ImageField(upload_to="product-images")
    product = models.ForeignKey(product,on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)
# negotiation model
class Negotiation(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    current_offer = models.FloatField(null=True, blank=True)
    counter_offer = models.FloatField(null=True, blank=True)
    final_price = models.FloatField(null=True, blank=True)  # Store the final agreed price
    attempts = models.PositiveIntegerField(default=0)
    max_attempts = models.PositiveIntegerField(default=3)
    is_successful = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Negotiation: {self.user.username} - {self.product.pname}"
class articals(models.Model):
    blog_name = models.CharField(max_length=50,null=False,blank=False)
    blog_image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    blog_description = models.TextField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self. blog_name
class cart(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    product_quantity = models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def product_price(self):
        """Return negotiated price if available; otherwise, return normal price."""
        negotiation = Negotiation.objects.filter(user=self.User, product=self.product, is_successful=True).first()
        return negotiation.current_offer if negotiation else self.product.nprice
    @property
    def product_total_price(self):
        """Calculate total price based on negotiated price if applicable."""
        return self.product_quantity * self.product_price 
class fav(models.Model):
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.User.username