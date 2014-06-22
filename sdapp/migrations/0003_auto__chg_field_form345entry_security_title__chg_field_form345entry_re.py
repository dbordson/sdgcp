# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Form345Entry.security_title'
        db.alter_column(u'sdapp_form345entry', 'security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True))

        # Changing field 'Form345Entry.reporting_owner_title'
        db.alter_column(u'sdapp_form345entry', 'reporting_owner_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True))

        # Changing field 'Form345Entry.reporting_owner_name'
        db.alter_column(u'sdapp_form345entry', 'reporting_owner_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True))

        # Changing field 'Form345Entry.underlying_title'
        db.alter_column(u'sdapp_form345entry', 'underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True))

    def backwards(self, orm):

        # Changing field 'Form345Entry.security_title'
        db.alter_column(u'sdapp_form345entry', 'security_title', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))

        # Changing field 'Form345Entry.reporting_owner_title'
        db.alter_column(u'sdapp_form345entry', 'reporting_owner_title', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))

        # Changing field 'Form345Entry.reporting_owner_name'
        db.alter_column(u'sdapp_form345entry', 'reporting_owner_name', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))

        # Changing field 'Form345Entry.underlying_title'
        db.alter_column(u'sdapp_form345entry', 'underlying_title', self.gf('django.db.models.fields.CharField')(max_length=40, null=True))

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
            'conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'direct_or_indirect': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'entry_internal_id': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'five_form_four_transactions': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'five_form_three_holdings': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'five_not_subject_to_section_sixteen': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'form_type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_director': ('django.db.models.fields.BooleanField', [], {}),
            'is_officer': ('django.db.models.fields.BooleanField', [], {}),
            'is_something_else': ('django.db.models.fields.BooleanField', [], {}),
            'is_ten_percent': ('django.db.models.fields.BooleanField', [], {}),
            'issuer_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.CIK']", 'null': 'True'}),
            'period_of_report': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'reporting_owner_cik': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'reporting_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'shares_following_xn': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'source_name_partial_path': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'tenbfive_note': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transaction_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'transaction_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'transaction_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transaction_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'xn_acq_disp_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'xn_price_per_share': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'})
        }
    }

    complete_apps = ['sdapp']