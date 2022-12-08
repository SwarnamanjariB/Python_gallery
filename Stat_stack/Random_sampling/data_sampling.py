
# Let's understand each sampling method and compare them based on thier randomness and bias.

import numpy.random as npr
import numpy        as np
import random       as rnd
import pandas       as pd

# Sampling - extracting a sample subset from the available population as its representative.
# Types: Random/probability, Systematic, Stratified, wieghted  and Cluster sampling.

class Data_sampling:
    def __init__(self,data_path):
            self.df = pd.read_csv(data_path)
            print("\n Original data (Population): \n",self.df.head())

    def random_sampling(self,n):
            # Random/probability sampling - The elements have equal probability to be extracted. 
            # This method is prone to bias and used when no information on the data is available.
            sample = self.df.sample(n)
            return sample


    def systematic_sampling(self,n):
            # Systematic sampling extracts the data points on a fixed interval index.
            # This method is prone to creating a biased subset. 
            # Can be used to collect sampleset with a timeframe.
            step      = int(len(self.df)/n)
            Intervals = np.arange(1,len(self.df),step)
            sample    = self.df.iloc[Intervals]
            return sample

    def clustered_sampling(self,n):
            # Clustered sampling method randomly groups the data points and 
            # picks any cluster to generate the sample. This doesn't seem to address the bias either.
            N        = len(self.df)
            K        = int(N/n)
            df       = self.df
            clusters = None
            for i in range(K):
                cluster          = df.sample(n)
                cluster["CL_ID"] = np.repeat(i,len(cluster))
                df               = df.drop(index=cluster.index)
                clusters         = pd.concat([clusters,cluster],axis=0)

            cl_ids = npr.randint(0,K,size=2)
            sample = clusters[clusters.CL_ID.isin(cl_ids)]
            return sample

    def weighted_sampling(self,n):
            # Weighted Sampling takes into account the ratio of the types of observations in the population
            # and generates an unbiased sample in similar pattern.
            avg             = sum(self.df['SALARY'])/len(self.df)
            df              = self.df
            df['SAL_SLAB']  = np.where(df['SALARY'] < avg,0,1)

            def group_weights(x):
                weight      = int(np.rint(n * len(x[x.SAL_SLAB != 0]) / len(df[df.SAL_SLAB != 0])))
                sample_df   = x.sample(weight).reset_index(drop=True)
                return (sample_df)

            sample          = df.groupby('DEPARTMENT_ID').apply(group_weights)
            print(sample['DEPARTMENT_ID'].value_counts())
            sample          = sample.drop(['SAL_SLAB','DEPARTMENT_ID'],axis=1)
            
            return sample

    def stratified_sampling(self,n):
            # Stratified sampling generate stratas(clusters) based on a specific characteristic, in the 
            # population and randomly extract one or more stratas into sample. Can be used given the 
            # required information prior.
            N               = len(self.df)
            avg             = sum(self.df['SALARY'])/len(self.df)
            df              = self.df
            df['SAL_SLAB']  = np.where(df['SALARY'] < avg,0,1)

            def weighted_sample():
                def group_weights(x):
                    weight      = int(np.rint(n * len(x[x.SAL_SLAB != 0]) / len(df[df.SAL_SLAB != 0])))
                    sample_df   = x.sample(weight)
                    return (sample_df)

                sample          = df.groupby('DEPARTMENT_ID').apply(group_weights)
                return sample

            stratas         = None
            K               = int(N/n)
            for i in range(K):
                cluster          = weighted_sample().reset_index(drop=True)
                cluster["CL_ID"] = np.repeat(i,len(cluster))
                stratas          = pd.concat([stratas,cluster],axis=0)
                df.drop(index=cluster.index)

            cl_ids          = npr.randint(0,K,size=2)
            sample          = stratas[stratas.CL_ID.isin(cl_ids)]
            sample          = sample.drop(['SAL_SLAB',"CL_ID"],axis=1)
            return sample


if __name__=="__main__":
    data_path = 'D://Download//employees.csv'
    obj       = Data_sampling(data_path)
    sampl_len = 10

    sample = obj.random_sampling(sampl_len)
    print("\n Random sampling: \n",sample)

    sample = obj.systematic_sampling(sampl_len)
    print("\n Systematic sampling: \n",sample)

    sample = obj.clustered_sampling(int(sampl_len/2))
    print("\n Clustered sampling: \n",sample)

    sample = obj.weighted_sampling(sampl_len)
    print("\n Weighted sampling: \n",sample)

    sample = obj.stratified_sampling(sampl_len)
    print("\n Stratified sampling: \n",sample,"\n")

# Referred links
#       https://towardsdatascience.com/data-sampling-methods-in-python-a4400628ea1b