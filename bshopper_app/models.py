from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django_facebook.models import FacebookCustomUser as User
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female'),
    ('n', 'Null'),
)
import os
PROFILE_IMAGE_PATH = os.path.join('uploads', 'profile_pictures/%Y/%m/%d')

class Categories(models.Model):
    """
    """
    CatId = models.AutoField(primary_key=True)
    Category_name = models.CharField(max_length=150,blank=True, null=True)
    Category_name_hier = models.CharField(max_length=150,blank=True, null=True)
    Gender = models.CharField(max_length=1)
    class Meta:
        db_table = "bshopper_app_categories"
        verbose_name = "Categorie"
        #verbose_name_plural = "Categories"
    def __str__(self):
        return "%s -- %s" % (self.CatId, self.Category_name)
#    def __unicode__(self):
#        return self.Category_name

class ScrapedItems(models.Model):
    """
    scraped_items
    """
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=750, blank=True, null=True)
    sku = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    manufacturer = models.CharField(max_length=750, blank=True, null=True)
    scraped_category = models.CharField(max_length=750, blank=True, null=True)
    color = models.CharField(max_length=750, blank=True, null=True)
    size = models.CharField(max_length=750, blank=True, null=True)
    title = models.CharField(max_length=750, blank=True, null=True)
    retail_price = models.CharField(max_length=750, blank=True, null=True)
    sale_price = models.CharField(max_length=750, blank=True, null=True)
    _type = models.CharField(max_length=100, blank=True, null=True)
    image_urls = models.CharField(max_length=3000, blank=True, null=True)
    images = models.CharField(max_length=3000, blank=True, null=True)
    images_json = models.CharField(max_length=3000, blank=True, null=True)
    project_id = models.CharField(max_length=100, blank=True, null=True)
    job_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    spider_name = models.CharField(max_length=100, blank=True, null=True)
    predicted_category_name = models.CharField(max_length=750, blank=True, null=True)
    #predicted_category_id = models.IntegerField()
    predicted_category = models.ForeignKey(Categories)
    duplication_check = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        db_table = "scraped_items"
        verbose_name = "Scraped item"
        #verbose_name_plural = "Scraped items"

class FacebookAuth(models.Model):
    """
    Facebook auth

    user id
    facebook id
    product page likes
    linked date
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    FacebookId = models.CharField(max_length=200)
    ProductPageLikes = models.CharField(max_length=1000)
    LinkedDate = models.DateTimeField(blank=True, null=True)

class MailChimp(models.Model):
    """
    Facebook auth

    user id
    facebook id
    product page likes
    linked date
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    MailChimpAllowed = models.BooleanField(default=True)

class UserPreferences(models.Model):
    """
    User preferences

    user id
    first name
    last name
    gender
    birthday
    profile picture path
    location
    categories (comma seperated)
    brands (comma seperated)
    price (comma seperated)
    color (comma seperated)
    """


    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    FirstName = models.CharField(max_length=100,blank=True, null=True)
    LastName = models.CharField(max_length=100,blank=True, null=True)
    Gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    BirthDay = models.DateField(blank=True, null=True)

    ProfilePicturePath = models.ImageField(upload_to=PROFILE_IMAGE_PATH, blank=True)
    Location = models.CharField(max_length=200)
    Categories = models.CharField(max_length=1000)
    Brands = models.CharField(max_length=1000)
    Price = models.CharField(max_length=1000)
    Color = models.CharField(max_length=1000)
    class Meta:
        verbose_name = "User preference"
        #verbose_name_plural = "User preferences"


class Manufacturer(models.Model):
    """
    """
    Manufacturer_id = models.AutoField(primary_key=True)
    Manufacturer_Name = models.CharField(max_length=150,blank=True, null=True)
    class Meta:
        db_table = "Manufacturer"

class User_Viewership(models.Model):
    """
    """
    RowID = models.AutoField(primary_key=True)
    UserId = models.IntegerField()
    ProductId = models.IntegerField()
    LikeProduct = models.IntegerField()
    NoOfViews = models.IntegerField()
    class Meta:
        db_table = "bshopper_user_viewership"

class Trending_Products(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    ProductId = models.IntegerField()
    UserId = models.IntegerField()
    #TransactionDate = models.DateTimeField(blank=True, null=True)
    TransactionDate = models.DateTimeField(default=datetime.now())
    class Meta:
        db_table = "bshopper_trending_products"

class Merchants(models.Model):
    """
    """
    id = models.AutoField(primary_key=True)
    merch_id = models.CharField(max_length=250,blank=True, null=True)
    merch_name = models.CharField(max_length=250,blank=True, null=True)
    class Meta:
        db_table = "bshopper_app_merchants"

class Product_Color(models.Model):
    """
    """
    ProductId = models.AutoField(primary_key=True)
    image = models.CharField(max_length=500,blank=True, null=True)
    Color = models.CharField(max_length=500,blank=True, null=True)
    Hex = models.CharField(max_length=20,blank=True, null=True)
    rgb = models.CharField(max_length=20,blank=True, null=True)
    class Meta:
        db_table = "bshopper_product_color"

class Top_Manufacturer(models.Model):
    """
    """
    Manufacturer_Id = models.AutoField(primary_key=True)
    Manufacturer = models.CharField(max_length=300,blank=True, null=True)
    class Meta:
        db_table = "bshopper_top_brands"

class Invitation(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=500,blank=True, null=True)
    code = models.CharField(max_length=20)
    sender = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s, %s' % (self.sender.username, self.email)
    def send(self):
        subject = u'Invitation to join Django Bookmarks'
        link = 'http://%s/friend/accept/%s/' % ("www.boredshopper.com", self.code)
        template = get_template('invitation_email.txt')
        context = Context({
            'name': self.name,
            'link': link,
            'sender': self.sender.username,
            })
        message = template.render(context)
        send_mail(
            subject, message,
            settings.DEFAULT_FROM_EMAIL, [self.email]
        )
    class Meta:
        db_table = "bshopper_email_invitation"