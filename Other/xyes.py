import sys


def xyes(remaining_runs = -1):
	# Get all but first argument, which is the file name itself
	args = sys.argv[1:]

	# If limit was passed, set remaining cycles to 20
	if len(args) > 0 and args[0] == '-limit':
		# Set limit
		remaining_runs = 20
		# Drop off -limit
		args = args[1:]

	# If no arguments follow, use "hello world"
	if len(args) > 0:
		to_print = ' '.join(args)
	else:
		to_print = 'hello world'

	# Run so long as we have a positive # of remaining runs
	while remaining_runs != 0:
		# Print concatenated string
		print(to_print)

		# If have positive remaining runs, subtract
		if remaining_runs > 0:
			# Subtract one
			remaining_runs -= 1
