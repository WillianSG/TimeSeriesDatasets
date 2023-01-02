# -*- coding: utf-8 -*-
"""
@author: w.soares.girao@rug.nl
@university: University of Groningen
@group: Bio-Inspired Circuits and System
"""

# import setuptools
import os, sys, pickle
import numpy as np
import matplotlib.pyplot as plt

# --- local variables ---------------------

mainFolder = 'EMG_data_for_gestures-processed'

skip_subject = ['34']
gestureList = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]

_trainingSubjects = ['0{}'.format(i) if len(str(i)) == 1 else str(i) for i in range(1, 31)]

_testingSubjects = ['0{}'.format(i) if len(str(i)) == 1 else str(i) for i in range(31, 37)]
_testingSubjects.remove(skip_subject[0])

processedSubjectData = os.listdir(mainFolder)
processedSubjectData.sort()
processedSubjectData = processedSubjectData[:-1]

_X_training = []
_Y_training = []

_X_testing = []
_Y_testing = []

# --- generaring unit dataset ---------------------

# reading data folder for each subject.

for subject in processedSubjectData:

	subjectFilePath = os.path.join(
		mainFolder,
		subject,
		'EMG_{}-merged_channel_per_gesture.pickle'.format(subject))

	# saparating data into training and testing datapoints.

	"""
	subjectDataDict = {
		'subject': subject,
		'gestures': _gests,
		'X': _X,
		'Y': _Y
	}
	"""
	with open(subjectFilePath,	'rb') as f:(
		subjectDataDict) = pickle.load(f)

	if subject in _trainingSubjects:					# training

		for i in range(0, len(subjectDataDict['Y'])):

			if subjectDataDict['Y'][i] in gestureList:

				_Y_training.append(subjectDataDict['Y'][i])
				_X_training.append(subjectDataDict['X'][i])

	elif subject in _testingSubjects:					# testing

		for i in range(0, len(subjectDataDict['Y'])):

			if subjectDataDict['Y'][i] in gestureList:

				_Y_testing.append(subjectDataDict['Y'][i])
				_X_testing.append(subjectDataDict['X'][i])

	else:

		pass

print('training (# datapoints):',  len(_Y_training))
print('testing (# datapoints):',  len(_Y_testing))

outputFile = 'training_{}-testing_{}-EMG_dataset.pickle'.format(
	len(_Y_training),
	len(_Y_testing))

with open(outputFile, 'wb') as f:
	pickle.dump(
		{
		'X_training': _X_training,
		'Y_training': _Y_training,
		'X_testing': _X_testing,
		'Y_testing': _Y_testing
		}
		, f)