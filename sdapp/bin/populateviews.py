from sdapp.models import ReportingPerson, IssuerCIK, Form345Entry,\
    Affiliation, ClosePrice, SecurityPriceHist
# from django.db import connection
import datetime


def weighted_avg(vectorunitoutput, weightingvector):
    dotproduct = sum(p * q for p, q in zip(vectorunitoutput, weightingvector))
    divisor = sum(weightingvector)
    wavg = dotproduct / divisor
    return wavg


def wavgdate(datevector, weightvector):
    try:
        today = datetime.date.today()
        tdvector = [float((entry - today).days) for entry in datevector]
        # the below line doesn't work with single entry lists
        if len(tdvector) == 1:
            return (today + datetime.timedelta(tdvector[0]))
        dotproduct = sum(float(p) * float(q)
                         for p, q in zip(tdvector, weightvector))
        denominator = sum(weightvector)
        wavgdelta = dotproduct / float(denominator)
        wavg = today + datetime.timedelta(wavgdelta)
        return wavg
    except:
        return None


def intrinsicvalcalc(conv_vector, unitsvector, underlyingprice):
    up = underlyingprice
    inthemoneyvector = [float(max((up - float(entry)), 0))
                        for entry in conv_vector]
    if len(inthemoneyvector) == 1:
        return float(inthemoneyvector[0]) * float(unitsvector[0])
    else:
        dotproduct =\
            sum(float(p) * float(q)
                for p, q in zip(inthemoneyvector, unitsvector))
        return dotproduct










