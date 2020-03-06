import pandas as pd
from sklearn.metrics import accuracy_score 
from sklearn.preprocessing import LabelEncoder 
from sklearn.model_selection import train_test_split 
import cudf
import dask
import dask_cudf
import dask_xgboost
import numpy as np
import os,sys
from dask.distributed import Client
import time, argparse

args = argparse.ArgumentParser()
args.add_argument('--nrows', default=1000000, type=int,
                    help='number of rows of input matrix')
args.add_argument('--npartitions', default=6, type=int,
                    help='number of data partitions')
args.add_argument('--check', action='store_true', default=False,
                    help='sanity check or not')
args = args.parse_args()
nrows = args.nrows
sanity_check = args.check
npartitions = args.npartitions
ncols = 250 
dsize=nrows*ncols*4./10**9
ndrop = 3

params = {
    'num_rounds':   100,
    'max_depth':    8,
    'max_leaves':   2**8,
    'n_gpus':       1,
    'tree_method':  'gpu_hist',
    'objective':    'reg:squarederror',
    'grow_policy':  'lossguide'
}

def validation(client):
  filename = os.path.join(os.getenv('WORKDIR'), '../iris.data') 
  pdf = pd.read_csv(filename, names=['sepal length','sepal width','petal length','petal width','target'])
  pdf = pdf.sample(frac=1)
  label_encoder = LabelEncoder()
  pdf['target'] = label_encoder.fit_transform(pdf['target'])
  X = pdf.drop('target',1)
  y = pdf['target']
  #y = (pdf['target'] > 0).astype(int) 
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

  X_train_dask_pdf = dask.dataframe.from_pandas(X_train, npartitions=npartitions)
  X_test_dask_pdf = dask.dataframe.from_pandas(X_test, npartitions=npartitions)
  y_train_dask_pdf = dask.dataframe.from_pandas(y_train, npartitions=npartitions)
  y_test_dask_pdf = dask.dataframe.from_pandas(y_test, npartitions=npartitions)
   
  X_train_dask_cdf = dask_cudf.from_dask_dataframe(X_train_dask_pdf)
  X_test_dask_cdf = dask_cudf.from_dask_dataframe(X_test_dask_pdf)
  y_train_dask_cdf = dask_cudf.from_dask_dataframe(y_train_dask_pdf)
  y_test_dask_cdf = dask_cudf.from_dask_dataframe(y_test_dask_pdf)

  X_train_dask_cdf = X_train_dask_cdf.persist()
  y_train_dask_cdf = y_train_dask_cdf.persist()
  X_test_dask_cdf = X_test_dask_cdf.persist()
  y_test_dask_cdf = y_test_dask_cdf.persist()

  #params['objective'] = 'binary:logistic'
  #params['objective'] = 'multi:softprob'
  #params['num_class'] = 3
  bst = dask_xgboost.train(client, params, X_train_dask_cdf, y_train_dask_cdf, 
                           num_boost_round=params['num_rounds'])
  pred = dask_xgboost.predict(client, bst, X_test_dask_cdf)
  pred = dask.dataframe.multi.concat([pred], axis=1)
  pred_test = [ int(round(i)) for i in pred[0].compute()]
  print ("Accuracy: %g"%(accuracy_score(y_test, pred_test)))
  for y,p in zip(y_test, pred_test):
    print ("y_test: %d y_pred %d"%(y,p))

def benchmark(client):
  
  pdf = pd.DataFrame(np.array(np.random.normal(0, 1, (nrows,ncols+1)), dtype=np.float32))
  X = pdf.iloc[:,0:-1]
  y = pdf.iloc[:,-1]
  X_dask_pdf = dask.dataframe.from_pandas(X, npartitions=npartitions)
  y_dask_pdf = dask.dataframe.from_pandas(y, npartitions=npartitions)
   
  X_dask_cdf = dask_cudf.from_dask_dataframe(X_dask_pdf)
  y_dask_cdf = dask_cudf.from_dask_dataframe(y_dask_pdf)

  #t = time.time()
  #bst = dask_xgboost.train(client, params, X_dask_cdf, y_dask_cdf, num_boost_round=params['num_rounds'])
  #print('training on first load data: %f (GB/s)'%(dsize/(time.time()-t))) 
  
  X_dask_cdf = X_dask_cdf.persist()
  y_dask_cdf = y_dask_cdf.persist()

  speed=[]
  for it in range(10):
    t = time.time()
    bst = dask_xgboost.train(client, params, X_dask_cdf, y_dask_cdf, num_boost_round=params['num_rounds'])
    speed.append(dsize/(time.time()-t))
  speed = np.array(speed)
  print('training on persist data: %f (%f) (GB/s)'%(speed[ndrop:].mean(), speed[ndrop:].std()))

  
 
if __name__ == '__main__':

  scheduler_file = os.getenv('WORKDIR') + '/my-scheduler-gpu.json'
  client = Client(scheduler_file=scheduler_file)
  '''
  client.run(
        rmm.reinitialize,
        pool_allocator=True,
        managed_memory=False,
        initial_pool_size=2**31,
  )
  ''' 
  if sanity_check:
    validation(client) 

  benchmark(client)
