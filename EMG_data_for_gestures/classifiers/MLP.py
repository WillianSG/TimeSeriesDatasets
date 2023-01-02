# -*- coding: utf-8 -*-
"""
@author: w.soares.girao@rug.nl
@university: University of Groningen
@group: Bio-Inspired Circuits and System
"""

# import setuptools
from sklearn.neural_network import MLPClassifier
import os, sys, pickle
import numpy as np

# --- local variables ---------------------

_CR = []
_dataset = 'training_360-testing_48-EMG_dataset.pickle'

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

for i in range(1):

	# --- train model -------------------------

	clf = MLPClassifier(
		solver = 'lbfgs', 
		alpha = 1e-5,
		hidden_layer_sizes = (200, 100),
		max_iter = 1000)

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

	_CR.append(np.round((correct/len(_EMGdataset['X_testing'])), 3))

print('\nCR: {}/{}'.format(
	np.round(np.mean(_CR), 3),
	np.round(np.std(_CR), 3)))