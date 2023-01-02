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

minlength = 2382	# minimum postprocessed array length.
skip_subject = ['34']
_phaseDifPairKey_simDataVal_dict = {}
lengths = []

proc_dataset_folder = 'EMG_data_for_gestures-processed'
if not(os.path.isdir(proc_dataset_folder)):
	os.mkdir(proc_dataset_folder)

# --- reading raw data ---------------------

raw_subject_data = os.listdir('EMG_data_for_gestures-master')
raw_subject_data.sort()
raw_subject_data = raw_subject_data[:-1]

# reading data folder for each subject.

for subject in raw_subject_data:

	if subject not in skip_subject:

		print('subject: ', subject)

		_X = []	# average of all channels (single time series)
		_Y = []	# gesture label

		# creating subject's data destination folder for postproc. data
		
		if not(os.path.isdir(os.path.join(proc_dataset_folder, subject))):
			os.mkdir(os.path.join(proc_dataset_folder, subject))

		# opening subjects data.txt

		rawSubjectData_path = os.path.join(
			'EMG_data_for_gestures-master',
			subject)

		raw_txt_data = os.listdir(rawSubjectData_path)
		raw_txt_data.sort()

		# reading subjects data.txt

		for txtData in raw_txt_data:

			file = os.path.join(
				rawSubjectData_path,
				txtData)

			sim_data_txt = open(file, 'r')
			lines = sim_data_txt.readlines()
			lin_count = 0

			_data_header = []
			_data_matrix = []

			for line in lines:

				if lin_count > 0:

					_ = [float(i) for i in line.replace('\n', '').split('\t')]

					_data_matrix.append(_)

				else:

					_data_header = line.replace('\n', '').split('\t')

				lin_count += 1

			_labels = list(set(list(list(zip(*_data_matrix))[-1])))
			_labels.remove(0.0)

			_data_per_label = {}

			for label in _labels:

				_data_per_label[label] = []

			for i in range(0, len(_data_matrix)):

				if _data_matrix[i][-1] != 0:

					_l = _data_matrix[i][-1]
					_d = _data_matrix[i][1:-1]

					_data_per_label[_l].append(_d)

			# merging channels (single time series) per gesture 

			for label, channels_data in _data_per_label.items():

				mean = []

				for i in range(0, len(channels_data[0])):

					mean.append(
						list(list(zip(*channels_data))[i]))

				_i = np.mean(mean, axis = 0) - np.min(np.mean(mean, axis = 0))

				_j = np.max(np.mean(mean, axis = 0)) - np.min(np.mean(mean, axis = 0))

				_normalizedChannelAvrageGesture = _i/_j

				lengths.append(len(_normalizedChannelAvrageGesture))

				_X.append(_normalizedChannelAvrageGesture[0:minlength])
				_Y.append(label)

			_gests = list(set(_Y))
			_gests.sort()

			_postProcessedData = {
			'subject': subject,
			'gestures': _gests,
			'X': _X,
			'Y': _Y
			}

			# saving postprocessed data to file

			fn = os.path.join(
				proc_dataset_folder, 
				subject,
				'EMG_{}-merged_channel_per_gesture.pickle'.format(subject))

			with open(fn, 'wb') as f:
				pickle.dump(_postProcessedData, f)

print('min. length: ', np.min(lengths))