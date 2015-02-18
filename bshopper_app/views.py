from django.conf import settings
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson as json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from forms import SignupForm, AddEmailForm, UserPreferencesForm
from emailconfirmation.models import EmailAddress, EmailConfirmation

from models import MailChimp,Categories,Manufacturer, User_Viewership, Trending_Products, ScrapedItems, Merchants, Product_Color, Top_Manufacturer
from django_facebook.models import FacebookCustomUser
from datetime import datetime, timedelta
import urllib2
from xml.dom import minidom
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

def fbtest(request):
    context = RequestContext(request)
    return render_to_response('fbtest.html', context)

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username, password = form.save()
            user = authenticate(username=username, password=password)
            login(request, user)

            mailchimps = request.user.mailchimp_set.all()
            mailchimp_allowed = form.cleaned_data["mailchimp"]
            if len(mailchimps) > 0:
                mailchimp = mailchimps[0]
                mailchimp.MailChimpAllowed = mailchimp_allowed
                mailchimp.save()
            else:
                new_mailchimp = MailChimp.objects.create(
                    user = request.user,
                    MailChimpAllowed = mailchimp_allowed,
                 )

            return HttpResponseRedirect("/")
    else:
        form = SignupForm()
    return render_to_response("signup.html", {
        "form": form,
    }, context_instance=RequestContext(request))

def user_preferences(request):
    if request.method == "POST":
        form = UserPreferencesForm(request.POST, None, request.user)
        if form.is_valid():
            form.save(request)
            #return HttpResponseRedirect("/")
    else:
        if len(request.user.userpreferences_set.all()) > 0:
            userpreference = request.user.userpreferences_set.all()[0]
        else:
            userpreference = None
        form = UserPreferencesForm(None, userpreference, request.user)
        print(form.as_p())
    return render_to_response("user_preferences.html", {
       "form": form,
       #"image_path":
    }, context_instance=RequestContext(request))

@csrf_exempt
@login_required
def user_setting_ajax_get_Manufacturer(request):
    Manufacturer_result = Manufacturer.objects.all()[:1000]
    #Manufacturer_result = Manufacturer.objects.all()
    str_result = ""

    if len(request.user.userpreferences_set.all()) > 0:
        userpreference = request.user.userpreferences_set.all()[0]
    else:
        userpreference = None
    form = UserPreferencesForm(None, userpreference, request.user)
    t_brands = "," + form.fields["Brands"].initial + ","
    for object in Manufacturer_result:
        str_result += "<option value='" + str(object.Manufacturer_id) + "'"
        t_brandid = "," + str(object.Manufacturer_id) + ","
        if t_brandid in t_brands:
            str_result += " class='selected' "
        str_result += ">" + object.Manufacturer_Name + "</option>"

    to_json = {}
    to_json['return_code'] = "success"
    to_json['result'] = str_result
    #raise Exception("for debug: %s" % str_result)
    return HttpResponse(json.dumps(to_json), mimetype="application/json")

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

