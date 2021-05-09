import time


def print_elapsed_time(func):
	def measure(*args, **kwargs):
		start = time.perf_counter()
		result = func(*args, **kwargs)
		print('Done in {:.4f} seconds'.format(time.perf_counter() - start))
		return result
	return measure
