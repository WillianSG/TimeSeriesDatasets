# -*- coding: utf-8 -*-
"""
@author: w.soares.girao@rug.nl
@university: University of Groningen
@group: Bio-Inspired Circuits and System
"""

# import setuptools
from sklearn import svm
import os, sys, pickle
import numpy as np

# --- local variables ---------------------

_dataset = 'training_360-testing_48-EMG_dataset.pickle'
_kernel = str(sys.argv[1])

# --- loading dataset ---------------------

"""
_EMGdataset = {
	'X_training': _X_training,
	'Y_training': _Y_training,
	'X_testing': _X_testing,
	'Y_testing': _Y_testing
}
"""
with open(_dataset,	'rb') as f:(
	_EMGdataset) = pickle.load(f)

# --- train model -------------------------

clf = svm.SVC(kernel = _kernel)
clf.fit(
	_EMGdataset['X_training'], 
	_EMGdataset['Y_training'])

# --- test model --------------------------

correct = 0

for i in np.arange(len(_EMGdataset['X_testing'])):

	pred = clf.predict([_EMGdataset['X_testing'][i]])[0]

	print('predicted / true: {} / {}'.format(
		pred, _EMGdataset['Y_testing'][i]))

	if pred == _EMGdataset['Y_testing'][i]:

		correct += 1

CR = np.round((correct/len(_EMGdataset['X_testing'])), 3)

print('\nCR ({} kernel): {}'.format(_kernel, CR))