# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'CompanyStockHist'
        db.delete_table(u'sdapp_companystockhist')

        # Deleting model 'Holding'
        db.delete_table(u'sdapp_holding')

        # Deleting model 'HoldingType'
        db.delete_table(u'sdapp_holdingtype')

        # Deleting model 'AggHoldingType'
        db.delete_table(u'sdapp_aggholdingtype')

        # Adding model 'SplitOrAdjustmentEvent'
        db.create_table(u'sdapp_splitoradjustmentevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'])),
            ('adjustment_factor', self.gf('django.db.models.fields.DecimalField')(max_digits=15, decimal_places=4)),
            ('event_date', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'sdapp', ['SplitOrAdjustmentEvent'])

        # Adding model 'Security'
        db.create_table(u'sdapp_security', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('public_price_available', self.gf('django.db.models.fields.BooleanField')()),
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
        ))
        db.send_create_signal(u'sdapp', ['Security'])

        # Adding model 'SecurityPriceHist'
        db.create_table(u'sdapp_securitypricehist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticker_sym', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'], null=True)),
            ('security', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'], null=True)),
        ))
        db.send_create_signal(u'sdapp', ['SecurityPriceHist'])

        # Deleting field 'IssuerCIK.id'
        db.delete_column(u'sdapp_issuercik', u'id')


        # Changing field 'IssuerCIK.cik_num'
        db.alter_column(u'sdapp_issuercik', 'cik_num', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True))
        # Adding unique constraint on 'IssuerCIK', fields ['cik_num']
        db.create_unique(u'sdapp_issuercik', ['cik_num'])

        # Deleting field 'ClosePrice.companystockhist'
        db.delete_column(u'sdapp_closeprice', 'companystockhist_id')

        # Adding field 'ClosePrice.SecurityPriceHist'
        db.add_column(u'sdapp_closeprice', 'SecurityPriceHist',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.SecurityPriceHist'], null=True),
                      keep_default=False)

        # Deleting field 'ReportingPerson.id'
        db.delete_column(u'sdapp_reportingperson', u'id')


        # Changing field 'ReportingPerson.reporting_owner_cik_num'
        db.alter_column(u'sdapp_reportingperson', 'reporting_owner_cik_num', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True))
        # Adding unique constraint on 'ReportingPerson', fields ['reporting_owner_cik_num']
        db.create_unique(u'sdapp_reportingperson', ['reporting_owner_cik_num'])

        # Adding field 'Form345Entry.securty'
        db.add_column(u'sdapp_form345entry', 'securty',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Security'], null=True),
                      keep_default=False)


        # Changing field 'Form345Entry.filedatetime'
        db.alter_column(u'sdapp_form345entry', 'filedatetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 12, 0, 0)))
        # Deleting field 'Affiliation.most_recent_filing'
        db.delete_column(u'sdapp_affiliation', 'most_recent_filing')

        # Deleting field 'Affiliation.is_ten_percent'
        db.delete_column(u'sdapp_affiliation', 'is_ten_percent')

        # Deleting field 'Affiliation.first_filing'
        db.delete_column(u'sdapp_affiliation', 'first_filing')

        # Deleting field 'Affiliation.is_something_else'
        db.delete_column(u'sdapp_affiliation', 'is_something_else')

        # Deleting field 'Affiliation.title'
        db.delete_column(u'sdapp_affiliation', 'title')

        # Deleting field 'Affiliation.is_director'
        db.delete_column(u'sdapp_affiliation', 'is_director')

        # Deleting field 'Affiliation.is_officer'
        db.delete_column(u'sdapp_affiliation', 'is_officer')

        # Deleting field 'Affiliation.issuer_cik_num'
        db.delete_column(u'sdapp_affiliation', 'issuer_cik_num')

        # Deleting field 'Affiliation.reporting_owner_cik_num'
        db.delete_column(u'sdapp_affiliation', 'reporting_owner_cik_num')


    def backwards(self, orm):
        # Removing unique constraint on 'ReportingPerson', fields ['reporting_owner_cik_num']
        db.delete_unique(u'sdapp_reportingperson', ['reporting_owner_cik_num'])

        # Removing unique constraint on 'IssuerCIK', fields ['cik_num']
        db.delete_unique(u'sdapp_issuercik', ['cik_num'])

        # Adding model 'CompanyStockHist'
        db.create_table(u'sdapp_companystockhist', (
            ('ticker_sym', self.gf('django.db.models.fields.CharField')(max_length=5)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'], null=True)),
        ))
        db.send_create_signal(u'sdapp', ['CompanyStockHist'])

        # Adding model 'Holding'
        db.create_table(u'sdapp_holding', (
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('underlying_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('most_recent_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('affiliation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Affiliation'])),
            ('units_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('first_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
        ))
        db.send_create_signal(u'sdapp', ['Holding'])

        # Adding model 'HoldingType'
        db.create_table(u'sdapp_holdingtype', (
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('tranches_included', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('underlying_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('wavg_xn_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('last_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('affiliation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.Affiliation'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.ReportingPerson'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('first_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('transactions_included', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('max_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('intrinsic_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('most_recent_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('underlying_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('units_transacted', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('wavg_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('units_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('first_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('wavg_conversion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('min_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
        ))
        db.send_create_signal(u'sdapp', ['HoldingType'])

        # Adding model 'AggHoldingType'
        db.create_table(u'sdapp_aggholdingtype', (
            ('deriv_or_nonderiv', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('tranches_included', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('underlying_shares', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('security_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
            ('wavg_xn_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('last_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issuer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.IssuerCIK'])),
            ('first_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('transactions_included', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('max_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('intrinsic_value', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('most_recent_xn', self.gf('django.db.models.fields.DateField')(null=True)),
            ('underlying_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('units_transacted', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('wavg_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('units_held', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('first_expiration_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('wavg_conversion', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('min_conversion_price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=15, decimal_places=4)),
            ('underlying_title', self.gf('django.db.models.fields.CharField')(max_length=80, null=True)),
        ))
        db.send_create_signal(u'sdapp', ['AggHoldingType'])

        # Deleting model 'SplitOrAdjustmentEvent'
        db.delete_table(u'sdapp_splitoradjustmentevent')

        # Deleting model 'Security'
        db.delete_table(u'sdapp_security')

        # Deleting model 'SecurityPriceHist'
        db.delete_table(u'sdapp_securitypricehist')

        # Adding field 'IssuerCIK.id'
        db.add_column(u'sdapp_issuercik', u'id',
                      self.gf('django.db.models.fields.AutoField')(default='error', primary_key=True),
                      keep_default=False)


        # Changing field 'IssuerCIK.cik_num'
        db.alter_column(u'sdapp_issuercik', 'cik_num', self.gf('django.db.models.fields.CharField')(max_length=10))
        # Adding field 'ClosePrice.companystockhist'
        db.add_column(u'sdapp_closeprice', 'companystockhist',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sdapp.CompanyStockHist'], null=True),
                      keep_default=False)

        # Deleting field 'ClosePrice.SecurityPriceHist'
        db.delete_column(u'sdapp_closeprice', 'SecurityPriceHist_id')

        # Adding field 'ReportingPerson.id'
        db.add_column(u'sdapp_reportingperson', u'id',
                      self.gf('django.db.models.fields.AutoField')(default='error', primary_key=True),
                      keep_default=False)


        # Changing field 'ReportingPerson.reporting_owner_cik_num'
        db.alter_column(u'sdapp_reportingperson', 'reporting_owner_cik_num', self.gf('django.db.models.fields.CharField')(max_length=10))
        # Deleting field 'Form345Entry.securty'
        db.delete_column(u'sdapp_form345entry', 'securty_id')


        # Changing field 'Form345Entry.filedatetime'
        db.alter_column(u'sdapp_form345entry', 'filedatetime', self.gf('django.db.models.fields.DateTimeField')(null=True))
        # Adding field 'Affiliation.most_recent_filing'
        db.add_column(u'sdapp_affiliation', 'most_recent_filing',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.is_ten_percent'
        db.add_column(u'sdapp_affiliation', 'is_ten_percent',
                      self.gf('django.db.models.fields.BooleanField')(default=0),
                      keep_default=False)

        # Adding field 'Affiliation.first_filing'
        db.add_column(u'sdapp_affiliation', 'first_filing',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Affiliation.is_something_else'
        db.add_column(u'sdapp_affiliation', 'is_something_else',
                      self.gf('django.db.models.fields.BooleanField')(default=0),
                      keep_default=False)

        # Adding field 'Affiliation.title'
        db.add_column(u'sdapp_affiliation', 'title',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True),
                      keep_default=False)

        # Adding field 'Affiliation.is_director'
        db.add_column(u'sdapp_affiliation', 'is_director',
                      self.gf('django.db.models.fields.BooleanField')(default=0),
                      keep_default=False)

        # Adding field 'Affiliation.is_officer'
        db.add_column(u'sdapp_affiliation', 'is_officer',
                      self.gf('django.db.models.fields.BooleanField')(default=0),
                      keep_default=False)

        # Adding field 'Affiliation.issuer_cik_num'
        db.add_column(u'sdapp_affiliation', 'issuer_cik_num',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=10),
                      keep_default=False)

        # Adding field 'Affiliation.reporting_owner_cik_num'
        db.add_column(u'sdapp_affiliation', 'reporting_owner_cik_num',
                      self.gf('django.db.models.fields.CharField')(default='error', max_length=10),
                      keep_default=False)


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
            'issuer_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'period_of_report': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'reporting_owner_cik': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.ReportingPerson']", 'null': 'True'}),
            'reporting_owner_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'reporting_owner_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'reporting_owner_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'sec_path': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'securty': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']", 'null': 'True'}),
            'shares_following_xn': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '15', 'decimal_places': '4'}),
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
            'cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'})
        },
        u'sdapp.reportingperson': {
            'Meta': {'object_name': 'ReportingPerson'},
            'person_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'reporting_owner_cik_num': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'})
        },
        u'sdapp.security': {
            'Meta': {'object_name': 'Security'},
            'deriv_or_nonderiv': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']"}),
            'public_price_available': ('django.db.models.fields.BooleanField', [], {}),
            'security_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'}),
            'underlying_title': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True'})
        },
        u'sdapp.securitypricehist': {
            'Meta': {'object_name': 'SecurityPriceHist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.IssuerCIK']", 'null': 'True'}),
            'security': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sdapp.Security']", 'null': 'True'}),
            'ticker_sym': ('django.db.models.fields.CharField', [], {'max_length': '5'})
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