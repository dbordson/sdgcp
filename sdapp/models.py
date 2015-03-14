from django.db import models
from decimal import Decimal
# class StockHistories(models.Model):
#


class IssuerCIK(models.Model):
    cik_num = models.IntegerField(primary_key=True)
    # Adapt this for companies with more than one public stock (GOOG)
    # to do this, we will need to update the ticker finder script

    def __unicode__(self):
        return str(self.cik_num)


class ReportingPerson(models.Model):
    person_name = models.CharField(max_length=80)
    reporting_owner_cik_num = models.IntegerField(primary_key=True)

    def __unicode__(self):
        return self.person_name


class Affiliation(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    reporting_owner = models.ForeignKey(ReportingPerson)
    person_name = models.CharField(max_length=80, null=True)

    def __unicode__(self):
        return unicode(self.person_name) or u''


class Security(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    short_sec_title = models.CharField(max_length=80, null=True)
    ticker = models.CharField(max_length=10, null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    scrubbed_underlying_title = models.CharField(max_length=80, null=True)
    conversion_multiple = models.DecimalField(max_digits=15, decimal_places=4,
                                              default=Decimal('1.00'))

    def __unicode__(self):
        return unicode(self.short_sec_title) or u''


class SecurityPriceHist(models.Model):
    ticker_sym = models.CharField(max_length=10)
    # stockhistories = models.ForeignKey(StockHistories)
    # last_update = models.DateField(auto_now=True)
    issuer = models.ForeignKey(IssuerCIK, null=True)
    security = models.ForeignKey(Security, null=True)

    def __unicode__(self):
        return self.ticker_sym


class ClosePrice(models.Model):
    close_price = models.DecimalField(max_digits=12, decimal_places=4)
    adj_close_price = models.DecimalField(max_digits=12, decimal_places=4)
    close_date = models.DateField()
    securitypricehist = models.ForeignKey(SecurityPriceHist, null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (str(self.securitypricehist),
                                str(self.close_price),
                                str(self.close_date))


class SplitOrAdjustmentEvent(models.Model):
    security = models.ForeignKey(Security)
    adjustment_factor = models.DecimalField(max_digits=15, decimal_places=4)
    event_date = models.DateField(null=True)

    def __unicode__(self):
        return unicode(self.security) or u''


class TransactionEvent(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    net_xn_val = models.DecimalField(max_digits=15, decimal_places=4,
                                     null=True)
    end_holding_val = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    net_xn_pct = models.DecimalField(max_digits=15, decimal_places=4,
                                     null=True)
    period_start = models.DateField(null=True)
    period_end = models.DateField(null=True)
    price_at_period_end = models.DecimalField(max_digits=15, decimal_places=4,
                                              null=True)
    perf_at_91_days = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    perf_at_182_days = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)
    perf_at_274_days = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)
    perf_at_365_days = models.DecimalField(max_digits=15,
                                           decimal_places=4,
                                           null=True)
    perf_at_456_days = models.DecimalField(max_digits=15,
                                           decimal_places=4,
                                           null=True)

    def __unicode__(self):
        return u"%s, %s, %s" % (str(self.issuer),
                                str(self.period_start),
                                str(self.period_end))


class SecurityView(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    security = models.ForeignKey(Security)
    short_sec_title = models.CharField(max_length=80, null=True)
    ticker = models.CharField(max_length=10, null=True)
    last_close_price = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)
    # security_title = models.CharField(max_length=80, null=True)
    units_held = models.DecimalField(max_digits=15, decimal_places=4,
                                     null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    first_expiration_date = models.DateField(null=True)
    last_expiration_date = models.DateField(null=True)
    wavg_expiration_date = models.DateField(null=True)
    min_conversion_price = models.DecimalField(max_digits=15,
                                               decimal_places=4,
                                               null=True)
    max_conversion_price = models.DecimalField(max_digits=15,
                                               decimal_places=4,
                                               null=True)
    wavg_conversion = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    # underlying_title = models.CharField(max_length=80, null=True)
    scrubbed_underlying_title = models.CharField(max_length=80, null=True)
    underlying_ticker = models.CharField(max_length=10, null=True)
    underlying_shares_total = models.DecimalField(max_digits=15,
                                                  decimal_places=4,
                                                  null=True)
    underlying_close_price = models.DecimalField(max_digits=15,
                                                 decimal_places=4,
                                                 null=True)
    intrinsic_value = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    first_xn = models.DateField(null=True)
    most_recent_xn = models.DateField(null=True)
    wavg_xn_date = models.DateField(null=True)

    def __unicode__(self):
        return unicode(self.short_sec_title) or u''


class PersonHoldingView(models.Model):
    issuer = models.ForeignKey(IssuerCIK)
    owner = models.ForeignKey(ReportingPerson)
    person_name = models.CharField(max_length=80, null=True)
    person_title = models.CharField(max_length=80, null=True)
    security = models.ForeignKey(Security)
    affiliation = models.ForeignKey(Affiliation)
    short_sec_title = models.CharField(max_length=80, null=True)
    ticker = models.CharField(max_length=10, null=True)
    last_close_price = models.DecimalField(max_digits=15, decimal_places=4,
                                           null=True)
    # security_title = models.CharField(max_length=80, null=True)
    units_held = models.DecimalField(max_digits=15, decimal_places=4,
                                     null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    first_expiration_date = models.DateField(null=True)
    last_expiration_date = models.DateField(null=True)
    wavg_expiration_date = models.DateField(null=True)
    min_conversion_price = models.DecimalField(max_digits=15,
                                               decimal_places=4,
                                               null=True)
    max_conversion_price = models.DecimalField(max_digits=15,
                                               decimal_places=4,
                                               null=True)
    wavg_conversion = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    # underlying_title = models.CharField(max_length=80, null=True)
    scrubbed_underlying_title = models.CharField(max_length=80, null=True)
    underlying_ticker = models.CharField(max_length=10, null=True)
    underlying_shares_total = models.DecimalField(max_digits=15,
                                                  decimal_places=4,
                                                  null=True)
    underlying_close_price = models.DecimalField(max_digits=15,
                                                 decimal_places=4,
                                                 null=True)
    intrinsic_value = models.DecimalField(max_digits=15, decimal_places=4,
                                          null=True)
    first_xn = models.DateField(null=True)
    most_recent_xn = models.DateField(null=True)
    wavg_xn_date = models.DateField(null=True)

    def __unicode__(self):
        return unicode(self.short_sec_title) or u''


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
        return unicode(self.sec_path, str(self.save_date)) or u''


class Form345Entry(models.Model):
    entry_internal_id = models.CharField(max_length=80)
    period_of_report = models.DateField(null=True)
    issuer_cik = models.ForeignKey(IssuerCIK, null=True)
    issuer_cik_num = models.IntegerField(max_length=10)
    issuer_name = models.CharField(max_length=80, null=True)
    security = models.ForeignKey(Security, null=True,
                                 related_name="security_relationship")
    reporting_owner_cik = models.ForeignKey(ReportingPerson, null=True)
    reporting_owner_cik_num = models.IntegerField(max_length=10)
    reporting_owner_name = models.CharField(max_length=80, null=True)
    affiliation = models.ForeignKey(Affiliation, null=True)
    is_director = models.BooleanField()
    is_officer = models.BooleanField()
    is_ten_percent = models.BooleanField()
    is_something_else = models.BooleanField()
    reporting_owner_title = models.CharField(max_length=80, null=True)
    security_title = models.CharField(max_length=80, null=True)
    short_sec_title = models.CharField(max_length=80, null=True)
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
    scrubbed_underlying_title = models.CharField(max_length=80, null=True)
    underlying_shares = models.DecimalField(max_digits=15, decimal_places=4,
                                            null=True)
    shares_following_xn = models.DecimalField(max_digits=15, decimal_places=4,
                                              null=True)
    reported_shares_following_xn = models.DecimalField(max_digits=15,
                                                       decimal_places=4,
                                                       null=True)
    shares_following_xn_is_adjusted = models.BooleanField(default=False)
    direct_or_indirect = models.CharField(max_length=2, null=True)
    tenbfive_note = models.IntegerField(null=True)
    transaction_number = models.IntegerField(null=True)
    sec_path = models.CharField(max_length=150, null=True)
    five_not_subject_to_section_sixteen = models.IntegerField(null=True)
    five_form_three_holdings = models.IntegerField(null=True)
    five_form_four_transactions = models.IntegerField(null=True)
    form_type = models.CharField(max_length=5, null=True)
    deriv_or_nonderiv = models.CharField(max_length=1, null=True)
    filedatetime = models.DateTimeField()
    supersededdt = models.DateTimeField(null=True)
    adjustment_factor = models.DecimalField(max_digits=15, decimal_places=4,
                                            default=Decimal('1.00'))
    adjustment_date = models.DateField(null=True)
    underlying_security = \
        models.ForeignKey(Security, null=True,
                          related_name="underlying_relationship")

    def __unicode__(self):
        return str(self.entry_internal_id)
