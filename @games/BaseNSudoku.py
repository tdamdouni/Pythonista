BASE = 9
BLOCK_HEIGHT = 3
BLOCK_WIDTH = 3

field = [
[1, 2, 3, 4, 5, 6, 7, 8, 9],
[4, 5, 6, 7, 8, 9, 1, 2, 3],
[7, 8, 9, 1, 2, 3, 4, 5, 6],
[2, 3, 4, 5, 6, 7, 8, 9, 1],
[5, 6, 7, 8, 9, 1, 2, 3, 4],
[8, 9, 1, 2, 3, 4, 5, 6, 7],
[3, 4, 5, 6, 7, 8, 9, 1, 2],
[6, 7, 8, 9, 1, 2, 3, 4, 5],
[9, 1, 2, 3, 4, 5, 6, 7, 8]
]

def precheck():
    # Step 0: Pre-solve consistency checks
    global BASE, BLOCK_HEIGHT, BLOCK_WIDTH, field
    try:
        BASE = int(BASE)
    except Exception as err:
        err.message = "Failed to convert BASE ({}) to int: ".format(BASE) + err.message
        raise

    global BASE_RANGE
    BASE_RANGE = range(1, BASE+1)

    try:
        BLOCK_HEIGHT = int(BLOCK_HEIGHT)
    except Exception as err:
        err.message = "Failed to convert BLOCK_HEIGHT ({}) to int: ".format(BLOCK_HEIGHT) + err.message
        raise

    try:
        BLOCK_WIDTH = int(BLOCK_WIDTH)
    except Exception as err:
        err.message = "Failed to convert BLOCK_WIDTH ({}) to int: ".format(BLOCK_WIDTH) + err.message
        raise

    if BLOCK_HEIGHT * BLOCK_WIDTH != BASE:
        raise ValueError("Block size ({} by {}) does not match number base ({})".format(BLOCK_WIDTH, BLOCK_HEIGHT, BASE))

    try:
        field = list(field)
    except Exception as err:
        err.message = "Failed to convert field ({}) to list: ".format(field) + err.message
        raise

    if len(field) != BASE:
        raise ValueError("Field height ({}) is not equal to number base ({})".format(len(field), BASE))

    if len(field) % BLOCK_HEIGHT != 0:
        raise ValueError("Field height ({}) is not divisible by block height ({})".format(len(field), BLOCK_HEIGHT))

    for y, row in enumerate(field):
        try:
            field[y] = list(row)
        except Exception as err:
            err.message = "Failed to convert row {} ({}) to list: ".format(y, row) + err.message

        if len(row) != BASE:
            raise ValueError("Width of row {} ({}) is not equal to number base ({})".format(i, len(row), BASE))

        if len(row) % BLOCK_HEIGHT != 0:
            raise ValueError("Width of row {} ({}) is not divisible by block height ({})".format(i, len(row), BLOCK_HEIGHT))

        for x, cell in enumerate(row):
            try:
                field[y][x] = int(cell)
            except Exception as err:
                err.message = "Failed to parse cell {} in row {} ({}) as int: ".format(x, y, cell) + err.message
                raise

            if not 0 <= cell <= BASE:
                raise ValueError("Cell {} in row {} ({}) must be greater than 0 and less than {}".format(x, y, cell, BASE))

        for n in BASE_RANGE:
            if row.count(n) > 1:
                raise ValueError("Number {} appears more than once in row {}".format(n, y))

    for x, col in enumerate(zip(*field)):
        for n in BASE_RANGE:
            if col.count(n) > 1:
                raise ValueError("Number {} appears more than once in column {}".format(n, x))

    for y in range(BASE / BLOCK_HEIGHT):
        rows = field[BLOCK_HEIGHT*y:BLOCK_HEIGHT*(y+1)]
        for x in range(BASE / BLOCK_WIDTH):
            block = []
            for row in rows:
                block += row[BLOCK_WIDTH*x:BLOCK_WIDTH*(x+1)]

            for n in BASE_RANGE:
                if block.count(n) > 1:
                    raise ValueError("Number {} appears more than once in block y={}, x={}".format(n, y, x))

    print("Checks done, field appears to be a valid sudoku. Proceeding to solve...")

