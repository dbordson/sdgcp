from django.db import models

# class StockHistories(models.Model):
#


class IssuerCIK(models.Model):
    cik_num = models.CharField(max_length=10)
    # Adapt this for companies with more than one public stock (GOOG)
    # to do this, we will need to update the ticker finder script

    def __unicode__(self):
        return self.cik_num


class CompanyStockHist(models.Model):
    ticker_sym = models.CharField(max_length=5)
    # stockhistories = models.ForeignKey(StockHistories)
    # last_update = models.DateField(auto_now=True)
    issuer = models.ForeignKey(IssuerCIK, null=True)

    def __unicode__(self):
        return self.ticker_sym


class ClosePrice(models.Model):
    close_price = models.DecimalField(max_digits=12, decimal_places=4)
    close_date = models.DateField()
    companystockhist = models.ForeignKey(CompanyStockHist, null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (self.companystockhist, self.close_price,
                                self.close_date)


class ReportingPerson(models.Model):
    person_name = models.CharField(max_length=80)
    reporting_owner_cik_num = models.CharField(max_length=10)

    def __unicode__(self):
        return self.person_name


class Affiliation(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    reporting_owner = models.ForeignKey(ReportingPerson)
    issuer_cik_num = models.CharField(max_length=10)
    reporting_owner_cik_num = models.CharField(max_length=10)
    person_name = models.CharField(max_length=80, null=True)
    title = models.CharField(max_length=30, null=True)
    is_director = models.BooleanField()
    is_officer = models.BooleanField()
    is_ten_percent = models.BooleanField()
    is_something_else = models.BooleanField()
    first_filing = models.DateField(null=True)
    most_recent_filing = models.DateField(null=True)

    def __unicode__(self):
        return unicode(self.title) or u''


class AggHoldingType(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    security_title = models.CharField(max_length=80, null=True)
    units_held = models.DecimalField(max_digits=15, decimal_places=4,
                                     null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    first_expiration_date = models.DateField(null=True)
    last_expiration_date = models.DateField(null=True)
    wavg_expiration_date = models.DateField(null=True)
    min_conversion_price = models.DecimalField(max_digits=15, decimal_places=4,
                                               null=True)
    max_conversion_price = models.DecimalField(max_digits=15, decimal_places=4,
                                               null=True)
    wavg_conversion = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    underlying_title = models.CharField(max_length=80, null=True)
    underlying_shares = models.DecimalField(max_digits=15, decimal_places=4,
                                            null=True)
    underlying_price = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)
    intrinsic_value = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    first_xn = models.DateField(null=True)
    most_recent_xn = models.DateField(null=True)
    wavg_xn_date = models.DateField(null=True)
    transactions_included = models.IntegerField(null=True)
    tranches_included = models.IntegerField(null=True)
    units_transacted = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)

    def __unicode__(self):
        return unicode(self.security_title) or u''


class HoldingType(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    owner = models.ForeignKey(ReportingPerson)
    affiliation = models.ForeignKey(Affiliation)
    security_title = models.CharField(max_length=80, null=True)
    units_held = models.DecimalField(max_digits=15, decimal_places=4,
                                     null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    first_expiration_date = models.DateField(null=True)
    last_expiration_date = models.DateField(null=True)
    wavg_expiration_date = models.DateField(null=True)
    min_conversion_price = models.DecimalField(max_digits=15, decimal_places=4,
                                               null=True)
    max_conversion_price = models.DecimalField(max_digits=15, decimal_places=4,
                                               null=True)
    wavg_conversion = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    underlying_title = models.CharField(max_length=80, null=True)
    underlying_shares = models.DecimalField(max_digits=15, decimal_places=4,
                                            null=True)
    underlying_price = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)
    intrinsic_value = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    first_xn = models.DateField(null=True)
    most_recent_xn = models.DateField(null=True)
    wavg_xn_date = models.DateField(null=True)
    transactions_included = models.IntegerField(null=True)
    tranches_included = models.IntegerField(null=True)
    units_transacted = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)

    def __unicode__(self):
        return unicode(self.security_title) or u''


class Holding(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    owner = models.ForeignKey(ReportingPerson)
    affiliation = models.ForeignKey(Affiliation)
    security_title = models.CharField(max_length=80, null=True)
    units_held = models.DecimalField(max_digits=15, decimal_places=4,
                                     null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    expiration_date = models.DateField(null=True)
    conversion_price = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)
    underlying_title = models.CharField(max_length=80, null=True)
    underlying_shares = models.DecimalField(max_digits=15, decimal_places=4,
                                            null=True)
    first_xn = models.DateField(null=True)
    most_recent_xn = models.DateField(null=True)

    def __unicode__(self):
        return unicode(self.security_title) or u''


class FTPFileList(models.Model):
    files = models.TextField()

    def __unicode__(self):
        return unicode(len(self.files)) or u''


class FullForm(models.Model):
    sec_path = models.CharField(max_length=150, primary_key=True)
    save_date = models.DateField(null=True)
    issuer_cik_num = models.CharField(max_length=10)
    text = models.TextField()

    def __unicode__(self):
        return unicode(self.sec_path, self.save_date) or u''


class Form345Entry(models.Model):
    entry_internal_id = models.CharField(max_length=80)
    period_of_report = models.DateField(null=True)
    issuer_cik = models.ForeignKey(IssuerCIK, null=True)
    issuer_cik_num = models.CharField(max_length=10)
    reporting_owner_cik = models.ForeignKey(ReportingPerson, null=True)
    reporting_owner_cik_num = models.CharField(max_length=10)
    reporting_owner_name = models.CharField(max_length=80, null=True)
    is_director = models.BooleanField()
    is_officer = models.BooleanField()
    is_ten_percent = models.BooleanField()
    is_something_else = models.BooleanField()
    reporting_owner_title = models.CharField(max_length=80, null=True)
    security_title = models.CharField(max_length=80, null=True)
    conversion_price = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)
    transaction_date = models.DateField(null=True)
    transaction_code = models.CharField(max_length=2, null=True)
    transaction_shares = models.DecimalField(max_digits=15, decimal_places=4,
                                             null=True)
    xn_price_per_share = models.DecimalField(max_digits=15, decimal_places=4,
                                             null=True)
    xn_acq_disp_code = models.CharField(max_length=2, null=True)
    expiration_date = models.DateField(null=True)
    underlying_title = models.CharField(max_length=80, null=True)
    underlying_shares = models.DecimalField(max_digits=15, decimal_places=4,
                                            null=True)
    shares_following_xn = models.DecimalField(max_digits=15, decimal_places=4,
                                              null=True)
    direct_or_indirect = models.CharField(max_length=2, null=True)
    tenbfive_note = models.IntegerField(null=True)
    transaction_number = models.IntegerField(null=True)
    sec_path = models.CharField(max_length=150, null=True)
    five_not_subject_to_section_sixteen = models.IntegerField(null=True)
    five_form_three_holdings = models.IntegerField(null=True)
    five_form_four_transactions = models.IntegerField(null=True)
    form_type = models.CharField(max_length=5, null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    filedatetime = models.DateTimeField(null=True)
    supersededdt = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.entry_internal_id
