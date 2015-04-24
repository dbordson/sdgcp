# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Signal.statement'
        db.delete_column(u'sdapp_signal', 'statement')

        # Adding field 'Signal.short_statement'
        db.add_column(u'sdapp_signal', 'short_statement',
                      self.gf('django.db.models.fields.CharField')(default='ERROR', max_length=200),
                      keep_default=False)

        # Adding field 'Signal.long_statement'
        db.add_column(u'sdapp_signal', 'long_statement',
                      self.gf('django.db.models.fields.CharField')(default='ERROR', max_length=200),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Signal.statement'
        db.add_column(u'sdapp_signal', 'statement',
                      self.gf('django.db.models.fields.CharField')(default='ERROR', max_length=200),
                      keep_default=False)

        # Deleting field 'Signal.short_statement'
        db.delete_column(u'sdapp_signal', 'short_statement')

        # Deleting field 'Signal.long_statement'
        db.delete_column(u'sdapp_signal', 'long_statement')


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
            'intrinsic_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '4'}),
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
        u'sdapp.reportingpersonatts': {
            'Meta': {'object_name': 'ReportingPersonAtts'},
            'activity_threshold': ('django.db.models.fields.BooleanField', [], {}),
            'b_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_10': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_120': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_150': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_30': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_60': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_90': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_win_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'buys': ('django.db.models.fields.IntegerField', [], {}),
            'exec_years': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reporting_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            's_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            's_win_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'sells': ('django.db.models.fields.IntegerField', [], {}),
            't_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            't_win_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'transactions': ('django.db.models.fields.IntegerField', [], {})
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
            'intrinsic_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '4'}),
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
        u'sdapp.signal': {
            'Meta': {'object_name': 'Signal'},
            'formentrysource': ('django.db.models.fields.CharField', [], {'default': "'ERROR'", 'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'long_statement': ('django.db.models.fields.CharField', [], {'default': "'ERROR'", 'max_length': '200'}),
            'reporting_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'reporting_person_name': ('django.db.models.fields.CharField', [], {'default': "'ERROR'", 'max_length': '80'}),
            'reporting_person_title': ('django.db.models.fields.CharField', [], {'default': "'ERROR'", 'max_length': '80'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"}),
            'security_title': ('django.db.models.fields.CharField', [], {'default': "'ERROR'", 'max_length': '80'}),
            'security_units': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'short_statement': ('django.db.models.fields.CharField', [], {'default': "'ERROR'", 'max_length': '200'}),
            'signal_date': ('django.db.models.fields.DateField', [], {}),
            'signal_name': ('django.db.models.fields.CharField', [], {'default': "'ERROR'", 'max_length': '80'}),
            'signal_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'transactions': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'unit_conversion': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'})
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
            'end_holding_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'net_xn_pct': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'net_xn_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_182_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_274_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_365_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_456_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'perf_at_91_days': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'period_end': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'period_start': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'price_at_period_end': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'})
        },
        u'sdapp.yearlyreportingpersonatts': {
            'Meta': {'object_name': 'YearlyReportingPersonAtts'},
            'b_perf_10': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_120': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_150': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_180': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_30': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_60': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_perf_90': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'b_win_rate_180': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            'buys': ('django.db.models.fields.IntegerField', [], {}),
            'exec_years': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reporting_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['sdapp']