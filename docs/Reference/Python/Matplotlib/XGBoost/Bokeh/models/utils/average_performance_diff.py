def average_performance_diff(dataset):
    lgbm_series = pd.Series(dataset['lgbm']['performance'])
    try:
        perf = 100*((lgbm_series-pd.Series(dataset['xgb']['performance']))/lgbm_series).mean()
    except KeyError:
        perf = None
    return perf
