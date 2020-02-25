'''
Performs principal component analysis (PCA) on continuous parameters,
given discrete-sliced sample set.
'''

from ATE import UniformSamplingStrategy, Domain, Samplerun, data_utils
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


def test_pca():
    '''
    Sets up uniform generation of data points and csv output.
    '''
    
    fpath = "output/100fix0000000out.csv"
    # load dataset into Pandas DataFrame
    df = pd.read_csv(fpath)
    
    # separate out cont and disc features, and target
    c, d, y = data_utils.c_d_y_split(df)

    # construct pca space consisting of continuous features and target
    cy = pd.concat([c, y[['tbr']]], axis = 1)
    numcomp = cy.columns.values.size
    cy = StandardScaler().fit_transform(cy)

    pca = PCA(n_components=numcomp)
    principalComponents = pca.fit_transform(cy)
    principalDf = pd.DataFrame(data = principalComponents, 
					           columns = ['pc1', 'pc2', 'pc3', 'pc4',
					                      'pc5', 'pc6', 'pc7', 'pc8',
					                      'pc9', 'pc10','pc11','pc12',
					                      'pc13'])

    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)
    ax.scatter(principalDf['pc1']
               , principalDf['pc2']
               , s = 50)
    ax.grid()	                    
    fig.savefig('pca_plot.jpg')
    
    print(pca.explained_variance_ratio_)

if __name__ == '__main__':
    test_pca()
