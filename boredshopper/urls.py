from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'boredshopper.views.home', name='home'),
    # url(r'^boredshopper/', include('boredshopper.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bshopper_app.views.ui_index', name='home'),
    #url(r'^homepage_(?P<type>\w+)/(?P<search_query>\w*)$', 'bshopper_app.views.ui_index_with_param', name='ui_index_with_param'),
    url(r'^homepage$', 'bshopper_app.views.ui_index_with_param', name='ui_index_with_param'),
    url(r'old_home^$', 'bshopper_app.views.homepage', name='old_home'),
    (r'^admin/', include(admin.site.urls)),
    (r'^signup/$', 'bshopper_app.views.signup'),
    (r'^login/$', 'django.contrib.auth.views.login', {"template_name": "login.html", }),
    (r'^logout/$', 'django.contrib.auth.views.logout', {"template_name": "logout.html"}),
#    url(r'^login/$', 'bshopper_app.views.login', name='login'),
#    url(r'^logout/$', 'bshopper_app.views.logout', name='logout'),

    (r'^confirm_email/(\w+)/$', 'emailconfirmation.views.confirm_email'),
    url(r'^fbtest/$', 'bshopper_app.views.fbtest', name='fbtest'),
    (r'^facebook/', include('django_facebook.urls')),
    url(r'^user_preferences/$', 'bshopper_app.views.user_preferences', name='user_preferences    '),

    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
            {'post_reset_redirect' : '/accounts/password/reset/done/'}, name='password_reset'),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',
            {'post_reset_redirect' : '/accounts/password/done/'}),
    url(r'^accounts/password/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^mailchimp/', include('mailchimp.urls')),

    url(r'^ajax_signup', 'bshopper_app.views.ajax_signup', name="ajax_signup"),
    url(r'^ajax_login', 'django.contrib.auth.views.ajax_login', name="ajax_login"),
    url(r'^ajax_logout/$', 'django.contrib.auth.views.ajax_logout', name='ajax_logout'),
    url(r'^ajax_share_send/$', 'bshopper_app.views.ajax_share_send', name='ajax_share_send'),
    url(r'^ajax_acc_welcome/$', 'bshopper_app.views.ajax_acc_welcome', name='ajax_acc_welcome'),
    url(r'^user_setting/$', 'bshopper_app.views.user_setting', name='user_setting'),
    url(r'^user_setting_ajax_get_Manufacturer/$', 'bshopper_app.views.user_setting_ajax_get_Manufacturer', name='user_setting_ajax_get_Manufacturer'),
    #url(r'^wall_post_ajax/$', 'django_facebook.example_views.wall_post_ajax', name='facebook_wall_post_ajax'),
    #url(r'^BShopperServices_getProducts/(?P<product_type>\w+)/(?P<pageNo>\d+)/(?P<min_price>\w+)/(?P<max_price>\w+)/(?P<brand>\w+)/(?P<categories>\w+)/(?P<color>\w+)/$', 'bshopper_app.views.BShopperServices_getProducts', name='BShopperServices_getProducts'),
    url(r'^BShopperServices_getProducts/$', 'bshopper_app.views.BShopperServices_getProducts', name='BShopperServices_getProducts'),
    #url(r'^BShopperServices_getSimilarProducts/(?P<productId>\d+)/(?P<pageNo>\d+)/$', 'bshopper_app.views.BShopperServices_getSimilarProducts', name='BShopperServices_getSimilarProducts'),
    url(r'^ajax_product_like_dislike/$', 'bshopper_app.views.ajax_product_like_dislike', name='ajax_product_like_dislike'),
    url(r'^products/(?P<productId>\d+)/$', 'bshopper_app.views.product_details', name='product_details'),

    #url(r'^new_index', ('bshopper_app.views.ui_index')),
    url(r'^new_page_2col', ('bshopper_app.views.ui_page_2col')),
    url(r'^new_users_setting', ('bshopper_app.views.ui_users_setting')),
    (r'^share/', include('share.urls')),
)
