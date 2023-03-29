from sklearn.metrics import (
    roc_auc_score, roc_curve, 
    accuracy_score, matthews_corrcoef, f1_score, precision_score, recall_score
)
from .log_util import logger
import numpy as np
from scipy import stats


def calc_metrics(y_true, y_score, threshold = 0.5):
    if not isinstance(y_score, np.ndarray):
        y_score = np.array(y_score)
    y_score = y_score > threshold
    accuracy = accuracy_score(y_true, y_score)
    f1 = f1_score(y_true, y_score)
    mcc = matthews_corrcoef(y_true, y_score)
    precision = precision_score(y_true, y_score)
    recall = recall_score(y_true, y_score)
    return accuracy, f1, mcc, precision, recall


def calc_f1_precision_recall(y_true, y_predict):
    """  """
    # accuracy = accuracy_score(y_true, y_predict)
    f1 = f1_score(y_true, y_predict)
    precision = precision_score(y_true, y_predict)
    recall = recall_score(y_true, y_predict)
    return f1, precision, recall


def find_threshold(y_true, y_score, alpha = 0.05):
    """ return threshold when fpr <= 0.05 """
    fpr, tpr, thresh = roc_curve(y_true, y_score)
    for i, _fpr in enumerate(fpr):
        if _fpr > alpha:
            return thresh[i-1]


def roc(y_true, y_score):
    fpr, tpr, thresh = roc_curve(y_true, y_score)
    roc = roc_auc_score(y_true, y_score)
    return roc, fpr, tpr


def calc_metrics_at_thresholds(y_true, y_pred_probability, thresholds=None, default_threshold=None):
    """  """
    if default_threshold:
        accuracy, f1, mcc, precision, recall = calc_metrics(y_true, y_pred_probability, default_threshold)
        logger.info(f'default_threshold {default_threshold}')
        logger.info(f"accuracy: {accuracy}\nf1: {f1}\nmcc: {mcc}\nprecision: {precision}\nrecall: {recall}")

    if not thresholds: return
    for threshold in thresholds:
        accuracy, f1, mcc, precision, recall = calc_metrics(y_true, y_pred_probability, threshold)
        logger.info(f"\nthreshold: {threshold}\naccuracy: {accuracy}\nf1: {f1}\nmcc: {mcc}\nprecision: {precision}\nrecall: {recall}")

        if default_threshold:
            # Extra test on the threshold value
            mil_threshold =  (threshold + default_threshold) / 2
            accuracy, f1, mcc, precision, recall = calc_metrics(y_true, y_pred_probability, mil_threshold)
            logger.info(f'mil_threshold {mil_threshold} which is the mean of threshold and default threshold')
            logger.info(f"accuracy: {accuracy}\nf1: {f1}\nmcc: {mcc}\nprecision: {precision}\nrecall: {recall}")


def calc_spearmanr(x, y):
    """
    Although calculation of the p-value does not make strong assumptions about the distributions underlying the samples, it is only accurate for very large samples (>500 observations). For smaller sample sizes, consider a permutation test.
    For small samples(<= 500 observations), consider performing a permutation test instead of relying on the asymptotic p-value. Note that to calculate the null distribution of the statistic (for all possibly pairings between observations in sample x and y), only one of the two inputs needs to be permuted.
    """
    res = stats.spearmanr(x, y)
    spearmanr = res.statistic
    pvalue = res.pvalue
    if len(x) <= 500:
        # logger.info(f'for small samples(<= 500 observations), the res_asymptotic.pvalue is {res.pvalue}, not accurate.\nPerform a permutation test to get exact pvalue')
        def statistic(x):  # permute only `x`
            return stats.spearmanr(x, y).statistic

        res_exact = stats.permutation_test((x,), statistic, permutation_type='pairings')
        pvalue = res_exact.pvalue
    logger.info(f'spearmanr {spearmanr}, pvalue {pvalue}')
    return spearmanr, pvalue
