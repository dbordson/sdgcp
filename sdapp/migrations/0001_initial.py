# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ReportingPerson'
        db.create_table(u'sdapp_reportingperson', (
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('reporting_owner_cik_num', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal(u'sdapp', ['ReportingPerson'])

        # Adding model 'IssuerCIK'
        db.create_table(u'sdapp_issuercik', (
            ('cik_num', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
        ))
        db.send_create_signal(u'sdapp', ['IssuerCIK'])

        # Adding model 'Affiliation'
        db.create_table(u'sdapp_affiliation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('reporting_owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('is_director', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_officer', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_ten_percent', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_something_else', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('reporting_owner_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('share_equivalents_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('average_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('equity_grant_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('share_equivalents_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('conversion_to_price_ratio', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('equity_grant_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('share_equivalents_value_percentile', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('average_conversion_price_ratio_percentile', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('equity_grant_value_percentile', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('latest_form_dt', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'sdapp', ['Affiliation'])

        # Adding model 'Security'
        db.create_table(u'sdapp_security', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('short_sec_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('ticker', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('scrubbed_underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('conversion_multiple', self.gf('django.db.models.fields.DecimalField')(default='1.00', max_digits=15, decimal_places=4)),
        ))
        db.send_create_signal(u'sdapp', ['Security'])

        # Adding model 'SecurityPriceHist'
        db.create_table(u'sdapp_securitypricehist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticker_sym', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('primary_ticker_sym', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'], null=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'], null=True)),
        ))
        db.send_create_signal(u'sdapp', ['SecurityPriceHist'])

        # Adding model 'ClosePrice'
        db.create_table(u'sdapp_closeprice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('close_price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('adj_close_price', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=4)),
            ('close_date', self.gf('django.db.models.fields.DateField')()),
            ('securitypricehist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.SecurityPriceHist'], null=True)),
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

        # Adding model 'TransactionEvent'
        db.create_table(u'sdapp_transactionevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('net_xn_val', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('end_holding_val', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('net_xn_pct', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('period_start', self.gf('django.db.models.fields.DateField')(null=True)),
            ('period_end', self.gf('django.db.models.fields.DateField')(null=True)),
            ('price_at_period_end', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('perf_at_91_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('perf_at_182_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('perf_at_274_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('perf_at_365_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('perf_at_456_days', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
        ))
        db.send_create_signal(u'sdapp', ['TransactionEvent'])

        # Adding model 'WatchedName'
        db.create_table(u'sdapp_watchedname', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('securitypricehist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.SecurityPriceHist'])),
            ('ticker_sym', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('last_signal_sent', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'sdapp', ['WatchedName'])

        # Adding model 'ReportingPersonAtts'
        db.create_table(u'sdapp_reportingpersonatts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reporting_person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('transactions', self.gf('django.db.models.fields.IntegerField')()),
            ('buys', self.gf('django.db.models.fields.IntegerField')()),
            ('sells', self.gf('django.db.models.fields.IntegerField')()),
            ('activity_threshold', self.gf('django.db.models.fields.BooleanField')()),
            ('t_win_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=4)),
            ('b_win_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=4)),
            ('s_win_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=4)),
            ('exec_years', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=4)),
            ('t_perf', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('s_perf', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_10', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_30', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_60', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_90', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_120', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_150', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
        ))
        db.send_create_signal(u'sdapp', ['ReportingPersonAtts'])

        # Adding model 'YearlyReportingPersonAtts'
        db.create_table(u'sdapp_yearlyreportingpersonatts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reporting_person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('buys', self.gf('django.db.models.fields.IntegerField')()),
            ('b_win_rate_180', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=4)),
            ('exec_years', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=4)),
            ('b_perf_10', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_30', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_60', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_90', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_120', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_150', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('b_perf_180', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
        ))
        db.send_create_signal(u'sdapp', ['YearlyReportingPersonAtts'])

        # Adding model 'SecurityView'
        db.create_table(u'sdapp_securityview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'])),
            ('short_sec_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('ticker', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('last_close_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('units_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('first_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('last_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('wavg_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('min_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('max_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('wavg_conversion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('scrubbed_underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('underlying_ticker', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('underlying_shares_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('underlying_close_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('intrinsic_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=4)),
            ('first_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('most_recent_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('wavg_xn_date', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'sdapp', ['SecurityView'])

        # Adding model 'PersonHoldingView'
        db.create_table(u'sdapp_personholdingview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('person_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'])),
            ('affiliation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Affiliation'])),
            ('short_sec_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('ticker', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('last_close_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('units_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('first_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('last_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('wavg_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('min_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('max_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('wavg_conversion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('scrubbed_underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('underlying_ticker', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('underlying_shares_total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('underlying_close_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('intrinsic_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=16, decimal_places=4)),
            ('first_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('most_recent_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('wavg_xn_date', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'sdapp', ['PersonHoldingView'])

        # Adding model 'FTPFileList'
        db.create_table(u'sdapp_ftpfilelist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('files', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'sdapp', ['FTPFileList'])

        # Adding model 'SECDayIndex'
        db.create_table(u'sdapp_secdayindex', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('indexname', self.gf('django.db.models.fields.TextField')()),
            ('indexcontents', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'sdapp', ['SECDayIndex'])

        # Adding model 'FullForm'
        db.create_table(u'sdapp_fullform', (
            ('sec_path', self.gf('django.db.models.fields.CharField')(max_length=150, primary_key=True)),
            ('save_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('issuer_cik_num', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('parsable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'sdapp', ['FullForm'])

        # Adding model 'Form345Entry'
        db.create_table(u'sdapp_form345entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry_internal_id', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('period_of_report', self.gf('django.db.models.fields.DateField')(null=True)),
            ('issuer_cik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'], null=True)),
            ('issuer_cik_num', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('issuer_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(related_name='security_relationship', null=True, to=orm['sdapp.Security'])),
            ('reporting_owner_cik', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'], null=True)),
            ('reporting_owner_cik_num', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
            ('reporting_owner_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('affiliation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Affiliation'], null=True)),
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
            ('reported_shares_following_xn', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('shares_following_xn_is_adjusted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('direct_or_indirect', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('tenbfive_note', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('transaction_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sec_path', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('sec_url', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('five_not_subject_to_section_sixteen', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('five_form_three_holdings', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('five_form_four_transactions', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('form_type', self.gf('django.db.models.fields.CharField')(max_length=5, null=True)),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('filedatetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('supersededdt', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('adjustment_factor', self.gf('django.db.models.fields.DecimalField')(default='1.00', max_digits=15, decimal_places=4)),
            ('adjustment_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('underlying_security', self.gf('django.db.models.fields.related.ForeignKey')(related_name='underlying_relationship', null=True, to=orm['sdapp.Security'])),
        ))
        db.send_create_signal(u'sdapp', ['Form345Entry'])

        # Adding model 'DiscretionaryXnEvent'
        db.create_table(u'sdapp_discretionaryxnevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('reporting_person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('person_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'])),
            ('form_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Form345Entry'], null=True)),
            ('xn_acq_disp_code', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('transaction_code', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('xn_val', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('xn_shares', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('filedate', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'sdapp', ['DiscretionaryXnEvent'])

        # Adding model 'PersonSignal'
        db.create_table(u'sdapp_personsignal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('sec_price_hist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.SecurityPriceHist'], null=True)),
            ('reporting_person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('eq_annual_share_grants', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('security_1', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'])),
            ('only_security_1', self.gf('django.db.models.fields.BooleanField')()),
            ('reporting_person_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('signal_name', self.gf('django.db.models.fields.CharField')(default='ERROR', max_length=80)),
            ('signal_detect_date', self.gf('django.db.models.fields.DateField')()),
            ('first_file_date', self.gf('django.db.models.fields.DateField')()),
            ('last_file_date', self.gf('django.db.models.fields.DateField')()),
            ('transactions', self.gf('django.db.models.fields.IntegerField')(max_length=15)),
            ('average_price_sec_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('gross_signal_value', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('net_signal_value', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('net_signal_shares', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=2)),
            ('prior_holding_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('net_signal_pct', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('preceding_stock_perf', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('perf_period_days', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('perf_after_detection', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('subs_stock_period_days', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('significant', self.gf('django.db.models.fields.BooleanField')()),
            ('new', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'sdapp', ['PersonSignal'])

        # Adding model 'SigDisplay'
        db.create_table(u'sdapp_sigdisplay', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('sec_price_hist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.SecurityPriceHist'], null=True)),
            ('last_signal', self.gf('django.db.models.fields.DateField')(null=True)),
            ('buy_on_weakness', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('bow_plural_insiders', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('bow_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('bow_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('bow_first_sig_detect_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('bow_person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('bow_includes_ceo', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('bow_net_signal_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('bow_first_perf_period_days', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True)),
            ('bow_first_pre_stock_perf', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('bow_first_post_stock_perf', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('cluster_buy', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('cb_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cb_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cb_plural_insiders', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('cb_buy_xns', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True)),
            ('cb_net_xn_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('discretionary_buy', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('db_large_xn_size', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('db_was_ceo', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('db_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('db_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('db_detect_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('db_person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('db_xn_val', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('db_security_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('db_xn_pct_holdings', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('sell_on_strength', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('sos_plural_insiders', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sos_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('sos_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('sos_first_sig_detect_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('sos_person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('sos_includes_ceo', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('sos_net_signal_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('sos_first_perf_period_days', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True)),
            ('sos_first_pre_stock_perf', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('sos_first_post_stock_perf', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('cluster_sell', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('cs_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cs_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cs_plural_insiders', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('cs_sell_xns', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True)),
            ('cs_net_xn_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('cs_annual_grant_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('cs_net_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('discretionary_sell', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('ds_large_xn_size', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ds_was_ceo', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ds_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('ds_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('ds_detect_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('ds_person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('ds_xn_val', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('ds_security_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('ds_xn_pct_holdings', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('total_transactions', self.gf('django.db.models.fields.IntegerField')(max_length=15)),
            ('signal_is_new', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'sdapp', ['SigDisplay'])


    def backwards(self, orm):
        # Deleting model 'ReportingPerson'
        db.delete_table(u'sdapp_reportingperson')

        # Deleting model 'IssuerCIK'
        db.delete_table(u'sdapp_issuercik')

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

        # Deleting model 'TransactionEvent'
        db.delete_table(u'sdapp_transactionevent')

        # Deleting model 'WatchedName'
        db.delete_table(u'sdapp_watchedname')

        # Deleting model 'ReportingPersonAtts'
        db.delete_table(u'sdapp_reportingpersonatts')

        # Deleting model 'YearlyReportingPersonAtts'
        db.delete_table(u'sdapp_yearlyreportingpersonatts')

        # Deleting model 'SecurityView'
        db.delete_table(u'sdapp_securityview')

        # Deleting model 'PersonHoldingView'
        db.delete_table(u'sdapp_personholdingview')

        # Deleting model 'FTPFileList'
        db.delete_table(u'sdapp_ftpfilelist')

        # Deleting model 'SECDayIndex'
        db.delete_table(u'sdapp_secdayindex')

        # Deleting model 'FullForm'
        db.delete_table(u'sdapp_fullform')

        # Deleting model 'Form345Entry'
        db.delete_table(u'sdapp_form345entry')

        # Deleting model 'DiscretionaryXnEvent'
        db.delete_table(u'sdapp_discretionaryxnevent')

        # Deleting model 'PersonSignal'
        db.delete_table(u'sdapp_personsignal')

        # Deleting model 'SigDisplay'
        db.delete_table(u'sdapp_sigdisplay')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sdapp.affiliation': {
            'Meta': {'object_name': 'Affiliation'},
            'average_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'average_conversion_price_ratio_percentile': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'conversion_to_price_ratio': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'equity_grant_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'equity_grant_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'equity_grant_value_percentile': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_director': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_officer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_something_else': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_ten_percent': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'latest_form_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'share_equivalents_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'share_equivalents_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'share_equivalents_value_percentile': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'})
        },
        u'sdapp.closeprice': {
            'Meta': {'object_name': 'ClosePrice'},
            'adj_close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            'close_date': ('django.db.models.fields.DateField', [], {}),
            'close_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '4'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'securitypricehist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'})
        },
        u'sdapp.discretionaryxnevent': {
            'Meta': {'object_name': 'DiscretionaryXnEvent'},
            'filedate': ('django.db.models.fields.DateField', [], {}),
            'form_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Form345Entry']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'person_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"}),
            'transaction_code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'xn_acq_disp_code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'xn_shares': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'xn_val': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'})
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
            'sec_url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'sdapp.fullform': {
            'Meta': {'object_name': 'FullForm'},
            'issuer_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'parsable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'save_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'sec_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'sdapp.issuercik': {
            'Meta': {'object_name': 'IssuerCIK'},
            'cik_num': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'})
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
        u'sdapp.personsignal': {
            'Meta': {'object_name': 'PersonSignal'},
            'average_price_sec_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'eq_annual_share_grants': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'first_file_date': ('django.db.models.fields.DateField', [], {}),
            'gross_signal_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_file_date': ('django.db.models.fields.DateField', [], {}),
            'net_signal_pct': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'net_signal_shares': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'net_signal_value': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '2'}),
            'new': ('django.db.models.fields.BooleanField', [], {}),
            'only_security_1': ('django.db.models.fields.BooleanField', [], {}),
            'perf_after_detection': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'perf_period_days': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'preceding_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_holding_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'reporting_person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'reporting_person_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'sec_price_hist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'}),
            'security_1': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']"}),
            'signal_detect_date': ('django.db.models.fields.DateField', [], {}),
            'signal_name': ('django.db.models.fields.CharField', [], {'default': "'ERROR'", 'max_length': '80'}),
            'significant': ('django.db.models.fields.BooleanField', [], {}),
            'subs_stock_period_days': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'transactions': ('django.db.models.fields.IntegerField', [], {'max_length': '15'})
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
        u'sdapp.secdayindex': {
            'Meta': {'object_name': 'SECDayIndex'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indexcontents': ('django.db.models.fields.TextField', [], {}),
            'indexname': ('django.db.models.fields.TextField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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
            'primary_ticker_sym': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
        u'sdapp.sigdisplay': {
            'Meta': {'object_name': 'SigDisplay'},
            'bow_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'bow_first_perf_period_days': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'bow_first_post_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'bow_first_pre_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'bow_first_sig_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'bow_includes_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'bow_net_signal_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'bow_person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'bow_plural_insiders': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'bow_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'buy_on_weakness': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'cb_buy_xns': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'cb_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'cb_net_xn_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'cb_plural_insiders': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'cb_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'cluster_buy': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'cluster_sell': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'cs_annual_grant_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'cs_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'cs_net_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'cs_net_xn_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'cs_plural_insiders': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'cs_sell_xns': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'cs_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'db_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'db_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'db_large_xn_size': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'db_person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'db_security_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'db_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'db_was_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'db_xn_pct_holdings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'db_xn_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'discretionary_buy': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'discretionary_sell': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'ds_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ds_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ds_large_xn_size': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ds_person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ds_security_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ds_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ds_was_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ds_xn_pct_holdings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'ds_xn_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_signal': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'sec_price_hist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'}),
            'sell_on_strength': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'signal_is_new': ('django.db.models.fields.BooleanField', [], {}),
            'sos_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'sos_first_perf_period_days': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'sos_first_post_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'sos_first_pre_stock_perf': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'sos_first_sig_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'sos_includes_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sos_net_signal_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'sos_person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'sos_plural_insiders': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'sos_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'total_transactions': ('django.db.models.fields.IntegerField', [], {'max_length': '15'})
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
        u'sdapp.watchedname': {
            'Meta': {'object_name': 'WatchedName'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_signal_sent': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'securitypricehist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']"}),
            'ticker_sym': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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