@csrf_exempt
def BShopperServices_getProducts(request):
    product_type="recommended"
    pageNo="1"
    min_price="null"
    max_price="null"
    brand="null"
    categories="null"
    color="null"
    #if request.method == "POST":
    product_type = request.REQUEST['product_type']
    pageNo = request.REQUEST['pageNo']
    min_price = request.REQUEST['min_price']
    max_price = request.REQUEST['max_price']
    brand = request.REQUEST['brand']
    categories = request.REQUEST['categories']
    color = request.REQUEST['color']
    #http://ec2-184-73-119-200.compute-1.amazonaws.com:8080/BShopperServices/services/RecommendationServiceImplPort/getNewProducts
    # ?userId=27&brand=&categories=4&color=&minPrice=5&maxPrice=7&pageNo=1
    servicepath = ""
    if product_type == "recommended":
        #if request.user.is_authenticated():
        servicepath = "http://ec2-184-73-119-200.compute-1.amazonaws.com:8080/BShopperServices/services/RecommendationServiceImplPort/getRecommendations?"
        servicepath += "userId=" + str(request.user.id)
        #servicepath += "userId=" + "21"
        servicepath += "&pageNo=" + str(pageNo)
    elif product_type == "trending":
        servicepath = "http://ec2-184-73-119-200.compute-1.amazonaws.com:8080/BShopperServices/services/RecommendationServiceImplPort/getTrendingProducts?"
        servicepath += "pageNo=" + str(pageNo)
    elif product_type == "newest":
        servicepath = "http://ec2-184-73-119-200.compute-1.amazonaws.com:8080/BShopperServices/services/RecommendationServiceImplPort/getNewProducts?"
        servicepath += "pageNo=" + str(pageNo)

    servicepath += "&pageNo=" + str(pageNo)
    if brand != "null":
        servicepath += "&brand=" + brand
    if categories != "null":
        servicepath += "&categories=" + categories
    if color != "null":
        servicepath += "&color=" + color
    if min_price != "null":
        if min_price == "500":
            min_price -= 1
        servicepath += "&minPrice=" + min_price
    if max_price != "null":
        if max_price != "500":
            servicepath += "&maxPrice=" + max_price
    #raise Exception(product_type)
    response = urllib2.urlopen(servicepath).read()
    dom = minidom.parseString(response)
    total_cnt = 0
    result = []
    for node in dom.getElementsByTagName('return'):
        item = {}
        categoryId = node.getElementsByTagName("categoryId")[0]
        #print "categoryId: %s" % getText(categoryId.childNodes)
        color = node.getElementsByTagName("color")[0]
        #print "color: %s" % getText(color.childNodes)
        description = node.getElementsByTagName("description")[0]
        #print "description: %s" % getText(description.childNodes)
        images = node.getElementsByTagName("images")[0]
        #print "images: %s" % getText(images.childNodes)
        images_json = node.getElementsByTagName("images_json")[0]
        #print "images_json: %s" % getText(images_json.childNodes)
        manufacturer = node.getElementsByTagName("manufacturer")[0]
        #print "manufacturer: %s" % getText(manufacturer.childNodes)
        productId = node.getElementsByTagName("productId")[0]
        #print "productId: %s" % getText(productId.childNodes)
        rating = node.getElementsByTagName("rating")[0]
        #print "rating: %s" % getText(rating.childNodes)
        retail_price = node.getElementsByTagName("retail_price")[0]
        #print "retail_price: %s" % getText(retail_price.childNodes)
        sale_price = node.getElementsByTagName("sale_price")[0]
        #print "sale_price: %s" % getText(sale_price.childNodes)
        size = node.getElementsByTagName("size")[0]
        #print "size: %s" % getText(size.childNodes)
        sku = node.getElementsByTagName("sku")[0]
        #print "sku: %s" % getText(sku.childNodes)
        spider_name = node.getElementsByTagName("spider_name")[0]
        #print "spider_name: %s" % getText(spider_name.childNodes)
        title = node.getElementsByTagName("title")[0]
        #print "title: %s" % getText(title.childNodes)
        url = node.getElementsByTagName("url")[0]
        #print "url: %s" % getText(url.childNodes)
        spider_name = node.getElementsByTagName("spider_name")[0]
        #print "spider_name: %s" % getText(spider_name.childNodes)
        userId = node.getElementsByTagName("userId")[0]
        #print "userId: %s" % getText(userId.childNodes)
        total_cnt += 1
        #raise Exception("for debug: %s" % getText(images_json.childNodes))
        #imageJson = json.loads( getText(images_json.childNodes) )
        #print "imageJson: " + imageJson["url"]
        #print "imageJson: " + imageJson[0]["url"]

        if len( getText(images.childNodes) ) > 0:
            item["productId"] = getText(productId.childNodes)
            CDN_url = "http://d3euhvysnzl3oa.cloudfront.net/"
            item["image"] = CDN_url + getText(images.childNodes).split(",")[0]
            item["image"] = item["image"].replace("full/", "thumbs/big/")
            item["width"] = 220
            item["height"] = 331
            item["url"] = getText(url.childNodes)

            t_title = getText(title.childNodes)
            if len( t_title ) > 35:
                t_title = t_title[:35] + "..."
            item["title"] = t_title

            #t_title = getText(title.childNodes)
            #if len( t_title ) > 20:
            #    t_title = t_title[:20] + "..."
            #item["short_title"] = t_title.replace("\n", " ")

            t_desc = getText(description.childNodes)
            if len( t_desc ) > 100:
                t_desc = t_desc[:100] + "..."
            item["description"] = t_desc

            item["retail_price"] = getText(retail_price.childNodes)
            item["sale_price"] = "$" + getText(sale_price.childNodes)
            if item["sale_price"] == "$0":
                item["sale_price"] = ""

            #get Like/Dislike
            likeproduct = "not_set_product"
            userId = ""
            if request.user.is_authenticated():
                userId = request.user.id
            if userId != '':
                try:
                    userviewership = User_Viewership.objects.get(UserId = int(userId), ProductId = int(item["productId"]))
                    if userviewership.LikeProduct == 0:
                        likeproduct = "disliked_product"
                    if userviewership.LikeProduct == 1:
                        likeproduct = "liked_product"
                except ObjectDoesNotExist:
                    likeproduct = "not_set_product"
            item["likeproduct"] = likeproduct

            result.append(item)

