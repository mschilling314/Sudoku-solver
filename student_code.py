import common

#helpful, but not needed
class variables:
	counter=0


def complete(sudoku):
	res = True
	for y in range(9):
		for x in range(9):
			if sudoku[y][x] == 0:
				res = False
	return res


def BT(sudoku):
	variables.counter += 1
	if complete(sudoku):
		return True
	for y in range(9):
		for x in range(9):
			if sudoku[y][x] == 0:
				for v in range(1, 10):
					if common.can_yx_be_z(sudoku, y, x, v):
						sudoku[y][x] = v
						r = BT(sudoku)
						if r == True:
							return True
						sudoku[y][x] = 0
				return False


def create_domain(sudoku):
	res = []
	for y in range(9):
		to = []
		for x in range(9):
			ti = []
			for v in range(1, 10):
				if common.can_yx_be_z(sudoku, y, x, v) or sudoku[y][x] == v:
					r = 1
				else:
					r = 0
				ti.append(r)
			to.append(ti)
		res.append(to)
	return res


def update_domain(loc, val, dom):
	res = dom
	y = loc[0]
	x = loc[1]
	v = val-1
	for i in range(9):
		res[y][i][v] = 0
		res[i][x][v] = 0
		res[(y//3)*3+(i//3)][(x//3)*3 + i%3][v] = 0
	res[y][x][v] = 1
	return res


def no_empty_domain(dom):
	# iterate over the entire board
	for y in range(9):
		for x in range(9):
			# counter, if it's ever 9 a domain is empty
			nozeros = 0
			# given the loc, check every v
			for v in range(9):
				# check to see if the domain value is 0
				if dom[y][x][v] == 0:
					# increment our counter
					nozeros += 1
			# if we have an empty domain return False
			if nozeros == 9:
				return False
	return True


def print_domain(dom):
	for v in range(9):
		print(f'V={v+1}\n')
		for y in range(9):
			temp = []
			for x in range(9):
				temp.append(dom[y][x][v])
			print(temp)
		print('\n\n')


def domain_copy(dom):
	res = []
	for y in range(9):
		to = []
		for x in range(9):
			ti = []
			for v in range(9):
				ti.append(dom[y][x][v])
			to.append(ti)
		res.append(to)
	return res


def FC(sudoku, domain):
	variables.counter += 1
	# check to see if the game is over
	if complete(sudoku):
		return True
	# iterate over the entire board
	for y in range(9):
		for x in range(9):
			# check to ensure the board is empty
			if sudoku[y][x] == 0:
				for v in range(1, 10):
					# if our move is valid then make it
					if common.can_yx_be_z(sudoku, y, x, v):
						# make a copy of our domain, jic we need to back up
						old_domain = domain_copy(domain)
						# update the value of the sudoku board
						sudoku[y][x] = v
						# update the domain
						domain = update_domain([y, x], v, domain)
						# by default the recursion fails
						r = False
						# check to see if the domain is empty
						if no_empty_domain(domain):
							# if there isn't an empty domain, recurse
							r = FC(sudoku, domain)
						# check to see if we've succeeded
						if r == True:
							# if the result of our recursion is true, return it
							return True
						# since our recursion failed, undo our move
						sudoku[y][x] = 0
						domain = domain_copy(old_domain)
				# our move wasn't valid, so sucks to suck
				return False


def print_board(board):
	print()
	for y in range(9):
		print(board[y])
	print()


def sudoku_backtracking(sudoku):
	variables.counter = 0
	#put your code here
	BT(sudoku)
	return variables.counter

def sudoku_forwardchecking(sudoku):
	#print_board(sudoku)
	variables.counter = 0
	#put your code here
	domain = create_domain(sudoku)
	FC(sudoku, domain)
	return variables.counter
