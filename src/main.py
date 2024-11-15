import os
import sys
import glpk
import warnings

def read_file(path):
    with open(path, "r") as f:
        return f.read()

def default_error():
    raise Exception("A error ocurred\n\tTry again or contact the developer team")

def start_equal_to_end_point_error():
    raise Exception("The start point must be different from end point\n\tFix it and try again!")

def instance_with_wrong_format_error():
    raise Exception("The instance is in the wrong format\n\tFix it and try again!")

def no_instance_path_passed_error():
    raise FileNotFoundError("No instance file path passed as argument\n\tUse: main.py <path_to_instance> <start_point> <end_point>")

def no_start_point_passed_error():
    raise FileNotFoundError("No start point passed as argument\n\tUse: main.py <path_to_instance> <start_point> <end_point>")

def no_end_point_passed_error():
    raise FileNotFoundError("No end point passed as argument\n\tUse: main.py <path_to_instance> <start_point> <end_point>")

def unecessary_arguments_warning():
    warnings.warn("Unecessary arguments passed\nUse only this format: main.py <path_to_instance> <start_point> <end_point>")

def print_columns(cols):
    for col in cols:
        if(col.primal != 0): print(" ", col.name, "=", col.primal)

def print_solution(lp):
    print('The problem was solved!')
    print(f'Value of objective function: {lp.obj.value}')
    print('Value of variables with no zero values:')
    print_columns(lp.cols)

def print_no_solution():
    print('The problem has no feasible solution!')
    print('Reavaluate the arguments and instance passed and try again!')

def solve(n, m, s, t, A, instance_name):
    lp = glpk.LPX()

    lp.name = 'Shortest path problem'
    lp.obj.maximize = False

    lp.cols.add(m)
    lp.rows.add(n)

    matrix = []
    obj = [0] * m

    for index, (i, j, c) in enumerate(A):
        col = lp.cols[index]

        col.name = "x%d_%d" % (i, j)
        col.bounds = 0, 1

        matrix.append((i, index, 1))
        matrix.append((j, index, -1))
        
        obj[index] = c

    for i in range(n):
        lp.rows[i].name = "cons_%d" % i

        if i == s: lp.rows[i].bounds = 1, 1
        elif i == t: lp.rows[i].bounds = -1, -1
        else: lp.rows[i].bounds = 0, 0

    lp.matrix = matrix
    lp.obj[:] = obj

    lp.simplex()

    if(lp.status == 'opt'): print_solution(lp)
    else: print_no_solution()

    if(not os.path.exists('output')): os.makedirs('output')
    lp.write(cpxlp=f'output/{instance_name}.lp')
    lp.write(sol=f'output/{instance_name}.sol')

def main():
    args = sys.argv[1:]

    if len(args) == 0: no_instance_path_passed_error()
    if len(args) == 1: no_start_point_passed_error()
    if len(args) == 2: no_end_point_passed_error()
    if len(args) > 3: unecessary_arguments_warning()

    instance_file_path = args[0]
    instance_content = read_file(instance_file_path)
    instance_lines = instance_content.split('\n')
    instance_name = os.path.basename(instance_file_path)

    s, t = int(args[1]), int(args[2])

    if(s == t): start_equal_to_end_point_error()

    A = []
    try:
        if instance_lines[0][0] != 'P': instance_with_wrong_format_error()

        n, m = map(int, instance_lines[0].split()[1:])

        for line in instance_lines[1:-1]:
            if(line[0] != 'A'): instance_with_wrong_format_error()

            i, j, c = map(int, line.split()[1:])
            A.append((i, j, c))
    except Exception:
        default_error()
            
    if instance_lines[-1][0] != 'T': instance_with_wrong_format_error()

    solve(n, m, s, t, A, instance_name)

main()
