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

        # Adding model 'IssuerCIK'
        db.create_table(u'sdapp_issuercik', (
            ('cik_num', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('companystockhist', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sdapp.CompanyStockHist'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'sdapp', ['IssuerCIK'])

        # Adding model 'ReportingPerson'
        db.create_table(u'sdapp_reportingperson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('affiliation_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('cik_num', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('first_filing', self.gf('django.db.models.fields.DateField')(null=True)),
            ('most_recent_filing', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'sdapp', ['ReportingPerson'])

        # Adding M2M table for field issuer on 'ReportingPerson'
        m2m_table_name = db.shorten_name(u'sdapp_reportingperson_issuer')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reportingperson', models.ForeignKey(orm[u'sdapp.reportingperson'], null=False)),
            ('issuercik', models.ForeignKey(orm[u'sdapp.issuercik'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reportingperson_id', 'issuercik_id'])

        # Adding model 'Holding'
        db.create_table(u'sdapp_holding', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('units_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
        ))
        db.send_create_signal(u'sdapp', ['Holding'])

        # Adding model 'Form345Entry'
        db.create_table(u'sdapp_form345entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry_internal_id', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('period_of_report', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('issuer_cik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'], null=True)),
            ('issuer_cik_num', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('reporting_owner_cik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'], null=True)),
            ('reporting_owner_cik_num', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('reporting_owner_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('is_director', self.gf('django.db.models.fields.BooleanField')()),
            ('is_officer', self.gf('django.db.models.fields.BooleanField')()),
            ('is_ten_percent', self.gf('django.db.models.fields.BooleanField')()),
            ('is_something_else', self.gf('django.db.models.fields.BooleanField')()),
            ('reporting_owner_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('transaction_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('transaction_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('transaction_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('xn_price_per_share', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('xn_acq_disp_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('underlying_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('shares_following_xn', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('direct_or_indirect', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('tenbfive_note', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('transaction_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('source_name_partial_path', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('five_not_subject_to_section_sixteen', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('five_form_three_holdings', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('five_form_four_transactions', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('form_type', self.gf('django.db.models.fields.CharField')(max_length=5, null=True)),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
        ))
        db.send_create_signal(u'sdapp', ['Form345Entry'])


    def backwards(self, orm):
        # Deleting model 'CompanyStockHist'
        db.delete_table(u'sdapp_companystockhist')

        # Deleting model 'ClosePrice'
        db.delete_table(u'sdapp_closeprice')

        # Deleting model 'IssuerCIK'
        db.delete_table(u'sdapp_issuercik')

        # Deleting model 'ReportingPerson'
        db.delete_table(u'sdapp_reportingperson')

        # Removing M2M table for field issuer on 'ReportingPerson'
        db.delete_table(db.shorten_name(u'sdapp_reportingperson_issuer'))

        # Deleting model 'Holding'
        db.delete_table(u'sdapp_holding')

        # Deleting model 'Form345Entry'
        db.delete_table(u'sdapp_form345entry')


    models = {
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
            'issuer_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']", 'null': 'True'}),
            'issuer_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'period_of_report': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'reporting_owner_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']", 'null': 'True'}),
            'reporting_owner_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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
        },
        u'sdapp.holding': {
            'Meta': {'object_name': 'Holding'},
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'units_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'})
        },
        u'sdapp.issuercik': {
            'Meta': {'object_name': 'IssuerCIK'},
            'cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'companystockhist': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['sdapp.CompanyStockHist']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'sdapp.reportingperson': {
            'Meta': {'object_name': 'ReportingPerson'},
            'affiliation_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'first_filing': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sdapp.IssuerCIK']", 'symmetrical': 'False'}),
            'most_recent_filing': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['sdapp']