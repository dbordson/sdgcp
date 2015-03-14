# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TransactionEvent'
        db.create_table(u'sdapp_transactionevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('net_xn_val', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('end_holding_val', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('net_xn_pct', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('period_start', self.gf('django.db.models.fields.DateField')(null=True)),
            ('period_end', self.gf('django.db.models.fields.DateField')(null=True)),
            ('price_at_period_end', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('price_at_91_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('price_at_182_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('price_at_274_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('price_at_365_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('price_at_456_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
        ))
        db.send_create_signal(u'sdapp', ['TransactionEvent'])


    def backwards(self, orm):
        # Deleting model 'TransactionEvent'
        db.delete_table(u'sdapp_transactionevent')


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
            'adj_close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'close_date': ('django.db.models.fields.DateField', [], {}),
            'close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'securitypricehist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'})
        },
        u'sdapp.form345entry': {
            'Meta': {'object_name': 'Form345Entry'},
            'adjustment_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'adjustment_factor': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '15', 'decimal_places': '4'}),
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Affiliation']", 'null': 'True'}),
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
            'issuer_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'period_of_report': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'reported_shares_following_xn': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'reporting_owner_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']", 'null': 'True'}),
            'reporting_owner_cik_num': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'reporting_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'scrubbed_underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'sec_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'security_relationship'", 'null': 'True', 'to': u"orm['sdapp.Security']"}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'shares_following_xn': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'shares_following_xn_is_adjusted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_sec_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'supersededdt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'tenbfive_note': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transaction_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'transaction_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'transaction_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'transaction_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_security': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'underlying_relationship'", 'null': 'True', 'to': u"orm['sdapp.Security']"}),
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
        u'sdapp.personholdingview': {
            'Meta': {'object_name': 'PersonHoldingView'},
            'affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Affiliation']"}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'first_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intrinsic_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_close_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'last_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'max_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'min_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'most_recent_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'person_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'scrubbed_underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"}),
            'short_sec_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'underlying_close_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_shares_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'units_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_conversion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'wavg_xn_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        u'sdapp.reportingperson': {
            'Meta': {'object_name': 'ReportingPerson'},
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'reporting_owner_cik_num': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        },
        u'sdapp.security': {
            'Meta': {'object_name': 'Security'},
            'conversion_multiple': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '15', 'decimal_places': '4'}),
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'scrubbed_underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'short_sec_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        u'sdapp.securitypricehist': {
            'Meta': {'object_name': 'SecurityPriceHist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']", 'null': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']", 'null': 'True'}),
            'ticker_sym': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'sdapp.securityview': {
            'Meta': {'object_name': 'SecurityView'},
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'first_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intrinsic_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_close_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'last_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'max_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'min_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'most_recent_xn': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'scrubbed_underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"}),
            'short_sec_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'underlying_close_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_shares_total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'underlying_ticker': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'units_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_conversion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'wavg_expiration_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'wavg_xn_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        u'sdapp.splitoradjustmentevent': {
            'Meta': {'object_name': 'SplitOrAdjustmentEvent'},
            'adjustment_factor': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '4'}),
            'event_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"})
        },
        u'sdapp.transactionevent': {
            'Meta': {'object_name': 'TransactionEvent'},
            'end_holding_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'net_xn_pct': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'net_xn_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'period_end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'period_start': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'price_at_182_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'price_at_274_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'price_at_365_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'price_at_456_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'price_at_91_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'price_at_period_end': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'})
        }
    }

    complete_apps = ['sdapp']