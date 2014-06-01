# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CompanyStockHist'
        db.create_table(u'stockhist_companystockhist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticker_sym', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'stockhist', ['CompanyStockHist'])

        # Adding model 'ClosePrice'
        db.create_table(u'stockhist_closeprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('close_price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('close_date', self.gf('django.db.models.fields.DateField')()),
            ('companystockhist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stockhist.CompanyStockHist'])),
        ))
        db.send_create_signal(u'stockhist', ['ClosePrice'])


    def backwards(self, orm):
        # Deleting model 'CompanyStockHist'
        db.delete_table(u'stockhist_companystockhist')

        # Deleting model 'ClosePrice'
        db.delete_table(u'stockhist_closeprice')


    models = {
        u'stockhist.closeprice': {
            'Meta': {'object_name': 'ClosePrice'},
            'close_date': ('django.db.models.fields.DateField', [], {}),
            'close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'companystockhist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stockhist.CompanyStockHist']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'stockhist.companystockhist': {
            'Meta': {'object_name': 'CompanyStockHist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticker_sym': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['stockhist']