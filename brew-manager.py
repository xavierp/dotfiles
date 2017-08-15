#!/usr/bin/env python
# coding: utf8

import argparse;
import json;
import subprocess


def current_taps():
	"""
	Retrieve tapped repositories.

    Returns
    -------
    list
        List of taps
	"""
	try:
		# Execute cmd: `brew tap-info --json=v1 --installed`
		# More info: `brew help tap-info`
		output = subprocess.check_output(['brew', 'tap-info', '--json=v1', '--installed']);
	except subprocess.CalledProcessError as e:
		print 'Error while reading current brew taps.';
	
	return [t['name'] for t in json.loads(output) if t['installed']];


def current_formulas():
	"""
	Retrieve currently installed formulas.

    Returns
    -------
    list
        List of formulas
	"""
	try:
		# Execute cmd: `brew leaves` which displays
		# More info: `man brew`
		output = subprocess.check_output(['brew', 'leaves']);
	except subprocess.CalledProcessError as e:
		print 'Error while reading current installed formulas.';
	
	return [f for f in output.split('\n') if f != ''];

def current_casks():
	"""
	Retrieve currently installed casks.

	This requires `brew casks to be installed` !

    Returns
    -------
    list
        List of casks
	"""
	try:
		# Execute cmd: `brew cask list -1`
		# More info: `man brew-cask`
		output = subprocess.check_output(['brew', 'cask', 'list', '-1']);
	except subprocess.CalledProcessError as e:
		print 'Error while reading current installed casks.';
	
	return [c for c in output.split('\n') if c != ''];


def update_db(db):
	"""
	Update database file.

    Parameters
    ----------
    db : string
        Path to database file, must be json formated.
	"""
	data = {
		'taps': current_taps(),
		'formulas': current_formulas(),
		'casks': current_casks()
	}
	
	with open(db, 'w') as f:
		f.write(json.dumps(data, f, indent=4));

	print 'Database updated.';


def install(db):
	"""
	Install everything.

	Tap repositories, install formulas and casks
	defined in database file.
	Already tapped or installed items are skipped.

    Parameters
    ----------
    db : string
        Path to database file, must be json formated.
	"""
	with open(db, 'r') as f:
		data = json.loads(f.read());

	installed_taps = current_taps();
	installed_formulas = current_formulas();
	installed_casks = current_casks();
	taps = [t for t in data['taps'] if t not in installed_taps];
	formulas = [f for f in data['formulas'] if f not in installed_formulas];
	casks = [c for c in data['casks'] if f not in installed_casks];

	for t in taps:
		print 'tapping %s' % t;
		subprocess.check_call(['brew', 'tap', t]);

	for f in formulas:
		print 'installing %s' % f;
		subprocess.check_call(['brew', 'install', f]);

	for c in casks:
		print 'installing cask %s' % c;
		subprocess.check_call(['brew', 'cask','install', c]);

	print 'All missing taps, formulas and casks have been installed.';



actions = {
	'update-db': update_db,
	'install': install,
}

parser = argparse.ArgumentParser(description='Manager for brew/casks packages');
parser.add_argument('--database', '-db', type=str, default='brew-packages.json',
                    help='Brew manager database', metavar='file');
parser.add_argument('action', type=str, choices=actions.keys(),
					help= 'Desired action. '
					      'update-db: update database file. '
					      'install: install taps, formulas and packages from database file');
args = parser.parse_args();
actions[args.action](args.database);

