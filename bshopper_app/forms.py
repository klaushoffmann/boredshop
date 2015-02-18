from django.conf import settings
from django import forms
from formfieldset.forms import FieldsetMixin
from django.db.models import get_model
from django.db import models
#from django.core.validators import alnum_re
from django_facebook.models import FacebookCustomUser
from models import UserPreferences
import re
alnum_re = re.compile(r'^\w+$') # regexp. from jamesodo in #django

#from django.contrib.auth.models import User
from emailconfirmation.models import EmailAddress
from models import GENDER_CHOICES, UserPreferences
# this code based in-part on django-registration
from chimpusers.models import UserSubscription
import datetime
from PIL import Image
from django.core.files.storage import default_storage
import StringIO

class SignupForm(forms.Form, FieldsetMixin):
    
    email = forms.EmailField(label="Your Email", required=True, widget=forms.TextInput())
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Password (again)", widget=forms.PasswordInput())
    FirstName = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(), required=False)
    LastName = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(), required=False)
    Gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES, required=False)
    BirthDay = forms.DateField(required=False)
    mailchimp = forms.BooleanField(
            label = "Mailchimp",
            initial=True,
            required=False,
            help_text = "Get informed about transifex service notifications, like outages and new features. You can unsubscribe at any time from your account's profile.",
        )

    def clean_email(self):
        try:
            self.user = FacebookCustomUser.objects.get(email__exact=self.cleaned_data["email"])
        except FacebookCustomUser.DoesNotExist:
            return self.cleaned_data["email"]
        raise forms.ValidationError(u"This email is already taken. Please choose another.")

    def clean_password1(self):
        return self.cleaned_data["password1"]

    def clean(self):
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError(u"You must type the same password each time.")
        return self.cleaned_data
    
    def save(self):
        print self.cleaned_data
        username = self.cleaned_data["email"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password1"]
        new_user = FacebookCustomUser.objects.create_user(username, email, password)

        new_userPreference = UserPreferences.objects.create(
            user = new_user,
            FirstName = self.cleaned_data["FirstName"],
            LastName = self.cleaned_data["LastName"],
            Gender = self.cleaned_data["Gender"],
            BirthDay = self.cleaned_data["BirthDay"],
        )
        if email:
            #self.user.message_set.create(message="Confirmation email sent to %s" % email)
            EmailAddress.objects.add_email(new_user, email)

        #subscribe mailchimp
        if self.cleaned_data["mailchimp"]:
            subscription = UserSubscription.objects.get(user=new_user)
            birthday = self.cleaned_data["BirthDay"].strftime('%Y-%m-%d')
            if subscription.is_subscribed():
                pass
            else:
                optin_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                optin_ip = getattr(settings, 'MAILCHIMP_TEST_IP', '184.106.168.48')
                merge = {'OPTIN_TIME': optin_time, 'OPTIN_IP': optin_ip,
                'FNAME': self.cleaned_data["FirstName"],
                'LNAME': self.cleaned_data["LastName"],
                'BDAY': birthday,
                'GENDER': self.cleaned_data["Gender"],
                }
                subscription.subscribe(merge_vars=merge, double_optin=False)
                subscription.sync()

        return username, password # required for authenticate()

class UserPreferencesForm(forms.Form, FieldsetMixin):
    """A fancy registration form"""
    fieldsets = (
        (u'Persional Info', {'fields': ('FirstName', 'LastName', 'Gender', 'BirthDay', 'ProfilePicturePath')}),
        (u'Preferences Info', {'fields': ('Location',
                                      'Categories',
                                      'Brands',
                                      'Price',
                                      'Color',)}),
    )

    #UserPreferences
    user = None
    FirstName = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(), required=False)
    LastName = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(), required=False)
    Gender = forms.ChoiceField(widget=forms.RadioSelect, choices=GENDER_CHOICES, required=True)
    BirthDay = forms.DateField(required=False)
    ProfilePicturePath = forms.ImageField(required=False)
    Location = forms.CharField(label="Location", max_length=200, widget=forms.TextInput(), required=False)
    Categories = forms.CharField(label="Categories", max_length=1000, widget=forms.TextInput(), required=False)
    Brands = forms.CharField(label="Brands", max_length=1000, widget=forms.TextInput(), required=False)
    Price = forms.CharField(label="Price", max_length=1000, widget=forms.TextInput(), required=False)
    Color = forms.CharField(label="Color", max_length=1000, widget=forms.TextInput(), required=False)

    def __init__(self, post, data=None, user=None):
        if post is not None:
            super(UserPreferencesForm, self).__init__(data=post)
        else:
            super(UserPreferencesForm, self).__init__()
        self.user = user
        if data is not None:
            self.fields["FirstName"].initial = data.FirstName
            self.fields["LastName"].initial = data.LastName
            self.fields["Gender"].initial = data.Gender
            self.fields["BirthDay"].initial = data.BirthDay
            self.fields["ProfilePicturePath"].initial = data.ProfilePicturePath
            self.fields["Location"].initial = data.Location
            self.fields["Categories"].initial = data.Categories
            self.fields["Brands"].initial = data.Brands
            self.fields["Price"].initial = data.Price
            self.fields["Color"].initial = data.Color

        #self.fields['ProfilePicturePath'].widget = forms.ImageField(attrs={'class':'ProfilePicturePath',})



    def clean(self):
        return self.cleaned_data

    def save(self, request):
        print self.cleaned_data

        if len(request.FILES) > 0:
            i = datetime.datetime.now()
            uploadedImage = request.FILES["ProfilePicturePath"]
            s_month = str(i.month)
            if int(i.month) < 10:
                s_month = "0" + str(i.month)
            s_day = str(i.day)
            if int(i.day) < 10:
                s_day = "0" + str(i.day)
            imgpath = 'uploads/profile_pictures/%s/%s/%s/%s' % (i.year, s_month, s_day, uploadedImage.name)
            #raise Exception("for debug: %s" % imgpath)
            #imgpath = 'uploads/userpreferences/%s/%s/%s/' % (i.year, i.month, i.day)
            #imgpath = 'uploads/userpreferences/%s/%s/%s/' % (i.year, i.month, i.day)
            #imgpath = imgpath + str(self.user.id)+uploadedImage.name

            #d = "%suploads/userpreferences" % settings.MEDIA_ROOT
            #if not os.path.exists(d):
            #    os.makedirs(d)
            #d = "%s/%s" % (d, i.year)
            #if not os.path.exists(d):
            #    os.makedirs(d)
            #d = "%s/%s" % (d, i.month)
            #if not os.path.exists(d):
            #    os.makedirs(d)
            #d = "%s/%s" % (d, i.day)
            #if not os.path.exists(d):
            #    os.makedirs(d)

            #destination = open("%s%s" % (settings.MEDIA_ROOT, imgpath), "wb+")
            #for chunk in uploadedImage.chunks():
            #    destination.write(chunk)
            #destination.close()
        else:
            imgpath = ""

        userpreferences = self.user.userpreferences_set.all()
        if len(userpreferences) > 0:
            userpreference = userpreferences[0]
            userpreference.user = self.user
            userpreference.FirstName = self.cleaned_data["FirstName"]
            userpreference.LastName = self.cleaned_data["LastName"]
            userpreference.Gender = self.cleaned_data["Gender"]
            userpreference.BirthDay = self.cleaned_data["BirthDay"]

            if len(request.FILES) > 0:
                #userpreference.ProfilePicturePath = imgpath
                userpreference.ProfilePicturePath = uploadedImage
            if request.POST.get('ProfilePicturePath-clear', False) == 'on':
                userpreference.ProfilePicturePath = ""

            userpreference.Location = self.cleaned_data["Location"]
            userpreference.Categories = self.cleaned_data["Categories"]
            userpreference.Brands = self.cleaned_data["Brands"]
            userpreference.Price = self.cleaned_data["Price"]
            userpreference.Color = self.cleaned_data["Color"]

            userpreference.save()

        else:
            new_userPreference = UserPreferences.objects.create(
                user = self.user,
                FirstName = self.cleaned_data["FirstName"],
                LastName = self.cleaned_data["LastName"],
                Gender = self.cleaned_data["Gender"],
                BirthDay = self.cleaned_data["BirthDay"],
                #ProfilePicturePath = imgpath,
                ProfilePicturePath = uploadedImage,
                Location = self.cleaned_data["Location"],
                Categories = self.cleaned_data["Categories"],
                Brands = self.cleaned_data["Brands"],
                Price = self.cleaned_data["Price"],
                Color = self.cleaned_data["Color"],
            )

        #manipulate image dimension
        if len(imgpath) > 0:
            img_file = default_storage.open(imgpath, 'r')
            im = StringIO.StringIO(img_file.read())
            img_file.close()
            resized_image = Image.open(im)
            nx, ny = resized_image.size
            ratio = 1.0
            max_dimension = float(300)
            if nx > max_dimension or nx > max_dimension:
                if nx > ny:
                    ratio = max_dimension / float(nx)
                else:
                    ratio = max_dimension / float(ny)
            resized_image = resized_image.resize((int(nx * ratio),int(ny * ratio)), Image.ANTIALIAS)
            #resized_image = resized_image.resize((int(max_dimension), int(max_dimension)), Image.ANTIALIAS)
            imgstring = StringIO.StringIO()
            resized_image = resized_image.convert('RGB')
            resized_image.save(imgstring, 'JPEG')

            img_file2 = default_storage.open(imgpath, 'w')
            img_file2.write(imgstring.getvalue())
            img_file2.close()

        self.user.first_name = self.cleaned_data["FirstName"]
        self.user.last_name = self.cleaned_data["LastName"]
        self.user.gender = self.cleaned_data["Gender"]
        self.user.date_of_birth = self.cleaned_data["BirthDay"]
        self.user.save()

        #update mailchimp
        if self.user.mailchimp_set.all()[0].MailChimpAllowed:
            subscription = UserSubscription.objects.get(user=self.user)
            birthday = self.cleaned_data["BirthDay"].strftime('%Y-%m-%d')
            if subscription.is_subscribed():
                optin_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                optin_ip = getattr(settings, 'MAILCHIMP_TEST_IP', '184.106.168.48')
                merge = {'OPTIN_TIME': optin_time, 'OPTIN_IP': optin_ip,
                'FNAME': self.cleaned_data["FirstName"],
                'LNAME': self.cleaned_data["LastName"],
                'BDAY': birthday,
                'GENDER': self.cleaned_data["Gender"],
                'LOC': self.cleaned_data["Location"],
                'PIC': imgpath,
                'CAT': self.cleaned_data["Categories"],
                'BRAND': self.cleaned_data["Brands"],
                'PRICE': self.cleaned_data["Price"],
                'COLOR': self.cleaned_data["Color"],
                }
                subscription.update(merge_vars=merge)
                subscription.sync()
            else:
                optin_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                optin_ip = getattr(settings, 'MAILCHIMP_TEST_IP', '184.106.168.48')
                merge = {'OPTIN_TIME': optin_time, 'OPTIN_IP': optin_ip,
                'FNAME': self.cleaned_data["FirstName"],
                'LNAME': self.cleaned_data["LastName"],
                'BDAY': birthday,
                'GENDER': self.cleaned_data["Gender"],
                'LOC': self.cleaned_data["Location"],
                'PIC': imgpath,
                'CAT': self.cleaned_data["Categories"],
                'BRAND': self.cleaned_data["Brands"],
                'PRICE': self.cleaned_data["Price"],
                'COLOR': self.cleaned_data["Color"],
                }
                subscription.subscribe(merge_vars=merge, double_optin=False)
                subscription.sync()

class AddEmailForm(forms.Form):
    
    def __init__(self, data=None, user=None):
        super(AddEmailForm, self).__init__(data=data)
        self.user = user

    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput())
    
    def clean_email(self):
        try:
            EmailAddress.objects.get(user=self.user, email=self.cleaned_data["email"])
        except EmailAddress.DoesNotExist:
            return self.cleaned_data["email"]
        raise forms.ValidationError(u"This email address already associated with this account.")
    
    def save(self):
        #self.user.message_set.create(message="Confirmation email sent to %s" % self.cleaned_data["email"])
        return EmailAddress.objects.add_email(self.user, self.cleaned_data["email"])
        