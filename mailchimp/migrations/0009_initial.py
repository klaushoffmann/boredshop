# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Queue'
        db.create_table(u'mailchimp_queue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('contents', self.gf('django.db.models.fields.TextField')()),
            ('list_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('template_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('to_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('folder_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('tracking_opens', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tracking_html_clicks', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tracking_text_clicks', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('authenticate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('google_analytics', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('auto_footer', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('generate_text', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auto_tweet', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('segment_options', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('segment_options_all', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('segment_options_conditions', self.gf('django.db.models.fields.TextField')()),
            ('type_opts', self.gf('django.db.models.fields.TextField')()),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.TextField')(null=True)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'mailchimp', ['Queue'])

        # Adding model 'Campaign'
        db.create_table(u'mailchimp_campaign', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sent_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('campaign_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('extra_info', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal(u'mailchimp', ['Campaign'])

        # Adding model 'Reciever'
        db.create_table(u'mailchimp_reciever', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(related_name='recievers', to=orm['mailchimp.Campaign'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'mailchimp', ['Reciever'])


    def backwards(self, orm):
        # Deleting model 'Queue'
        db.delete_table(u'mailchimp_queue')

        # Deleting model 'Campaign'
        db.delete_table(u'mailchimp_campaign')

        # Deleting model 'Reciever'
        db.delete_table(u'mailchimp_reciever')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mailchimp.campaign': {
            'Meta': {'ordering': "['-sent_date']", 'object_name': 'Campaign'},
            'campaign_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'extra_info': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sent_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'mailchimp.queue': {
            'Meta': {'object_name': 'Queue'},
            'authenticate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_footer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_tweet': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'campaign_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'contents': ('django.db.models.fields.TextField', [], {}),
            'extra_info': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'folder_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'generate_text': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'google_analytics': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'segment_options': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'segment_options_all': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'segment_options_conditions': ('django.db.models.fields.TextField', [], {}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'template_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'tracking_html_clicks': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tracking_opens': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'tracking_text_clicks': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type_opts': ('django.db.models.fields.TextField', [], {})
        },
        u'mailchimp.reciever': {
            'Meta': {'object_name': 'Reciever'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recievers'", 'to': u"orm['mailchimp.Campaign']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['mailchimp']