def train_time_ratio(dataset):
    try: 
        val = dataset['xgb']['train_time']/dataset['lgbm']['train_time']
    except KeyError:
        val = None
    return val

def train_time_ratio_hist(dataset):
    try: 
        val = dataset['xgb_hist']['train_time']/dataset['lgbm']['train_time']
    except KeyError:
        val = None
    return val

def test_time_ratio(dataset):
    try: 
        val = dataset['xgb']['test_time']/dataset['lgbm']['test_time']
    except KeyError:
        val = None
    return val
 
In [14]:
metrics = juxt(average_performance_diff, train_time_ratio, train_time_ratio_hist, test_time_ratio)
res_per_dataset = {dataset_key:metrics(dataset) for dataset_key, dataset in results.items()}
 
In [15]:
results_df = pd.DataFrame(res_per_dataset, index=['Perf. Difference(%)', 
                                                  'Train Time Ratio',
                                                  'Train Time Ratio Hist',
                                                  'Test Time Ratio']).T
 
In [16]:
results_df
