#   
#   This program trains a binary classifer to recognize a numeric digit.
#   The number of features chosen to feed the classifier is denoted by the variable k.
#   The features are chosen from the picture size recieved. For the training of this classifier, the
#   picture size is 784 pixels x 784 pixels, which is 784*784 features. Because of the large feature size
#   the data, i.e. pictures, will be reduced in dimension using PCA. The number of dimensions to reduce to will
#   also be denoted by the variable k. The total number of samples used is denoted by variable n.
#
import numpy as np
from sklearn import svm

# find the data from a file on the computer
# I assume the data is in a .csv file
data_name = 'data_MNIST56.csv'
labels_name = 'labels_MNIST56.csv'
images = np.genfromtxt(
        data_name,   # file name, should replace with data_name
        skip_header= 0,    # lines to skip at the top
        skip_footer= 0,    # lines to skip at the bottom
        delimiter = ",",    # column delimiter
        dtype = 'int',    # data type
        filling_values = 0    # fill missing values with 0
    )
labels = np.genfromtxt(
    labels_name,   # file name, should replace with labels_name
    skip_header= 0,    # lines to skip at the top
    skip_footer= 0,    # lines to skip at the bottom
    delimiter = ",",    # column delimiter
    dtype = 'int',    # data type
    filling_values = 0    # fill missing values with 0
)
print('data shape: {0}'.format(images.shape))
print('labels shape: {0}'.format(labels.shape))

# using data, perform PCA to reduce dimensions from d --> k
# current data size: nxd  -->  reduced data size: nxk
# To do this, the method of Singular Value Decomposition (SVD) is used
sigma = np.dot(images.T, images)
print('covariance matrix shape: {0}'.format(sigma.shape))

# choose the reduced dimension size
k = 100

# using the covariance matirx sigma execute the method of SVD
U,S,V = np.linalg.svd(sigma, full_matrices =True)
print('U shape: {0}'.format(U.shape))
print('S shape: {0}'.format(S.shape))
print('V shape: {0}'.format(V.shape))

# reduce the U matrix from (dxd) --> (dxk)
U_reduc = U[:,:k]
print('U_reduc shape: {0}'.format(U_reduc.shape))

# reduce the dimensions of the data from (nxd) --> (nxk)
images_reduc =np.dot(images, U_reduc)
print('images_reduc shape: {0}'.format(images_reduc.shape))

# using the reduced features of the data and the corresponding labels, train the classifier
labels_r = np.ravel(labels)
clf = svm.SVC(gamma = 0.1, C = 10)
clf.fit(images_reduc, labels_r)

# test the classifier
# test values that it has already learned
for i in range(10):
    print("Correct value: ", labels[i+5000])
    x_samp = images_reduc[i+5000,:]
    x_samp = x_samp.reshape(1,-1)
    predict = clf.predict(x_samp)
    print("Predicted value: ", predict)
    print()
