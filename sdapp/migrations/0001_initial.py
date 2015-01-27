# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IssuerCIK'
        db.create_table(u'sdapp_issuercik', (
            ('cik_num', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal(u'sdapp', ['IssuerCIK'])

        # Adding model 'ReportingPerson'
        db.create_table(u'sdapp_reportingperson', (
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('reporting_owner_cik_num', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal(u'sdapp', ['ReportingPerson'])

        # Adding model 'Affiliation'
        db.create_table(u'sdapp_affiliation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('reporting_owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
        ))
        db.send_create_signal(u'sdapp', ['Affiliation'])

        # Adding model 'Security'
        db.create_table(u'sdapp_security', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('ticker', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
        ))
        db.send_create_signal(u'sdapp', ['Security'])

        # Adding model 'SecurityPriceHist'
        db.create_table(u'sdapp_securitypricehist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticker_sym', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'], null=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'], null=True)),
        ))
        db.send_create_signal(u'sdapp', ['SecurityPriceHist'])

        # Adding model 'ClosePrice'
        db.create_table(u'sdapp_closeprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('close_price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('close_date', self.gf('django.db.models.fields.DateField')()),
            ('SecurityPriceHist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.SecurityPriceHist'], null=True)),
        ))
        db.send_create_signal(u'sdapp', ['ClosePrice'])

        # Adding model 'SplitOrAdjustmentEvent'
        db.create_table(u'sdapp_splitoradjustmentevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'])),
            ('adjustment_factor', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=4)),
            ('event_date', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'sdapp', ['SplitOrAdjustmentEvent'])

        # Adding model 'FTPFileList'
        db.create_table(u'sdapp_ftpfilelist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('files', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'sdapp', ['FTPFileList'])

        # Adding model 'FullForm'
        db.create_table(u'sdapp_fullform', (
            ('sec_path', self.gf('django.db.models.fields.CharField')(max_length=150, primary_key=True)),
            ('save_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('issuer_cik_num', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'sdapp', ['FullForm'])

        # Adding model 'Form345Entry'
        db.create_table(u'sdapp_form345entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry_internal_id', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('period_of_report', self.gf('django.db.models.fields.DateField')(null=True)),
            ('issuer_cik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'], null=True)),
            ('issuer_cik_num', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('securty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'], null=True)),
            ('reporting_owner_cik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'], null=True)),
            ('reporting_owner_cik_num', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('reporting_owner_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('is_director', self.gf('django.db.models.fields.BooleanField')()),
            ('is_officer', self.gf('django.db.models.fields.BooleanField')()),
            ('is_ten_percent', self.gf('django.db.models.fields.BooleanField')()),
            ('is_something_else', self.gf('django.db.models.fields.BooleanField')()),
            ('reporting_owner_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('short_sec_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('transaction_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('transaction_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('transaction_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('xn_price_per_share', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('xn_acq_disp_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('scrubbed_underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('underlying_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('shares_following_xn', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('direct_or_indirect', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('tenbfive_note', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('transaction_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sec_path', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('five_not_subject_to_section_sixteen', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('five_form_three_holdings', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('five_form_four_transactions', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('form_type', self.gf('django.db.models.fields.CharField')(max_length=5, null=True)),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('filedatetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('supersededdt', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'sdapp', ['Form345Entry'])


    def backwards(self, orm):
        # Deleting model 'IssuerCIK'
        db.delete_table(u'sdapp_issuercik')

        # Deleting model 'ReportingPerson'
        db.delete_table(u'sdapp_reportingperson')

        # Deleting model 'Affiliation'
        db.delete_table(u'sdapp_affiliation')

        # Deleting model 'Security'
        db.delete_table(u'sdapp_security')

        # Deleting model 'SecurityPriceHist'
        db.delete_table(u'sdapp_securitypricehist')

        # Deleting model 'ClosePrice'
        db.delete_table(u'sdapp_closeprice')

        # Deleting model 'SplitOrAdjustmentEvent'
        db.delete_table(u'sdapp_splitoradjustmentevent')

        # Deleting model 'FTPFileList'
        db.delete_table(u'sdapp_ftpfilelist')

        # Deleting model 'FullForm'
        db.delete_table(u'sdapp_fullform')

        # Deleting model 'Form345Entry'
        db.delete_table(u'sdapp_form345entry')


    models = {
        u'sdapp.affiliation': {
            'Meta': {'object_name': 'Affiliation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"})
        },
        u'sdapp.closeprice': {
            'Meta': {'object_name': 'ClosePrice'},
            'SecurityPriceHist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'}),
            'close_date': ('django.db.models.fields.DateField', [], {}),
            'close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sdapp.form345entry': {
            'Meta': {'object_name': 'Form345Entry'},
            'conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'direct_or_indirect': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'entry_internal_id': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'filedatetime': ('django.db.models.fields.DateTimeField', [], {}),
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
            'issuer_cik_num': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'period_of_report': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'reporting_owner_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']", 'null': 'True'}),
            'reporting_owner_cik_num': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'reporting_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'scrubbed_underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'sec_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'securty': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']", 'null': 'True'}),
            'shares_following_xn': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'short_sec_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'supersededdt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
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
        u'sdapp.ftpfilelist': {
            'Meta': {'object_name': 'FTPFileList'},
            'files': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'sdapp.fullform': {
            'Meta': {'object_name': 'FullForm'},
            'issuer_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'save_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'sec_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'sdapp.issuercik': {
            'Meta': {'object_name': 'IssuerCIK'},
            'cik_num': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'sdapp.reportingperson': {
            'Meta': {'object_name': 'ReportingPerson'},
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'reporting_owner_cik_num': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'sdapp.security': {
            'Meta': {'object_name': 'Security'},
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'})
        },
        u'sdapp.securitypricehist': {
            'Meta': {'object_name': 'SecurityPriceHist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']", 'null': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']", 'null': 'True'}),
            'ticker_sym': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'sdapp.splitoradjustmentevent': {
            'Meta': {'object_name': 'SplitOrAdjustmentEvent'},
            'adjustment_factor': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '4'}),
            'event_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"})
        }
    }

    complete_apps = ['sdapp']