def solve():
    global field

    # the following loop is just to be able to use "continue", it terminates after one full loop
    step = 1
    while step >= 0:
        # reread variables
        zipfield = zip(*field)
        blocks = []
        for y in range(BASE / BLOCK_HEIGHT):
            blocks.append([])
            rows = field[BLOCK_HEIGHT*y:BLOCK_HEIGHT*(y+1)]
            for x in range(BASE / BLOCK_WIDTH):
                block = []
                for row in rows:
                    block += row[BLOCK_WIDTH*x:BLOCK_WIDTH*(x+1)]
                blocks[y].append(block)
        if step == 0:
            step = 1
        elif step == 1:
            # Step 1: Basic solving of single-possibility cells
            print("Step 1...")
            for y, row in enumerate(field):
                for x, cell in enumerate(row):
                    if isinstance(cell, set) or cell == 0:
                        # cell is a list or nonzero number, i. e. unsolved
                        poss = set()
                        for n in BASE_RANGE:
                            if n not in row and n not in zipfield[x] and n not in blocks[y//BLOCK_HEIGHT][x//BLOCK_WIDTH]:
                                # n does not yet exist in row, column or block
                                poss.add(n)
                        
                        if len(poss) == 1:
                            # single possibility, cell is solved
                            print("Cell {} in row {} must be {}".format(x, y, list(poss)[0]))
                            field[y][x] = list(poss)[0]
                            step = 0
                        elif len(poss) == 0:
                            # no possibilities, something went wrong
                            print("No possibilities for cell {} in row {}, this should never happen!".format(x, y))
                            retry = True
                            step = -1
                        else:
                            # more than one possibility, store for later
                            field[y][x] = poss
                    
                    if step <= 0:
                        break
                if step <= 0:
                    break
            if step == 1:
                step = 2
        elif step == 2:
            # Step 2: Analyze mutually exclusive possibilities
            print("Step 2...")
            for y, row in enumerate(field):
                for x, cell in enumerate(row):
                    if isinstance(cell, set):
                        poss = set()
                        # Step 2.1: Correlate with other possibilities in same row
                        oposs = set()
                        for ocell in row:
                            if isinstance(ocell, set) and ocell is not cell:
                                oposs.update(ocell)
                        
                        for n in cell:
                            if n not in oposs:
                                # if n cannot go elsewhere, it must go here
                                poss.add(n)
                        
                        # Step 2.2: Correlate with other possibilities in same column
                        oposs = set()
                        for ocell in zipfield[x]:
                            if isinstance(ocell, set) and ocell is not cell:
                                oposs.update(ocell)
                        
                        for n in cell:
                            if n not in oposs:
                                # if n cannot go elsewhere, it must go here
                                poss.add(n)

                        # Step 2.3: Correlate with other possibilities in same block
                        oposs = set()
                        for ocell in blocks[y//BLOCK_HEIGHT][x//BLOCK_WIDTH]:
                            if isinstance(ocell, set) and ocell is not cell:
                                oposs.update(ocell)
                        
                        for n in cell:
                            if n not in oposs:
                                # if n cannot go elsewhere, it must go here
                                poss.add(n)
                        if len(poss) == 1:
                            # single possibility, cell is solved
                            print("Cell {} in row {} must be {}".format(x, y, list(poss)[0]))
                            field[y][x] = list(poss)[0]
                            step = 0
                        elif len(poss) == 0:
                            # no possibilities, simply ignore
                            pass
                        else:
                            # more than one possibility, something went wrong
                            print("More than one possibility ({}) in step 2 for cell {} in row {}, this should not happen!".format(poss, x, y))
                    
                    if step <= 0:
                        break
                if step <= 0:
                    break
            if step == 2:
                step = -1
    
    print("Final result: [")
    for row in field:
        print(str(row) + ",")
    print("]")

if __name__ == "__main__":
    precheck()
    solve()
