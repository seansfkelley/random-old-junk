# For a given sum n, number of squares sq, maximum single value mx, compute all the possible
# different sums up to n without repeats.
def additions(n, sq, mx, exceptions = None):
    solutions = []
    additions_helper(n, sq, [mx], solutions)
    if exceptions is not None:
        exceptions = set(exceptions)
        solutions = filter(lambda x: len(exceptions & set(x)) == 0, solutions)
    print solutions

def additions_helper(n, sq, cur, solutions):
    mx = cur.pop()
    if n == 0 and sq == 0:
        solutions.append(cur)
    if n < 0 or sq < 0:
        return
    for i in xrange(min(mx, n), 0, -1):
        additions_helper(n - i, sq - 1, cur + [i, i], solutions)
