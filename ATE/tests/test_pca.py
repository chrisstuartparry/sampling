'''
Performs principal component analysis (PCA) on continuous parameters,
given discrete-sliced sample set.
'''

from ATE import UniformSamplingStrategy, Domain, Samplerun
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def test_pca():
    '''
    Sets up uniform generation of data points and csv output.
    '''
    
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
	# load dataset into Pandas DataFrame
    df = pd.read_csv(url, names=['sepal length','sepal width' ,'petal length','petal width','target'])

    features = ['sepal length', 'sepal width', 'petal length', 'petal width']
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:,['target']].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)

    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data = principalComponents, 
					           columns = ['principal component 1', 'principal component 2'])
    finalDf = pd.concat([principalDf, df[['target']]], axis = 1)

    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)
    targets = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
    colors = ['r', 'g', 'b']
    for target, color in zip(targets,colors):
        indicesToKeep = finalDf['target'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
                   , finalDf.loc[indicesToKeep, 'principal component 2']
                   , c = color
                   , s = 50)
    ax.legend(targets)
    ax.grid()	                    
    fig.savefig('pca_plot.jpg')
    
    print(pca.explained_variance_ratio_)

if __name__ == '__main__':
    test_pca()
