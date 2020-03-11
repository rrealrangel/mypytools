# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 12:35:40 2019

@author: r.realrangel
"""
import numpy as np


# =============================================================================
# Scalar Attributes Characterizing 2×2 Contingency Tables
# =============================================================================
# Accuracy
def pc(hits, corrneg, n):
    """Compute the proportion correct (PC).

    Proposed by Finley (1884). This is simply the fraction of the n
    forecast occasions for which the nonprobabilistic forecast
    correctly anticipated the subsequent event or non event.

    Reference: Wilks, D. S. (2006). Statistical methods in the
    atmospheric sciences (2nd ed). Amsterdam ; Boston: Academic Press.

    Parameters
    ----------
    hits : float
        Occasions in which the event in question was succesfully
        forecast to occur. Also called "hits".
    corrneg : float
        Instances of the event not occurring after a forecast that it
        would not occur. Sometimes called "correct rejection" or
        "correct negative".
    n : flot
        Number of events.

    Return
    ------
    float
        The value of the proportion correct.
    """
    hits = float(hits)
    corrneg = float(corrneg)
    n = float(n)
    return((hits + corrneg) / n)


def ts(hits, falseal, misses):
    """Compute the threat score (TS).

    Also called the critical sucess index (CSI), this is an alternative
    to the proportion correct (PC) that is particularly useful when the
    event to forecast (as the yes event) occurs substantially less
    frequently than the nonoccurrence (no). Is the number of correct
    yes forecast divided by the total number of occasions on which that
    event was forecast and/or observed.

    Reference: Wilks, D. S. (2006). Statistical methods in the
    atmospheric sciences (2nd ed). Amsterdam ; Boston: Academic Press.

    Parameters
    ----------
    hits : float
        Occasions in which the event in question was succesfully
        forecast to occur. Also called "hits".
    falseal : float
        Occasions called "false alarms" on which the event was forcast
        to occur but did not.
    misses : float
        Instances of the event of interest occurring after a forecast
        that it would not occur, called "misses".

    Return
    ------
    float
        The value of the threat score.
    """
    hits = float(hits)
    falseal = float(falseal)
    misses = float(misses)

    try:
        return(hits / (hits + falseal + misses))

    except ZeroDivisionError:
        return(np.nan)


# Reliability and resolution.
def far(hits, falseal):
    """Compute the false alarm ratio (FAR).

    FAR is the fraction of yes forecasts that turn out to be wrong, or
    that proportion of the forecast events that fail to materialize.
    The FAR has a negative orientation, so that smaller values of FAR
    are the preferred. The best possible FAR is zero, and the worst
    possible FAR is one. The FAR has also been called the false alarm
    "rate".

    Reference: Wilks, D. S. (2006). Statistical methods in the
    atmospheric sciences (2nd ed). Amsterdam ; Boston: Academic Press.

    Parameters
    ----------
    hits : float
        Occasions in which the event in question was succesfully
        forecast to occur. Also called "hits".
    falseal : float
        Occasions called "false alarms" on which the event was forcast
        to occur but did not.

    Return
    ------
    float
        The value of the false alarm ratio.
    """
    hits = float(hits)
    falseal = float(falseal)

    try:
        return(falseal / (hits + falseal))

    except ZeroDivisionError:
        return(np.nan)


# Discriminiation.
def h(hits, misses):
    """Compute the hit rate (H).

    The hit rate is the ratio of correct forecasts to the number of
    times this event occurred. Equivalently, this statistic can be
    regarded as the fraction of those occasions when the forecast event
    occurred on which it was also forecast, and so is also called the
    probability of detection (POD).
        Reference: Wilks, D. S. (2006). Statistical methods in the
    atmospheric sciences (2nd ed). Amsterdam ; Boston: Academic Press.

    Parameters
    ----------
    hits : float
        Occasions in which the event in question was succesfully
        forecast to occur. Also called "hits".
    misses : float
        Instances of the event of interest occurring after a forecast
        that it would not occur, called "misses".

    Return
    ------
    float
        The value of the hit rate.
    """
    hits = float(hits)
    misses = float(misses)

    try:
        return(hits / (hits + misses))

    except ZeroDivisionError:
        return(np.nan)


# =============================================================================
# Skill Scores for 2×2 Contingency Tables
# =============================================================================
def heidke_ss(hits, falseal, misses, corrneg):
    """Compute the Heidke Skill Score (HSS).

    The HSS is a skill score based on the proportion correct (PC) as
    the basic accuracy measure. Thus, perfect forecasts receive HSS =
    1, forecasts equivalent to the reference forecasts receive zero,
    and forecasts worse than the reference forecast receive negative
    scores. The reference accuracy measure in the Heidke score is the
    proportion correct that would be achieved by random forecasts that
    are statistically independent of the observations.

    Reference: Wilks, D. S. (2006). Statistical methods in the
    atmospheric sciences (2nd ed). Amsterdam ; Boston: Academic Press.

    Parameters
    ----------
    hits : float
        Occasions in which the event in question was succesfully
        forecast to occur. Also called "hits".
    falseal : float
        Occasions called "false alarms" on which the event was forcast
        to occur but did not.
    misses : float
        Instances of the event of interest occurring after a forecast
        that it would not occur, called "misses".
    corrneg : float
        Instances of the event not occurring after a forecast that it
        would not occur. Sometimes called "correct rejection" or
        "correct negative".

    Return
    ------
    float
        The value of the Heidke Skill Score.
    """
    hits = float(hits)
    falseal = float(falseal)
    misses = float(misses)
    corrneg = float(corrneg)
    return(
        (2 * ((hits * corrneg) - (falseal * misses))) /
        (((hits + misses) * (misses + corrneg)) +
         ((hits + falseal) * (falseal + corrneg)))
        )


def peirce_ss(hits, falseal, misses, corrneg):
    """Compute the Peirce Skill Score (PSS).

    The Peirce Skill Score is formulated similarly to the Heidke score,
    except that the reference hit rate in the denominator is that for
    random forecasts that are constrained to be unbiased. The PSS can
    also been understood as the difference between two conditional
    probabilities in the likelyhood-base rate factorization of the
    joint distribution, namely the hit rate (H) and the false alarm
    rate (FAR); that is, PSS = H - FAR. Perfect forecasts receive a
    score of one, random forecasts receive a score of zero, and
    forecasts inferior to the random forecasts receive negative scores.

    Reference: Wilks, D. S. (2006). Statistical methods in the
    atmospheric sciences (2nd ed). Amsterdam ; Boston: Academic Press.

    Parameters
    ----------
    hits : float
        Occasions in which the event in question was succesfully
        forecast to occur. Also called "hits".
    falseal : float
        Occasions called "false alarms" on which the event was forcast
        to occur but did not.
    misses : float
        Instances of the event of interest occurring after a forecast
        that it would not occur, called "misses".
    corrneg : float
        Instances of the event not occurring after a forecast that it
        would not occur. Sometimes called "correct rejection" or
        "correct negative".

    Return
    ------
    float
        The value of the Peirce Skill Score.
    """
    hits = float(hits)
    falseal = float(falseal)
    misses = float(misses)
    corrneg = float(corrneg)
    return(
        ((hits * corrneg) - (falseal * misses)) /
        ((hits + misses) * (falseal + corrneg))
        )


def clayton_ss(hits, falseal, misses, corrneg):
    """Compute the Clayton Skill Score (CSS).

    Reference: Wilks, D. S. (2006). Statistical methods in the
    atmospheric sciences (2nd ed). Amsterdam ; Boston: Academic Press.

    Parameters
    ----------
    hits : float
        Occasions in which the event in question was succesfully
        forecast to occur. Also called "hits".
    falseal : float
        Occasions called "false alarms" on which the event was forcast
        to occur but did not.
    misses : float
        Instances of the event of interest occurring after a forecast
        that it would not occur, called "misses".
    corrneg : float
        Instances of the event not occurring after a forecast that it
        would not occur. Sometimes called "correct rejection" or
        "correct negative".

    Return
    ------
    float
        The value of the Peirce Skill Score.
    """
    hits = float(hits)
    falseal = float(falseal)
    misses = float(misses)
    corrneg = float(corrneg)
    return(
        ((hits * corrneg) - (falseal * misses)) /
        ((hits + falseal) * (misses + corrneg))
        )


def gilbert_ss(hits, falseal, misses, corrneg):
    """Compute the Gilbert Skill Score (GSS).

    Reference: Wilks, D. S. (2006). Statistical methods in the
    atmospheric sciences (2nd ed). Amsterdam ; Boston: Academic Press.

    Parameters
    ----------
    hits : float
        Occasions in which the event in question was succesfully
        forecast to occur. Also called "hits".
    falseal : float
        Occasions called "false alarms" on which the event was forcast
        to occur but did not.
    misses : float
        Instances of the event of interest occurring after a forecast
        that it would not occur, called "misses".
    corrneg : float
        Instances of the event not occurring after a forecast that it
        would not occur. Sometimes called "correct rejection" or
        "correct negative".

    Return
    ------
    float
        The value of the Peirce Skill Score.
    """
    hits = float(hits)
    falseal = float(falseal)
    misses = float(misses)
    corrneg = float(corrneg)
    n = hits + falseal + misses + corrneg
    a_ref = ((hits + falseal) * (hits + misses)) / n
    return((hits - a_ref) / (hits - a_ref + falseal + misses))