#    to_json = {}
#    to_json['total'] = str(total_cnt)
#    to_json['result'] = result
    #raise Exception("for debug: %s" % str_result)
#    return HttpResponse(json.dumps(to_json), mimetype="application/json")
    to_json = {}
    to_json['rendered_string'] = render_to_string('waterfall_area.html',
                                   {'total':str(total_cnt),'result':result},
                                   context_instance=RequestContext(request))
    to_json['total_cnt'] = total_cnt
    return HttpResponse(json.dumps(to_json), mimetype='application/json')

@login_required
def user_setting(request):
    successfully_saved = 0
    if request.method == "POST":
        form = UserPreferencesForm(request.POST, None, request.user)
        if form.is_valid():
            form.save(request)
            successfully_saved = 1
            #return HttpResponseRedirect("/")
    if len(request.user.userpreferences_set.all()) > 0:
        userpreference = request.user.userpreferences_set.all()[0]
    else:
        userpreference = None

    form = UserPreferencesForm(None, userpreference, request.user)
    print(form.as_p())

    birthday = form.fields["BirthDay"].initial
    birthday_sep = [birthday.year, birthday.month, birthday.day]
    opposite_Gender = "m"
    if form.fields["Gender"].initial == "f":
        opposite_Gender = "m"
    else:
        opposite_Gender = "f"

    Categories_result = Categories.objects.exclude(Gender=opposite_Gender)
    #Categories_result = Categories.objects.all()
    Manufacturer_result = Manufacturer.objects.all()

    return render_to_response("users-setting.html", {
       "form": form,
       #"image_path":
       "yearlst": range(datetime.now().year, datetime.now().year-100, -1),
       "monthlst": range(1, 13),
       "datelst": range(1, 32),
       "birthday_sep": birthday_sep,
       "Categories": Categories_result,
       "Manufacturer": Manufacturer_result,
       "successfully_saved": successfully_saved,
       "gender": form.fields["Gender"].initial
    }, context_instance=RequestContext(request))

def waterfall_area(request):
    type = "null"
    category = "null"
    brands = "null"
    min_price = "null"
    max_price = "null"
    color = "null"

    if type == "null":
        if request.user.is_authenticated():
            type = "recommended"
        else:
            type = "trending"
    Top_Manufacturers = Top_Manufacturer.objects.all()[:50]
    return render_to_response("waterfall_area.html", {
        "user": request.user,
        "Top_Manufacturers": Top_Manufacturers,
        "type": type,
        "category": category,
        "brands": brands,
        "min_price": min_price,
        "max_price": max_price,
        "color": color,
    }, context_instance=RequestContext(request))

def homepage(request):
    if request.method == "POST" and request.user.is_authenticated():
        if request.POST["action"] == "add":
            add_email_form = AddEmailForm(request.POST, request.user)
            if add_email_form.is_valid():
                add_email_form.save()
        elif request.POST["action"] == "send":
            email = request.POST["email"]
            try:
                email_address = EmailAddress.objects.get(user=request.user, email=email)
                #request.user.message_set.create(message="Confirmation email sent to %s" % email)
                EmailConfirmation.objects.send_confirmation(email_address)
            except EmailAddress.DoesNotExist:
                pass
            add_email_form = AddEmailForm()
    else:
        add_email_form = AddEmailForm()

    return render_to_response("homepage.html", {
        "user": request.user,
        "messages": "",
        "add_email_form": add_email_form,
    }, context_instance=RequestContext(request))

