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
            ('issuer_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('reporting_owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            ('person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('is_director', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_officer', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_ten_percent', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('is_something_else', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('reporting_owner_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('share_equivalents_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('average_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('share_equivalents_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('conversion_to_price_ratio', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('equity_grant_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('avg_grant_conv_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('prior_share_equivalents_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('prior_average_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('prior_share_equivalents_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('prior_conversion_to_price_ratio', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('recent_xns_shares_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('recent_xns_value_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('hist_xns_shares_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('hist_xns_value_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('increase_in_selling_disc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('expected_recent_share_sale_amount_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('selling_date_disc', self.gf('django.db.models.fields.DateField')(null=True)),
            ('selling_close_price_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('price_motivated_sale_detected_disc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('selling_prior_performance_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('selling_subs_performance_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('increase_in_buying_disc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('buying_date_disc', self.gf('django.db.models.fields.DateField')(null=True)),
            ('buying_close_price_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('price_motivated_buy_detected_disc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('buying_prior_performance_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('buying_subs_performance_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('xn_days_disc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('recent_xns_shares_10b5_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('recent_xns_value_10b5_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('hist_xns_shares_10b5_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('hist_xns_value_10b5_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('increase_in_selling_10b5_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('expected_recent_share_sale_amount_10b5_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('selling_date_10b5_1', self.gf('django.db.models.fields.DateField')(null=True)),
            ('selling_close_price_10b5_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('price_trigger_detected_10b5_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('selling_prior_performance_10b5_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('selling_subs_performance_10b5_1', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('xn_days_10b5_1', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('qtrs_with_disc_sales_in_tracking_period', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_3_mo_decline_disc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_3_mo_measured_disc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_6_mo_decline_disc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_6_mo_measured_disc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_9_mo_decline_disc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_9_mo_measured_disc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_12_mo_decline_disc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_12_mo_measured_disc', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('post_sale_perf_3mo_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('post_sale_perf_6mo_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('post_sale_perf_9mo_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('post_sale_perf_12mo_disc', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('qtrs_with_buys_in_tracking_period', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('buy_qtr_ct_3_mo_increase', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('buy_qtr_ct_3_mo_measured', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('buy_qtr_ct_6_mo_increase', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('buy_qtr_ct_6_mo_measured', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('buy_qtr_ct_9_mo_increase', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('buy_qtr_ct_9_mo_measured', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('buy_qtr_ct_12_mo_increase', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('buy_qtr_ct_12_mo_measured', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('post_buy_perf_3mo', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('post_buy_perf_6mo', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('post_buy_perf_9mo', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('post_buy_perf_12mo', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('qtrs_with_10b_sales_in_tracking_period', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_3_mo_decline_10b', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_3_mo_measured_10b', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_6_mo_decline_10b', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_6_mo_measured_10b', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_9_mo_decline_10b', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_9_mo_measured_10b', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_12_mo_decline_10b', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('sale_qtr_ct_12_mo_measured_10b', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('post_sale_perf_3mo_10b', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('post_sale_perf_6mo_10b', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('post_sale_perf_9mo_10b', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('post_sale_perf_12mo_10b', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('annualized_perf_in_tracking_period', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('first_form_dt', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('latest_form_dt', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('behavior', self.gf('django.db.models.fields.CharField')(max_length=15, null=True)),
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
            ('event_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(1900, 1, 1, 0, 0))),
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
            ('prim_security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'], null=True)),
            ('xn_prim_share_eq', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('xn_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('xn_full_conv_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('prim_adjustment_factor', self.gf('django.db.models.fields.DecimalField')(default='1.00', max_digits=15, decimal_places=4)),
            ('prim_adjustment_date', self.gf('django.db.models.fields.DateField')(null=True)),
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
            ('buyonweakness', self.gf('django.db.models.fields.BooleanField')(default=False)),
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
            ('clusterbuy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cb_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cb_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cb_plural_insiders', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('cb_buy_xns', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True)),
            ('cb_net_xn_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('discretionarybuy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('db_large_xn_size', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('db_was_ceo', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('db_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('db_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('db_detect_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('db_person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('db_xn_val', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('db_security_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('db_xn_pct_holdings', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('sellonstrength', self.gf('django.db.models.fields.BooleanField')(default=False)),
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
            ('clustersell', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cs_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cs_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('cs_plural_insiders', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('cs_sell_xns', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True)),
            ('cs_net_xn_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('cs_annual_grant_rate', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('cs_net_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('discretionarysell', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ds_large_xn_size', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ds_was_ceo', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('ds_start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('ds_end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('ds_detect_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('ds_person_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('ds_xn_val', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('ds_security_name', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('ds_xn_pct_holdings', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('total_transactions', self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True)),
            ('active_insiders', self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True)),
            ('sellers', self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True)),
            ('insiders_reduced_holdings', self.gf('django.db.models.fields.IntegerField')(max_length=15, null=True)),
            ('average_holding_reduction', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('number_of_recent_shares_sold', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('value_of_recent_shares_sold', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('historical_selling_rate_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('historical_selling_rate_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('percent_change_in_shares_historical_to_recent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('percent_change_in_value_historical_to_recent', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('percent_options_converted_to_expire_in_current_year', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('percent_recent_shares_sold_under_10b5_1_plans', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('recent_share_sell_rate_for_10b5_1_plans', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
            ('historical_share_sell_rate_for_10b5_1_plans', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2)),
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
            'annualized_perf_in_tracking_period': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'average_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'avg_grant_conv_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'behavior': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'buy_qtr_ct_12_mo_increase': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'buy_qtr_ct_12_mo_measured': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'buy_qtr_ct_3_mo_increase': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'buy_qtr_ct_3_mo_measured': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'buy_qtr_ct_6_mo_increase': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'buy_qtr_ct_6_mo_measured': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'buy_qtr_ct_9_mo_increase': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'buy_qtr_ct_9_mo_measured': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'buying_close_price_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'buying_date_disc': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'buying_prior_performance_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'buying_subs_performance_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'conversion_to_price_ratio': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'equity_grant_rate': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'expected_recent_share_sale_amount_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'expected_recent_share_sale_amount_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'first_form_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'hist_xns_shares_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'hist_xns_shares_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'hist_xns_value_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'hist_xns_value_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'increase_in_buying_disc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'increase_in_selling_10b5_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'increase_in_selling_disc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_director': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_officer': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_something_else': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_ten_percent': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'issuer_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'latest_form_dt': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'post_buy_perf_12mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_buy_perf_3mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_buy_perf_6mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_buy_perf_9mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_12mo_10b': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_12mo_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_3mo_10b': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_3mo_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_6mo_10b': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_6mo_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_9mo_10b': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_9mo_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'price_motivated_buy_detected_disc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_motivated_sale_detected_disc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_trigger_detected_10b5_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prior_average_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_conversion_to_price_ratio': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_share_equivalents_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_share_equivalents_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'qtrs_with_10b_sales_in_tracking_period': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'qtrs_with_buys_in_tracking_period': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'qtrs_with_disc_sales_in_tracking_period': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'recent_xns_shares_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'recent_xns_shares_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'recent_xns_value_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'recent_xns_value_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'reporting_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'sale_qtr_ct_12_mo_decline_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_12_mo_decline_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_12_mo_measured_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_12_mo_measured_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_3_mo_decline_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_3_mo_decline_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_3_mo_measured_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_3_mo_measured_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_6_mo_decline_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_6_mo_decline_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_6_mo_measured_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_6_mo_measured_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_9_mo_decline_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_9_mo_decline_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_9_mo_measured_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sale_qtr_ct_9_mo_measured_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'selling_close_price_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'selling_close_price_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'selling_date_10b5_1': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'selling_date_disc': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'selling_prior_performance_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'selling_prior_performance_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'selling_subs_performance_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'selling_subs_performance_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'share_equivalents_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'share_equivalents_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'xn_days_10b5_1': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'xn_days_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
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
            'prim_adjustment_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'prim_adjustment_factor': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '15', 'decimal_places': '4'}),
            'prim_security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']", 'null': 'True'}),
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
            'xn_full_conv_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'xn_price_per_share': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'xn_prim_share_eq': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'xn_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'})
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
        u'sdapp.sigdisplay': {
            'Meta': {'object_name': 'SigDisplay'},
            'active_insiders': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'average_holding_reduction': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
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
            'buyonweakness': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cb_buy_xns': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'cb_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'cb_net_xn_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'cb_plural_insiders': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'cb_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'clusterbuy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clustersell': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'discretionarybuy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'discretionarysell': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ds_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ds_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ds_large_xn_size': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ds_person_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ds_security_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'ds_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'ds_was_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'ds_xn_pct_holdings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'ds_xn_val': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'historical_selling_rate_shares': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'historical_selling_rate_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'historical_share_sell_rate_for_10b5_1_plans': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insiders_reduced_holdings': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'last_signal': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'number_of_recent_shares_sold': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'percent_change_in_shares_historical_to_recent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'percent_change_in_value_historical_to_recent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'percent_options_converted_to_expire_in_current_year': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'percent_recent_shares_sold_under_10b5_1_plans': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'recent_share_sell_rate_for_10b5_1_plans': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'sec_price_hist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'}),
            'sellers': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'sellonstrength': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
            'total_transactions': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'value_of_recent_shares_sold': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'})
        },
        u'sdapp.splitoradjustmentevent': {
            'Meta': {'object_name': 'SplitOrAdjustmentEvent'},
            'adjustment_factor': ('django.db.models.fields.DecimalField', [], {'max_digits': '15', 'decimal_places': '4'}),
            'event_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(1900, 1, 1, 0, 0)'}),
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