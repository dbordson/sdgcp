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
    period_of_report = models.CharField(max_length=12)
    issuer_cik = models.ForeignKey(CIK)
    reporting_owner_cik = models.CharField(max_length=10)
    reporting_owner_name = models.CharField(max_length=40)
    is_director = models.BooleanField()
    is_officer = models.BooleanField()
    is_ten_percent = models.BooleanField()
    is_something_else = models.BooleanField()
    reporting_owner_title = models.CharField(max_length=40)
    security_title = models.CharField(max_length=40)
    conversion_price = models.DecimalField(max_digits=12, decimal_places=4)
    transaction_date = models.DateField()
    transaction_code = models.CharField(max_length=2)
    transaction_shares = models.DecimalField(max_digits=12, decimal_places=4)
    xn_price_per_share = models.DecimalField(max_digits=12, decimal_places=4)
    xn_acq_disp_code = models.CharField(max_length=2)
    expiration_date = models.DateField()
    underlying_title = models.CharField(max_length=40)
    underlying_shares = models.CharField(max_length=40)
    direct_or_indirect = models.CharField(max_length=2)
    tenbfive_note = models.BooleanField()
    transaction_number = models.IntegerField()
    source_name_partial_path = models.CharField(max_length=80)
    five_not_subject_to_section_sixteen = models.BooleanField()
    five_form_three_holdings = models.BooleanField()
    five_form_four_transactions = models.BooleanField()
    deriv_or_nonderiv = models.CharField(max_length=1)
