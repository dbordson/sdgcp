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
    companystockhist = models.ForeignKey(CompanyStockHist)

    def __unicode__(self):
        return self.cik_num