def ui_index(request):
    type = "null"
    category = "null"
    brands = "null"
    min_price = "null"
    max_price = "null"
    color = "null"

    if type == "null":
        if request.user.is_authenticated():
            type = "recommended"
        else:
            type = "trending"
    Top_Manufacturers = Top_Manufacturer.objects.all()[:50]
    return render_to_response("index.html", {
        "user": request.user,
        "Top_Manufacturers": Top_Manufacturers,
        "type": type,
        "category": category,
        "brands": brands,
        "min_price": min_price,
        "max_price": max_price,
        "color": color,
    }, context_instance=RequestContext(request))

def ui_index_with_param(request):
    #raise Exception(type + ", " + search_query)
    type = "null"
    category = "null"
    brands = "null"
    min_price = "null"
    max_price = "null"
    color = "null"

    if request.method == "POST":
        type = request.POST["type"]
        category = request.POST["category"]
        brands = request.POST["brands"]
        min_price = request.POST["min_price"]
        max_price = request.POST["max_price"]
        color = request.POST["color"]

    if type == "null":
        if request.user.is_authenticated():
            type = "recommended"
        else:
            type = "trending"

    Top_Manufacturers = Top_Manufacturer.objects.all()[:50]

    return render_to_response("index.html", {
        "user": request.user,
        "Top_Manufacturers": Top_Manufacturers,
        "type": type,
        "category": category,
        "brands": brands,
        "min_price": min_price,
        "max_price": max_price,
        "color": color,
    }, context_instance=RequestContext(request))

def ui_page_2col(request):
    return render_to_response("page-2col.html", {
    }, context_instance=RequestContext(request))
def ui_users_setting(request):
    return render_to_response("users-setting.html", {
    }, context_instance=RequestContext(request))

@csrf_exempt
def ajax_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
#            already_exist = False
#            try:
#                user = FacebookCustomUser.objects.get(email__exact=form.cleaned_data["email"])
#                already_exist = True
#            except FacebookCustomUser.DoesNotExist:
#                already_exist = False
#            if not already_exist:
            username, password = form.save()
            user = authenticate(username=username, password=password)
            login(request, user)

            mailchimps = request.user.mailchimp_set.all()
            mailchimp_allowed = form.cleaned_data["mailchimp"]
            if len(mailchimps) > 0:
                mailchimp = mailchimps[0]
                mailchimp.MailChimpAllowed = mailchimp_allowed
                mailchimp.save()
            else:
                new_mailchimp = MailChimp.objects.create(
                    user = request.user,
                    MailChimpAllowed = mailchimp_allowed,
                 )
            to_json = {}
            to_json['return_code'] = "success"
            return HttpResponse(json.dumps(to_json), mimetype="application/json")

    to_json = {}
    to_json['return_code'] = "email_exist"
    return HttpResponse(json.dumps(to_json), mimetype="application/json")

@csrf_exempt
def ajax_acc_welcome(request):
    if request.method == "POST":
        gender = request.POST.get('gender','n')
        Categories = request.POST.get('Categories','')

        userpreferences = request.user.userpreferences_set.all()
        if len(userpreferences) > 0:
            userpreference = userpreferences[0]
            userpreference.Gender = gender
            userpreference.Categories = Categories
            userpreference.save()

            to_json = {}
            to_json['return_code'] = "success"
            return HttpResponse(json.dumps(to_json), mimetype="application/json")

    to_json = {}
    to_json['return_code'] = "failed"
    return HttpResponse(json.dumps(to_json), mimetype="application/json")

@csrf_exempt
def ajax_product_like_dislike(request):
    if request.method == "POST":
        like = request.POST.get('like','1')
        productId = request.POST.get('productId','')
        #userId = request.POST.get('userId','')
        userId = ""
        if request.user.is_authenticated():
            userId = request.user.id

        #raise Exception("UserId: %s" % userId)
        if userId != '':
            try:
                userviewership = User_Viewership.objects.get(UserId = int(userId), ProductId = int(productId))
                userviewership.LikeProduct = int(like)
                userviewership.save()
            except ObjectDoesNotExist:
                userviewership = User_Viewership.objects.create(UserId = int(userId), ProductId = int(productId), LikeProduct = int(like), NoOfViews = 0)
                #userviewershipsend = User_Viewership.objects.create(UserId = 4, ProductId = 3, LikeProduct = 1, NoOfViews = 0)

        #trendingproducts = Trending_Products.objects.create(id = 2, UserId = 2, ProductId = 2, TransactionDate = datetime.now())
        #if userId == "":
        #    userId = 0
        #trendingproducts = Trending_Products.objects.create(UserId = userId, ProductId = int(productId))

        to_json = {}
        to_json['return_code'] = "success"
        return HttpResponse(json.dumps(to_json), mimetype="application/json")


    to_json = {}
    to_json['return_code'] = "failed"
    return HttpResponse(json.dumps(to_json), mimetype="application/json")

