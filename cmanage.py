""" C-Manage 42 projects (written by Philipp Rollinger)
use inside a project folder with a project file
>>> python3 cmanage.py add <function_file_name.c>
    => creates files for code, test & readme
>>> python3 cmanage.py run <receipt_name> <optional parameter>
	=> runs a receipt from the _project.py definitions

>>> python3 cmanage.py run norm <file_name>|ALL
>>> python3 cmanage.py run test <file_name>|ALL
>>> python3 cmanage.py run commit <file_name>
>>> python3 cmanage.py run test external <path/to/other/repo>
"""
import os, sys, subprocess
import importlib.util
from string import Template

cmanage_directory = os.path.dirname(os.path.realpath(__file__))
current_working_directory = os.getcwd()

def prepare_bash_commands(receipt_definition, manage_parameters):
	parameters = {'PARAM_{}'.format(i): x for i,x in enumerate(manage_parameters)}
	receipt_definition.update(parameters)
	runner = {
		'prepare': Template(receipt_definition['prepare']).substitute(receipt_definition),
		'run': Template(receipt_definition['run']).substitute(receipt_definition),
		'cleanup': Template(receipt_definition['cleanup']).substitute(receipt_definition),
	}
	return runner

print("=== Manage 42 C - Projects === \t(%s)"%(current_working_directory))

spec = importlib.util.spec_from_file_location("module.name", "%s/_project.py"%(current_working_directory))
project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(project)
#print(project.CONFIG); exit(0);

command = sys.argv[1] if len(sys.argv) >= 2 else None
param_1 = sys.argv[2] if len(sys.argv) >= 3 else None

if command == "add" and param_1:
	#>>> python3 cmanage.py add <function_file_name>
	#=> creates files for code, test & readme
	substitutions = {
		'filename':param_1,
		'name':param_1.replace(".c", ""),
	}
	print("Adding function file %s to project..."%(substitutions['filename']))
	# Function File
	function_file_path = '%s/%s/%s' % (current_working_directory, project.CONFIG['src_folder'], substitutions['filename'])
	if not os.path.isfile(function_file_path):
		with open('%s/function_file.txt'%(cmanage_directory), 'r') as f1:
		    src = Template(f1.read())
		    result = src.substitute(substitutions)
		with open(function_file_path, 'w') as f2:
			f2.write(result)
	# Test File
	#test_file_path = '%s/%s/test_%s' % (current_working_directory, project.CONFIG['test_folder'], substitutions['filename'])
	#if not os.path.isfile(test_file_path):
	#	with open('%s/test_file.txt'%(cmanage_directory), 'r') as f1:
	#	    src = Template(f1.read())
	#	    result = src.substitute(substitutions)
	#	with open(test_file_path, 'w') as f2:
	#		f2.write(result)
	exit()
elif command == "run":
	# RUN RECEIPT:
	#>>> python3 cmanage.py run <receipt_name> <optional parameter>
	#=> runs a receipt from the _project.py definitions
	if param_1 in project.CONFIG['receipts'].keys():
		runner = prepare_bash_commands(project.CONFIG['receipts'][param_1], sys.argv)
		print("RUN: %s" % (param_1) )
		if runner['prepare']:
			print(runner['prepare'])
			os.system(runner['prepare'])
		if runner['run']:
			print(runner['run'])
			os.system(runner['run'])
		if runner['cleanup']:
			print(runner['cleanup'])
			os.system(runner['cleanup'])
	else:
		print("UNKNOWN Receipt: %s\nUSE: %s" % (param_1, project.CONFIG['receipts'].keys()) )
	exit()
