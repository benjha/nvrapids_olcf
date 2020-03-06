import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.decomposition import PCA as skPCA
import cudf,rmm
from cuml import PCA as cumlPCA
from cuml import KMeans as cumlKMeans 
import time, argparse

n_components=3
whiten = False
random_state = 42
svd_solver="full"
npartitions=6
ndrop = 3 

args = argparse.ArgumentParser()
args.add_argument('--nrows', default=1000000, type=int,
                    help='number of rows of input matrix')
args.add_argument('--check', action='store_true', default=False,
                    help='sanity check or not')
args = args.parse_args()
nrows = args.nrows
sanity_check = args.check 
ncols = 250
dsize=nrows*ncols*4./10**9

def verification_test():
  def to_nparray(x):
      if isinstance(x,np.ndarray) or isinstance(x,pd.DataFrame):
          return np.array(x)
      elif isinstance(x,np.float64):
          return np.array([x])
      elif isinstance(x,cudf.DataFrame) or isinstance(x,cudf.Series):
          return x.to_pandas().values
      return x

  def array_equal(a,b,threshold=1e-3,with_sign=True):
      a = to_nparray(a)
      b = to_nparray(b)
      if with_sign == False:
        a,b = np.abs(a),np.abs(b)
      error = mean_squared_error(a,b)
      res = error<threshold
      return res

  df = pd.read_csv('iris.data', names=['sepal length','sepal width','petal length','petal width','target'])

  X = df.drop('target',1)
  y = df['target']

  pca = skPCA(n_components=n_components,svd_solver=svd_solver,
	    whiten=whiten, random_state=random_state)  
  result_sk = pca.fit_transform(X)  
  explained_variance_sk = pca.explained_variance_ratio_  
  print(explained_variance_sk)

  cuX = cudf.DataFrame.from_pandas(X)
  pca_cuml = cumlPCA(n_components=n_components,svd_solver=svd_solver, 
	      whiten=whiten, random_state=random_state)
  result_cuml = pca_cuml.fit_transform(cuX)
  explained_variance_cuml = pca_cuml.explained_variance_ratio_  
  print(explained_variance_cuml)


  passed = array_equal(result_sk,result_cuml)
  message = 'cuml.PCA sanity check %s'%('PASS'if passed else 'FAIL')
  print(message)
  

def benchmark():
  pca_cuml = cumlPCA(n_components=n_components,svd_solver=svd_solver, 
	      whiten=whiten, random_state=random_state)
  kmeans_cuml = cumlKMeans(n_clusters=2,max_iter=2)
  benchmarks = [pca_cuml, kmeans_cuml]
  df = pd.DataFrame(data=np.random.normal(0,1,(nrows,ncols)).astype('float32'))  
  cdf = cudf.from_pandas(df)
  #pdf = dask.dataframe.from_pandas(df, npartitions=npartitions)
  #ddf = dask_cudf.from_dask_dataframe(pdf)

  for bench in benchmarks:   
    #t = time.time()
    #bench.fit(cdf)
    #print('%s: training on first load data: %f (GB/s)'%(bench, dsize/(time.time()-t)))
  
    #cdf.persist()
    speed=[]
    for it in range(10): 
      t = time.time()
      bench.fit(cdf)
      speed.append(dsize/(time.time()-t))
    speed = np.array(speed)
    print('%s: training on persist data: %f (%f) (GB/s)'%(bench, speed[ndrop:].mean(), speed[ndrop:].std()))
 

if __name__ == '__main__':
  #cluster = LocalCUDACluster()
  #client = Client(cluster)
  rmm.reinitialize(
    pool_allocator=True,
    managed_memory=True,
    initial_pool_size=2**31,
  )
  if sanity_check:  
    verification_test()
  benchmark()

