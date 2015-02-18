# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ScrapedItems.predicted_category'
        db.delete_column('scraped_items', 'predicted_category_id')

        # Adding field 'ScrapedItems.predicted_category_id'
        db.add_column('scraped_items', 'predicted_category_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['bshopper_app.Categories']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'ScrapedItems.predicted_category'
        db.add_column('scraped_items', 'predicted_category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['bshopper_app.Categories']),
                      keep_default=False)

        # Deleting field 'ScrapedItems.predicted_category_id'
        db.delete_column('scraped_items', 'predicted_category_id_id')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'bshopper_app.categories': {
            'CatId': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Category_name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'Category_name_hier': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'Gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'Meta': {'object_name': 'Categories'}
        },
        u'bshopper_app.facebookauth': {
            'FacebookId': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'LinkedDate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'FacebookAuth'},
            'ProductPageLikes': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'bshopper_app.mailchimp': {
            'MailChimpAllowed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'Meta': {'object_name': 'MailChimp'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'bshopper_app.manufacturer': {
            'Manufacturer_Name': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'Manufacturer_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Manufacturer', 'db_table': "'Manufacturer'"}
        },
        u'bshopper_app.scrapeditems': {
            'Meta': {'object_name': 'ScrapedItems', 'db_table': "'scraped_items'"},
            '_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duplication_check': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_urls': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'images': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'images_json': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'job_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'predicted_category_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bshopper_app.Categories']"}),
            'predicted_category_name': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'retail_price': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'sale_price': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'scraped_category': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'sku': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'spider_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '750', 'null': 'True', 'blank': 'True'})
        },
        u'bshopper_app.userpreferences': {
            'BirthDay': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'Brands': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'Categories': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'Color': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'FirstName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'LastName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'Location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'Meta': {'object_name': 'UserPreferences'},
            'Price': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'ProfilePicturePath': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_facebook.FacebookCustomUser']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_facebook.facebookcustomuser': {
            'Meta': {'object_name': 'FacebookCustomUser'},
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_open_graph': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_profile_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'new_token_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'website_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['bshopper_app']