# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Affiliation.share_equivalents_held'
        db.add_column(u'sdapp_affiliation', 'share_equivalents_held',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.average_conversion_price'
        db.add_column(u'sdapp_affiliation', 'average_conversion_price',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.share_equivalents_value'
        db.add_column(u'sdapp_affiliation', 'share_equivalents_value',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.conversion_to_price_ratio'
        db.add_column(u'sdapp_affiliation', 'conversion_to_price_ratio',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.equity_grant_rate'
        db.add_column(u'sdapp_affiliation', 'equity_grant_rate',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.avg_grant_conv_price'
        db.add_column(u'sdapp_affiliation', 'avg_grant_conv_price',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.prior_share_equivalents_held'
        db.add_column(u'sdapp_affiliation', 'prior_share_equivalents_held',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.prior_average_conversion_price'
        db.add_column(u'sdapp_affiliation', 'prior_average_conversion_price',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.prior_share_equivalents_value'
        db.add_column(u'sdapp_affiliation', 'prior_share_equivalents_value',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.prior_conversion_to_price_ratio'
        db.add_column(u'sdapp_affiliation', 'prior_conversion_to_price_ratio',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.recent_xns_shares_disc'
        db.add_column(u'sdapp_affiliation', 'recent_xns_shares_disc',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.recent_xns_value_disc'
        db.add_column(u'sdapp_affiliation', 'recent_xns_value_disc',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.hist_xns_shares_disc'
        db.add_column(u'sdapp_affiliation', 'hist_xns_shares_disc',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.hist_xns_value_disc'
        db.add_column(u'sdapp_affiliation', 'hist_xns_value_disc',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.increase_in_selling_disc'
        db.add_column(u'sdapp_affiliation', 'increase_in_selling_disc',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Affiliation.expected_recent_share_sale_amount_disc'
        db.add_column(u'sdapp_affiliation', 'expected_recent_share_sale_amount_disc',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.xns_date_disc'
        db.add_column(u'sdapp_affiliation', 'xns_date_disc',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.xns_close_price_disc'
        db.add_column(u'sdapp_affiliation', 'xns_close_price_disc',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.price_motivated_sale_detected_disc'
        db.add_column(u'sdapp_affiliation', 'price_motivated_sale_detected_disc',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Affiliation.xns_prior_performance_disc'
        db.add_column(u'sdapp_affiliation', 'xns_prior_performance_disc',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.xns_subs_performance_disc'
        db.add_column(u'sdapp_affiliation', 'xns_subs_performance_disc',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.xn_days_disc'
        db.add_column(u'sdapp_affiliation', 'xn_days_disc',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.recent_xns_shares_10b5_1'
        db.add_column(u'sdapp_affiliation', 'recent_xns_shares_10b5_1',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.recent_xns_value_10b5_1'
        db.add_column(u'sdapp_affiliation', 'recent_xns_value_10b5_1',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.hist_xns_shares_10b5_1'
        db.add_column(u'sdapp_affiliation', 'hist_xns_shares_10b5_1',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.hist_xns_value_10b5_1'
        db.add_column(u'sdapp_affiliation', 'hist_xns_value_10b5_1',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.increase_in_selling_10b5_1'
        db.add_column(u'sdapp_affiliation', 'increase_in_selling_10b5_1',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Affiliation.expected_recent_share_sale_amount_10b5_1'
        db.add_column(u'sdapp_affiliation', 'expected_recent_share_sale_amount_10b5_1',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.selling_date_10b5_1'
        db.add_column(u'sdapp_affiliation', 'selling_date_10b5_1',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.selling_close_price_10b5_1'
        db.add_column(u'sdapp_affiliation', 'selling_close_price_10b5_1',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=2),
                      keep_default=False)

        # Adding field 'Affiliation.price_trigger_detected_10b5_1'
        db.add_column(u'sdapp_affiliation', 'price_trigger_detected_10b5_1',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Affiliation.selling_prior_performance_10b5_1'
        db.add_column(u'sdapp_affiliation', 'selling_prior_performance_10b5_1',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.selling_subs_performance_10b5_1'
        db.add_column(u'sdapp_affiliation', 'selling_subs_performance_10b5_1',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.xn_days_10b5_1'
        db.add_column(u'sdapp_affiliation', 'xn_days_10b5_1',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.quarters_with_disc_sales_in_tracking_period'
        db.add_column(u'sdapp_affiliation', 'quarters_with_disc_sales_in_tracking_period',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.quarter_count_3_mo_decline'
        db.add_column(u'sdapp_affiliation', 'quarter_count_3_mo_decline',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.quarter_count_6_mo_decline'
        db.add_column(u'sdapp_affiliation', 'quarter_count_6_mo_decline',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.quarter_count_9_mo_decline'
        db.add_column(u'sdapp_affiliation', 'quarter_count_9_mo_decline',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.quarter_count_12_mo_decline'
        db.add_column(u'sdapp_affiliation', 'quarter_count_12_mo_decline',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.post_sale_perf_3mo'
        db.add_column(u'sdapp_affiliation', 'post_sale_perf_3mo',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.post_sale_perf_6mo'
        db.add_column(u'sdapp_affiliation', 'post_sale_perf_6mo',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.post_sale_perf_9mo'
        db.add_column(u'sdapp_affiliation', 'post_sale_perf_9mo',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.post_sale_perf_12mo'
        db.add_column(u'sdapp_affiliation', 'post_sale_perf_12mo',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.quarters_with_10b_sales_in_tracking_period'
        db.add_column(u'sdapp_affiliation', 'quarters_with_10b_sales_in_tracking_period',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.quarter_count_3_mo_decline_10b'
        db.add_column(u'sdapp_affiliation', 'quarter_count_3_mo_decline_10b',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.quarter_count_6_mo_decline_10b'
        db.add_column(u'sdapp_affiliation', 'quarter_count_6_mo_decline_10b',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.quarter_count_9_mo_decline_10b'
        db.add_column(u'sdapp_affiliation', 'quarter_count_9_mo_decline_10b',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.quarter_count_12_mo_decline_10b'
        db.add_column(u'sdapp_affiliation', 'quarter_count_12_mo_decline_10b',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.post_sale_perf_10b_3mo'
        db.add_column(u'sdapp_affiliation', 'post_sale_perf_10b_3mo',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.post_sale_perf_10b_6mo'
        db.add_column(u'sdapp_affiliation', 'post_sale_perf_10b_6mo',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.post_sale_perf_10b_9mo'
        db.add_column(u'sdapp_affiliation', 'post_sale_perf_10b_9mo',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.post_sale_perf_10b_12mo'
        db.add_column(u'sdapp_affiliation', 'post_sale_perf_10b_12mo',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.annualized_perf_in_tracking_period'
        db.add_column(u'sdapp_affiliation', 'annualized_perf_in_tracking_period',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4),
                      keep_default=False)

        # Adding field 'Affiliation.first_form_dt'
        db.add_column(u'sdapp_affiliation', 'first_form_dt',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.latest_form_dt'
        db.add_column(u'sdapp_affiliation', 'latest_form_dt',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.is_active'
        db.add_column(u'sdapp_affiliation', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Affiliation.behavior'
        db.add_column(u'sdapp_affiliation', 'behavior',
                      self.gf('django.db.models.fields.CharField')(max_length=15, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Affiliation.share_equivalents_held'
        db.delete_column(u'sdapp_affiliation', 'share_equivalents_held')

        # Deleting field 'Affiliation.average_conversion_price'
        db.delete_column(u'sdapp_affiliation', 'average_conversion_price')

        # Deleting field 'Affiliation.share_equivalents_value'
        db.delete_column(u'sdapp_affiliation', 'share_equivalents_value')

        # Deleting field 'Affiliation.conversion_to_price_ratio'
        db.delete_column(u'sdapp_affiliation', 'conversion_to_price_ratio')

        # Deleting field 'Affiliation.equity_grant_rate'
        db.delete_column(u'sdapp_affiliation', 'equity_grant_rate')

        # Deleting field 'Affiliation.avg_grant_conv_price'
        db.delete_column(u'sdapp_affiliation', 'avg_grant_conv_price')

        # Deleting field 'Affiliation.prior_share_equivalents_held'
        db.delete_column(u'sdapp_affiliation', 'prior_share_equivalents_held')

        # Deleting field 'Affiliation.prior_average_conversion_price'
        db.delete_column(u'sdapp_affiliation', 'prior_average_conversion_price')

        # Deleting field 'Affiliation.prior_share_equivalents_value'
        db.delete_column(u'sdapp_affiliation', 'prior_share_equivalents_value')

        # Deleting field 'Affiliation.prior_conversion_to_price_ratio'
        db.delete_column(u'sdapp_affiliation', 'prior_conversion_to_price_ratio')

        # Deleting field 'Affiliation.recent_xns_shares_disc'
        db.delete_column(u'sdapp_affiliation', 'recent_xns_shares_disc')

        # Deleting field 'Affiliation.recent_xns_value_disc'
        db.delete_column(u'sdapp_affiliation', 'recent_xns_value_disc')

        # Deleting field 'Affiliation.hist_xns_shares_disc'
        db.delete_column(u'sdapp_affiliation', 'hist_xns_shares_disc')

        # Deleting field 'Affiliation.hist_xns_value_disc'
        db.delete_column(u'sdapp_affiliation', 'hist_xns_value_disc')

        # Deleting field 'Affiliation.increase_in_selling_disc'
        db.delete_column(u'sdapp_affiliation', 'increase_in_selling_disc')

        # Deleting field 'Affiliation.expected_recent_share_sale_amount_disc'
        db.delete_column(u'sdapp_affiliation', 'expected_recent_share_sale_amount_disc')

        # Deleting field 'Affiliation.xns_date_disc'
        db.delete_column(u'sdapp_affiliation', 'xns_date_disc')

        # Deleting field 'Affiliation.xns_close_price_disc'
        db.delete_column(u'sdapp_affiliation', 'xns_close_price_disc')

        # Deleting field 'Affiliation.price_motivated_sale_detected_disc'
        db.delete_column(u'sdapp_affiliation', 'price_motivated_sale_detected_disc')

        # Deleting field 'Affiliation.xns_prior_performance_disc'
        db.delete_column(u'sdapp_affiliation', 'xns_prior_performance_disc')

        # Deleting field 'Affiliation.xns_subs_performance_disc'
        db.delete_column(u'sdapp_affiliation', 'xns_subs_performance_disc')

        # Deleting field 'Affiliation.xn_days_disc'
        db.delete_column(u'sdapp_affiliation', 'xn_days_disc')

        # Deleting field 'Affiliation.recent_xns_shares_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'recent_xns_shares_10b5_1')

        # Deleting field 'Affiliation.recent_xns_value_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'recent_xns_value_10b5_1')

        # Deleting field 'Affiliation.hist_xns_shares_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'hist_xns_shares_10b5_1')

        # Deleting field 'Affiliation.hist_xns_value_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'hist_xns_value_10b5_1')

        # Deleting field 'Affiliation.increase_in_selling_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'increase_in_selling_10b5_1')

        # Deleting field 'Affiliation.expected_recent_share_sale_amount_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'expected_recent_share_sale_amount_10b5_1')

        # Deleting field 'Affiliation.selling_date_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'selling_date_10b5_1')

        # Deleting field 'Affiliation.selling_close_price_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'selling_close_price_10b5_1')

        # Deleting field 'Affiliation.price_trigger_detected_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'price_trigger_detected_10b5_1')

        # Deleting field 'Affiliation.selling_prior_performance_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'selling_prior_performance_10b5_1')

        # Deleting field 'Affiliation.selling_subs_performance_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'selling_subs_performance_10b5_1')

        # Deleting field 'Affiliation.xn_days_10b5_1'
        db.delete_column(u'sdapp_affiliation', 'xn_days_10b5_1')

        # Deleting field 'Affiliation.quarters_with_disc_sales_in_tracking_period'
        db.delete_column(u'sdapp_affiliation', 'quarters_with_disc_sales_in_tracking_period')

        # Deleting field 'Affiliation.quarter_count_3_mo_decline'
        db.delete_column(u'sdapp_affiliation', 'quarter_count_3_mo_decline')

        # Deleting field 'Affiliation.quarter_count_6_mo_decline'
        db.delete_column(u'sdapp_affiliation', 'quarter_count_6_mo_decline')

        # Deleting field 'Affiliation.quarter_count_9_mo_decline'
        db.delete_column(u'sdapp_affiliation', 'quarter_count_9_mo_decline')

        # Deleting field 'Affiliation.quarter_count_12_mo_decline'
        db.delete_column(u'sdapp_affiliation', 'quarter_count_12_mo_decline')

        # Deleting field 'Affiliation.post_sale_perf_3mo'
        db.delete_column(u'sdapp_affiliation', 'post_sale_perf_3mo')

        # Deleting field 'Affiliation.post_sale_perf_6mo'
        db.delete_column(u'sdapp_affiliation', 'post_sale_perf_6mo')

        # Deleting field 'Affiliation.post_sale_perf_9mo'
        db.delete_column(u'sdapp_affiliation', 'post_sale_perf_9mo')

        # Deleting field 'Affiliation.post_sale_perf_12mo'
        db.delete_column(u'sdapp_affiliation', 'post_sale_perf_12mo')

        # Deleting field 'Affiliation.quarters_with_10b_sales_in_tracking_period'
        db.delete_column(u'sdapp_affiliation', 'quarters_with_10b_sales_in_tracking_period')

        # Deleting field 'Affiliation.quarter_count_3_mo_decline_10b'
        db.delete_column(u'sdapp_affiliation', 'quarter_count_3_mo_decline_10b')

        # Deleting field 'Affiliation.quarter_count_6_mo_decline_10b'
        db.delete_column(u'sdapp_affiliation', 'quarter_count_6_mo_decline_10b')

        # Deleting field 'Affiliation.quarter_count_9_mo_decline_10b'
        db.delete_column(u'sdapp_affiliation', 'quarter_count_9_mo_decline_10b')

        # Deleting field 'Affiliation.quarter_count_12_mo_decline_10b'
        db.delete_column(u'sdapp_affiliation', 'quarter_count_12_mo_decline_10b')

        # Deleting field 'Affiliation.post_sale_perf_10b_3mo'
        db.delete_column(u'sdapp_affiliation', 'post_sale_perf_10b_3mo')

        # Deleting field 'Affiliation.post_sale_perf_10b_6mo'
        db.delete_column(u'sdapp_affiliation', 'post_sale_perf_10b_6mo')

        # Deleting field 'Affiliation.post_sale_perf_10b_9mo'
        db.delete_column(u'sdapp_affiliation', 'post_sale_perf_10b_9mo')

        # Deleting field 'Affiliation.post_sale_perf_10b_12mo'
        db.delete_column(u'sdapp_affiliation', 'post_sale_perf_10b_12mo')

        # Deleting field 'Affiliation.annualized_perf_in_tracking_period'
        db.delete_column(u'sdapp_affiliation', 'annualized_perf_in_tracking_period')

        # Deleting field 'Affiliation.first_form_dt'
        db.delete_column(u'sdapp_affiliation', 'first_form_dt')

        # Deleting field 'Affiliation.latest_form_dt'
        db.delete_column(u'sdapp_affiliation', 'latest_form_dt')

        # Deleting field 'Affiliation.is_active'
        db.delete_column(u'sdapp_affiliation', 'is_active')

        # Deleting field 'Affiliation.behavior'
        db.delete_column(u'sdapp_affiliation', 'behavior')


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
            'post_sale_perf_10b_12mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_10b_3mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_10b_6mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_10b_9mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_12mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_3mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_6mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'post_sale_perf_9mo': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'price_motivated_sale_detected_disc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'price_trigger_detected_10b5_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prior_average_conversion_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_conversion_to_price_ratio': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_share_equivalents_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'prior_share_equivalents_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'quarter_count_12_mo_decline': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quarter_count_12_mo_decline_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quarter_count_3_mo_decline': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quarter_count_3_mo_decline_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quarter_count_6_mo_decline': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quarter_count_6_mo_decline_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quarter_count_9_mo_decline': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quarter_count_9_mo_decline_10b': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quarters_with_10b_sales_in_tracking_period': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'quarters_with_disc_sales_in_tracking_period': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'recent_xns_shares_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'recent_xns_shares_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'recent_xns_value_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'recent_xns_value_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'reporting_owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']"}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'selling_close_price_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'selling_date_10b5_1': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'selling_prior_performance_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'selling_subs_performance_10b5_1': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
            'share_equivalents_held': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'share_equivalents_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'xn_days_10b5_1': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'xn_days_disc': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'xns_close_price_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'xns_date_disc': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'xns_prior_performance_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'xns_subs_performance_disc': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'})
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
            'saleofall': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sec_price_hist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.SecurityPriceHist']", 'null': 'True'}),
            'sellers': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'sellonstrength': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signal_is_new': ('django.db.models.fields.BooleanField', [], {}),
            'soa_biggest_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
            'soa_detect_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'soa_end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'soa_inc_ceo': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'soa_people_count': ('django.db.models.fields.IntegerField', [], {'max_length': '15', 'null': 'True'}),
            'soa_primary_affiliation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Affiliation']", 'null': 'True'}),
            'soa_start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'soa_total_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '2'}),
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