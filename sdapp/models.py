from django.db import models


# class StockHistories(models.Model):
#


class CompanyStockHist(models.Model):
    ticker_sym = models.CharField(max_length=5)
    # stockhistories = models.ForeignKey(StockHistories)
    # last_update = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.ticker_sym


class ClosePrice(models.Model):
    close_price = models.DecimalField(max_digits=12, decimal_places=4)
    close_date = models.DateField()
    companystockhist = models.ForeignKey(CompanyStockHist)

    def __unicode__(self):
        return u"%s, %s, %s" % (self.companystockhist, self.close_price,
                                self.close_date)


class CIK(models.Model):
    cik_num = models.CharField(max_length=10)
    companystockhist = models.OneToOneField(CompanyStockHist, primary_key=True)

    def __unicode__(self):
        return self.cik_num


class Form345Entry(models.Model):
    entry_internal_id = models.CharField(max_length=80)
    period_of_report = models.CharField(max_length=12, null=True)
    issuer_cik = models.ForeignKey(CIK, null=True)
    reporting_owner_cik = models.CharField(max_length=10, null=True)
    reporting_owner_name = models.CharField(max_length=40, null=True)
    is_director = models.BooleanField()
    is_officer = models.BooleanField()
    is_ten_percent = models.BooleanField()
    is_something_else = models.BooleanField()
    reporting_owner_title = models.CharField(max_length=40, null=True)
    security_title = models.CharField(max_length=40, null=True)
    conversion_price = models.DecimalField(max_digits=12, decimal_places=4,
                                           null=True)
    transaction_date = models.DateField(null=True)
    transaction_code = models.CharField(max_length=2, null=True)
    transaction_shares = models.DecimalField(max_digits=12, decimal_places=4,
                                             null=True)
    xn_price_per_share = models.DecimalField(max_digits=12, decimal_places=4,
                                             null=True)
    xn_acq_disp_code = models.CharField(max_length=2, null=True)
    expiration_date = models.DateField(null=True)
    underlying_title = models.CharField(max_length=40, null=True)
    underlying_shares = models.DecimalField(max_digits=12, decimal_places=4,
                                            null=True)
    shares_following_xn = models.DecimalField(max_digits=12, decimal_places=4,
                                              null=True)
    direct_or_indirect = models.CharField(max_length=2, null=True)
    tenbfive_note = models.IntegerField(null=True)
    transaction_number = models.IntegerField(null=True)
    source_name_partial_path = models.CharField(max_length=80, null=True)
    five_not_subject_to_section_sixteen = models.IntegerField(null=True)
    five_form_three_holdings = models.IntegerField(null=True)
    five_form_four_transactions = models.IntegerField(null=True)
    form_type = models.CharField(max_length=5, null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