def set_cookie(response, key, value, days_expire = 7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  #one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

@csrf_exempt
def product_details(request, productId):
    #add recored for Trending_Products
    userId = "0"
    if request.user.is_authenticated():
        userId = request.user.id
    Trending_Products.objects.create(UserId = userId, ProductId = productId)

    try:
        scrapeditem = ScrapedItems.objects.get(id = int(productId))
        scrapeditem.retail_price = "%0.2f" % scrapeditem.retail_price
        if len(scrapeditem.description) > 1000:
            scrapeditem.description = scrapeditem.description[:1000] + "..."
        image_urls_arr = scrapeditem.image_urls.split(",")
        images_arr = scrapeditem.images.split(",")
        product_imgs = []
        product_thumb_imgs = []
        idx = 0
        while idx < len(images_arr):
            #imgurl = image_urls_arr[idx]
            #imgurl.replace("$detailMain$", images_arr[idx])
            CDN_url = "http://d3euhvysnzl3oa.cloudfront.net/"
            imgurl = CDN_url + images_arr[idx]
            product_imgs.append(imgurl)
            thumb_imgurl = imgurl.replace("full/", "thumbs/small/")
            product_thumb_imgs.append(thumb_imgurl)
            idx += 1

        sizes_arr = scrapeditem.size.split(",")
        sizes = []
        idx = 0
        while idx < len(sizes_arr):
            if len(sizes_arr[idx].strip()) > 0 and sizes_arr[idx].strip() != "ONE SIZE":
                sizes.append(sizes_arr[idx].strip())
            idx += 1
        scrapeditem.predicted_category_name_fmt = scrapeditem.predicted_category_name.replace(",", ", ")

    except ObjectDoesNotExist:
        scrapeditem = None

    #get similar products
    #http://ec2-184-73-119-200.compute-1.amazonaws.com:8080/BShopperServices/services/RecommendationServiceImplPort/getSimilarProducts?productId=1&pageNo=1
    servicepath = "http://ec2-184-73-119-200.compute-1.amazonaws.com:8080/BShopperServices/services/RecommendationServiceImplPort/getSimilarProducts?"
    servicepath += "productId=" + str(productId)
    pageNo = 1
    servicepath += "&pageNo=" + str(pageNo)

    response = urllib2.urlopen(servicepath).read()
    dom = minidom.parseString(response)
    similar_products = []
    for node in dom.getElementsByTagName('return'):
        #print "similar_productId: %s" % getText(node.childNodes)
        try:
            similar_productId = getText(node.childNodes)
            similar_scrapeditem = ScrapedItems.objects.get(id = int(similar_productId))
            similarsend_scrapeditem.retail_price = "%0.2f" % similar_scrapeditem.retail_price

            similar_image_urls_arr = similar_scrapeditem.image_urls.split(",")
            similar_images_arr = similar_scrapeditem.images.split(",")
            similar_product_imgs = []
            idx = 0
            while idx < len(similar_images_arr):
                #imgurl = similar_images_arr[idx]
                #imgurl.replace("$detailMain$", similar_images_arr[idx])
                CDN_url = "http://d3euhvysnzl3oa.cloudfront.net/"
                imgurl = CDN_url + similar_images_arr[idx]
                similar_product_imgs.append( imgurl.replace("full/", "thumbs/big/") )
                idx += 1
            similar_scrapeditem.product_imgs = similar_product_imgs
            similar_products.append(similar_scrapeditem)
        except:
            pass

    #get cookie
    recently_viewed = ["","","","",""]
    if request.COOKIES.has_key( 'recently_viewed1' ):
        recently_viewed[0] = request.COOKIES[ 'recently_viewed1' ]
    if request.COOKIES.has_key( 'recently_viewed2' ):
        recently_viewed[1] = request.COOKIES[ 'recently_viewed2' ]
    if request.COOKIES.has_key( 'recently_viewed3' ):
        recently_viewed[2] = request.COOKIES[ 'recently_viewed3' ]
    if request.COOKIES.has_key( 'recently_viewed4' ):
        recently_viewed[3] = request.COOKIES[ 'recently_viewed4' ]
    if request.COOKIES.has_key( 'recently_viewed5' ):
        recently_viewed[4] = request.COOKIES[ 'recently_viewed5' ]

    recently_products = []
    for recently_viewed_item in recently_viewed:
        #print "recviewed_product: %s" % recently_products
        if len(recently_viewed_item) == 0:
            continue
        try:
            recently_scrapeditem = ScrapedItems.objects.get(id = int(recently_viewed_item))
            recently_scrapeditem.retail_price = "%0.2f" % recently_scrapeditem.retail_price

            recently_image_urls_arr = recently_scrapeditem.image_urls.split(",")
            recently_images_arr = recently_scrapeditem.images.split(",")
            recently_product_imgs = []
            idx = 0
            while idx < len(recently_images_arr):
                #imgurl = similar_images_arr[idx]
                #imgurl.replace("$detailMain$", similar_images_arr[idx])
                CDN_url = "http://d3euhvysnzl3oa.cloudfront.net/"
                imgurl = CDN_url + recently_images_arr[idx]
                recently_product_imgs.append( imgurl.replace("full/", "thumbs/big/") )
                idx += 1
            recently_scrapeditem.product_imgs = recently_product_imgs
            recently_products.append(recently_scrapeditem)
        except:
            pass

    #get Like/Dislike
    likeproduct = "not_set_product"
    if userId != '0':
        try:
            userviewership = User_Viewership.objects.get(UserId = int(userId), ProductId = int(productId))
            if userviewership.LikeProduct == 0:
                likeproduct = "disliked_product"
            if userviewership.LikeProduct == 1:
                likeproduct = "liked_product"
        except ObjectDoesNotExist:
            likeproduct = "not_set_product"

    #get Merchants record
    merch_name = ""
    if scrapeditem is not None:
        try:
            merchants_rec = Merchants.objects.get(merch_id = scrapeditem.spider_name)
            merch_name = merchants_rec.merch_name
        except ObjectDoesNotExist:
            pass
    #get Product_Color record
    Hex = ""
    if scrapeditem is not None:
        try:
            merchants_rec = Product_Color.objects.get(ProductId = scrapeditem.id)
            Hex = merchants_rec.Hex
        except ObjectDoesNotExist:
            pass

    #raise Exception(product_imgs)
    response = render_to_response("product-details.html", {
        "scrapeditem": scrapeditem, "product_imgs": product_imgs, "product_thumb_imgs": product_thumb_imgs, "sizes": sizes, "similar_products": similar_products,
        "recently_products": recently_products, "likeproduct": likeproduct, "merch_name": merch_name, "Hex": Hex,
    }, context_instance=RequestContext(request))

    #set cookie
    if productId not in recently_viewed:
        set_cookie(response, 'recently_viewed1', productId)
        set_cookie(response, 'recently_viewed2', recently_viewed[0])
        set_cookie(response, 'recently_viewed3', recently_viewed[1])
        set_cookie(response, 'recently_viewed4', recently_viewed[2])
        set_cookie(response, 'recently_viewed5', recently_viewed[3])

    return response

@csrf_exempt
def ajax_share_send(request):
    if request.method == "POST":
        share_send_to = request.POST.get('share_send_to','')
        share_send_from = request.POST.get('share_send_from','')
        share_send_subject = request.POST.get('share_send_subject','')
        share_send_message = request.POST.get('share_send_message','')
        share_send_url = request.POST.get('share_send_url','')

        template = get_template('share_email.txt')
        context = Context({
            'name': share_send_to,
            'link': share_send_url,
            'sender': share_send_from,
            })
        message = template.render(context)

        #send_mail(
        #    share_send_subject, share_send_message,
        #    share_send_from, [share_send_to]
        #)
        #send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email_address.email])
        send_mail(share_send_subject, message, settings.DEFAULT_FROM_EMAIL, [share_send_to])
        to_json = {}
        to_json['return_code'] = "success"
        return HttpResponse(json.dumps(to_json), mimetype="application/json")

    to_json = {}
    to_json['return_code'] = "failed"
    return HttpResponse(json.dumps(to_json), mimetype="application/json")
