# -*- coding: utf-8 -*-
"""
@author: w.soares.girao@rug.nl
@university: University of Groningen
@group: Bio-Inspired Circuits and System
"""

# import setuptools
import os, sys
import numpy as np
import matplotlib.pyplot as plt

subject = sys.argv[1]
gesture = int(sys.argv[2])

# --- local variables ---------------------

_phaseDifPairKey_simDataVal_dict = {}

# --- reading raw data ---------------------

# root = os.path.dirname(os.path.abspath(os.path.join(__file__ ,  '../..')))

raw_data_folders_path = os.path.join(
	'EMG_data_for_gestures-master',
	subject)

raw_txt_data = os.listdir(raw_data_folders_path)
raw_txt_data.sort()

file = os.path.join(
	raw_data_folders_path,
	raw_txt_data[0])

sim_data_txt = open(file, 'r')
lines = sim_data_txt.readlines()
lin_count = 0

_data_header = []
_data_matrix = []

for line in lines:

	if lin_count > 0:

		_ = [float(i) for i in line.replace('\n', '').split('\t')]

		if int(_[-1]) == gesture:

			_data_matrix.append(_)

	else:

		_data_header = line.replace('\n', '').split('\t')

	lin_count += 1

for i in range(1, len(_data_header)-6):

	x_ = np.arange(
		0, 
		len(list(list(zip(*_data_matrix))[i])),
		1)

	plt.plot(x_, list(list(zip(*_data_matrix))[i]), 
		lw = 1.0,
		label = _data_header[i])

	plt.legend(loc = 'best', framealpha = 0.0)

plt.show()
plt.close()

mean = []

for i in range(1, len(_data_header)-1):

	mean.append(
		list(list(zip(*_data_matrix))[i]))

x_ = np.arange(
	0, 
	len(np.mean(mean, axis = 0)),
	1)

_ = np.mean(mean, axis = 0)/np.max(np.mean(mean, axis = 0))

plt.plot(x_, _, 
	lw = 1.0, color = 'k')

plt.title('gesture # {}'.format(gesture))

plt.show()
plt.close()