# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CompanyStockHist'
        db.create_table(u'sdapp_companystockhist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticker_sym', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'sdapp', ['CompanyStockHist'])

        # Adding model 'ClosePrice'
        db.create_table(u'sdapp_closeprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('close_price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('close_date', self.gf('django.db.models.fields.DateField')()),
            ('companystockhist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.CompanyStockHist'])),
        ))
        db.send_create_signal(u'sdapp', ['ClosePrice'])

        # Adding model 'CIK'
        db.create_table(u'sdapp_cik', (
            ('cik_num', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('companystockhist', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sdapp.CompanyStockHist'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'sdapp', ['CIK'])

        # Adding model 'Form345Entry'
        db.create_table(u'sdapp_form345entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('period_of_report', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('issuer_cik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.CIK'])),
            ('reporting_owner_cik', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('reporting_owner_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_director', self.gf('django.db.models.fields.BooleanField')()),
            ('is_officer', self.gf('django.db.models.fields.BooleanField')()),
            ('is_ten_percent', self.gf('django.db.models.fields.BooleanField')()),
            ('is_something_else', self.gf('django.db.models.fields.BooleanField')()),
            ('reporting_owner_title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('conversion_price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('transaction_date', self.gf('django.db.models.fields.DateField')()),
            ('transaction_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('transaction_shares', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('xn_price_per_share', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('xn_acq_disp_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('expiration_date', self.gf('django.db.models.fields.DateField')()),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('underlying_shares', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('direct_or_indirect', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('tenbfive_note', self.gf('django.db.models.fields.BooleanField')()),
            ('transaction_number', self.gf('django.db.models.fields.IntegerField')()),
            ('source_name_partial_path', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('five_not_subject_to_section_sixteen', self.gf('django.db.models.fields.BooleanField')()),
            ('five_form_three_holdings', self.gf('django.db.models.fields.BooleanField')()),
            ('five_form_four_transactions', self.gf('django.db.models.fields.BooleanField')()),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'sdapp', ['Form345Entry'])


    def backwards(self, orm):
        # Deleting model 'CompanyStockHist'
        db.delete_table(u'sdapp_companystockhist')

        # Deleting model 'ClosePrice'
        db.delete_table(u'sdapp_closeprice')

        # Deleting model 'CIK'
        db.delete_table(u'sdapp_cik')

        # Deleting model 'Form345Entry'
        db.delete_table(u'sdapp_form345entry')


    models = {
        u'sdapp.cik': {
            'Meta': {'object_name': 'CIK'},
            'cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'companystockhist': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sdapp.CompanyStockHist']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sdapp.closeprice': {
            'Meta': {'object_name': 'ClosePrice'},
            'close_date': ('django.db.models.fields.DateField', [], {}),
            'close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'companystockhist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.CompanyStockHist']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sdapp.companystockhist': {
            'Meta': {'object_name': 'CompanyStockHist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticker_sym': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        },
        u'sdapp.form345entry': {
            'Meta': {'object_name': 'Form345Entry'},
            'conversion_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'direct_or_indirect': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {}),
            'five_form_four_transactions': ('django.db.models.fields.BooleanField', [], {}),
            'five_form_three_holdings': ('django.db.models.fields.BooleanField', [], {}),
            'five_not_subject_to_section_sixteen': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_director': ('django.db.models.fields.BooleanField', [], {}),
            'is_officer': ('django.db.models.fields.BooleanField', [], {}),
            'is_something_else': ('django.db.models.fields.BooleanField', [], {}),
            'is_ten_percent': ('django.db.models.fields.BooleanField', [], {}),
            'issuer_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.CIK']"}),
            'period_of_report': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'reporting_owner_cik': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'reporting_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'source_name_partial_path': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'tenbfive_note': ('django.db.models.fields.BooleanField', [], {}),
            'transaction_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'transaction_date': ('django.db.models.fields.DateField', [], {}),
            'transaction_number': ('django.db.models.fields.IntegerField', [], {}),
            'transaction_shares': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'underlying_shares': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'xn_acq_disp_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'xn_price_per_share': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'})
        }
    }

    complete_apps = ['sdapp']