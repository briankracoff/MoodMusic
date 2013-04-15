import marsyas
from itertools import izip_longest, izip
from collections import namedtuple
import math

from data.DB_Helper import *

# Notes:
# No beat features

msm = marsyas.MarSystemManager()

def to_list(realvec):
	cols = realvec.getCols()
	rows = realvec.getRows()

	return [[realvec[r*cols + c] for c in range(cols)] for r in range(rows)]

def get_control(msys, type, name):
	func = 'to_' + type
	type = 'mrs_' + type

	return getattr(msys.getControl(type + '/' + name), func)()

def obs_names(msys):
	return [attr for attr in get_control(msys, 'string', 'onObsNames').split(',')
	             if attr]

def create(spec):
	if isinstance(spec, str):
		return msm.create(spec)

	msys = msm.create(spec['name'])

	if 'child' in spec and 'children' in spec:
		raise RuntimeError

	children = []
	if 'child' in spec:
		children = [spec['child']]
	elif 'children' in spec:
		children = spec['children']

	for child in children:
		msys.addMarSystem(create(child))

	if 'links' in spec:
		for src, dst in spec['links'].iteritems():
			if isinstance(src, tuple):
				src = '/'.join(src)
			if isinstance(dst, tuple):
				dst = '/'.join(dst)

			msys.linkControl(src, dst)

	if 'controls' in spec:
		it = spec['controls']
		if isinstance(it, dict):
			it = it.iteritems()

		for ctrl, val in it:
			msys.updControl(ctrl, val)

	return msys

def grouper(n, iterable, fillvalue=None):
	'Collect data into fixed-length chunks or blocks'
	# grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
	args = [iter(iterable)] * n
	return izip_longest(fillvalue=fillvalue, *args)

MarSysDesc = namedtuple('MarSysDesc', 'type name')

def reset_msys(msys):
	for path, ctrl in msys.getControls().iteritems():
		path = [MarSysDesc(type, name) for type, name in grouper(2, path.split('/'))]

		if path[-2].type in ('ShiftInput', 'Flux', 'Memory') and \
		   path[-1].type == 'mrs_bool' and path[-1].name == 'reset':
			ctrl.setValue_bool(True)

net_spec = {
	'name': 'Series/bextractNetwork',
	'controls': {
		'mrs_real/israte': 44100.0,
	},
	'links': {
		'mrs_string/filename': ('SoundFileSource/src',
		                        'mrs_string/filename'),
		'mrs_bool/hasData': ('SoundFileSource/src',
		                     'mrs_bool/hasData'),
		'mrs_natural/channels': ('SoundFileSource/src',
		                         'mrs_natural/onObservations')
	},
	'children': [
		'SoundFileSource/src',
		{
			'name': 'Fanout/timbrepanning',
			'children': [
				{
					'name': 'Series/monotimbre',
					'children': [
						'Stereo2Mono/s2m',
						{
							'name': 'TimbreFeatures/featExtractor',
							'controls': [
								# All the features!
								('mrs_string/enableSPChild', 'Series/chromaPrSeries'),
								('mrs_string/enableSPChild', 'MFCC/mfcc'),
								('mrs_string/enableSPChild', 'SFM/sfm'),
								('mrs_string/enableSPChild', 'SCF/scf'),
								('mrs_string/enableSPChild', 'Rolloff/rlf'),
								('mrs_string/enableSPChild', 'Flux/flux'),
								('mrs_string/enableSPChild', 'Centroid/cntrd'),
								('mrs_string/enableLPCChild', 'Series/lspbranch'),
								('mrs_string/enableLPCChild', 'Series/lpccbranch'),
								('mrs_string/enableTDChild', 'ZeroCrossings/zcrs')
							]
						}
					]
				},
				'StereoPanningSpectrumFeatures/SPSFeatures'
			]
		}
	]
}

msys = create(net_spec)
reset_msys(msys)

# Disgusting hack to get the observation names to look like they
# would with a stereo audio file.
msys.getControl('SoundFileSource/src/mrs_natural/onObservations').setValue_natural(2)
msys.getControl('SoundFileSource/src/mrs_string/onObsNames').setValue_string('AudioCh0,AudioCh1,')
msys.getChildMarSystem('SoundFileSource/src').update() # WHY IS THIS NECESSARY AAAAAAAAA

attributes = obs_names(msys)

attribute_schema = []
for attr in attributes:
	attribute_schema.append(FieldInfo('mean_' + attr, 'REAL'))
	attribute_schema.append(FieldInfo('stdev_' + attr, 'REAL'))

def song_attributes(filename, verbose=True, db=None):
	if db is None:
		db = DB_Helper()

	if db.is_in_db(filename):
		return

	msys.updControl('mrs_string/filename', filename)
	if not get_control(msys, 'bool', 'hasData'):
		raise RuntimeError('It looks like Marsyas was unable to load your file! '
		                   'Make sure you have the right codec support enabled.')

	# The StereoPanningSpectrumFeatures will only work
	# correctly with two channels.
	if get_control(msys, 'natural', 'channels') == 2:
		chan_control = 'enableChild'
	else:
		chan_control = 'disableChild'

	msys.updControl('Fanout/timbrepanning/mrs_string/' + chan_control,
	                'StereoPanningSpectrumFeatures/SPSFeatures')

	observations = get_control(msys, 'natural', 'onObservations')

	sum_vals = [0] * observations
	sum_of_squares = [0] * observations
	count = 0
	while get_control(msys, 'bool', 'hasData'):
		msys.tick()

		vals = get_control(msys, 'realvec', 'processedData')
		sum_vals = [old + new for old, new in izip(sum_vals, vals)]
		sum_of_squares = [old + new**2 for old, new in izip(sum_of_squares, vals)]
		count += 1

	reset_msys(msys)

	out = {field.name: None for field in attribute_schema}

	for i, attr in enumerate(obs_names(msys)):
		avg = sum_vals[i] / count
		squares_avg = sum_of_squares[i] / count

		out['mean_' + attr] = avg
		out['stdev_' + attr] = math.sqrt(squares_avg - avg**2)

	out[commonPath] = filename
	out[commonArtist] = None
	out[commonTitle] = None

	db.add_song(out)
