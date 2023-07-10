import pygad
import numpy
import subprocess
import random as r
import os


header_content = f'''\
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>


//RGA constants
#define THRESHOLD 3
#define STAR_MIN_PIXEL 3
#define STAR_MAX_PIXEL 150
#define MAX_STARS 100
#define SKIP_PIXELS 2
#define LENGTH 808
#define BREADTH 608
#define PIXEL_WIDTH 0.0000048
#define NUM_MAX_STARS 13

//SM constants
#define FOCAL_LENGTH 0.036
#define EPSILON 2.22e-15
#define DELTA 1e-4
#define ANG_DIST_TOLERANCE 1.2
#define N_GC 8876
#define N_KVEC_PAIRS 224792
#define Y_MAX 0.9999999999926209
#define Y_MIN 0.9900261208247870
#define TOL 0.5
#define P1 35
#define P2 80


'''
global quat_ideal 
header_file_path = 'D:\GitHub\STADS-AlgoTesting\ORION\constants.h'  # Path to the header file

with open(header_file_path, 'w') as file:
    file.write(header_content)

c_code_file = '/mnt/d/GitHub/STADS-AlgoTesting/ORION/main.c'

# Compile the C code
subprocess.run(['wsl', 'gcc', c_code_file, '-o', 'output', '-lm'])

# Execute the compiled C program
completed_process = subprocess.run(['wsl', './output'], capture_output=True, text=True)
print("C program output:")
output = completed_process.stdout

# Save the output into Python variables (example)
quat = output.split('\n')
quat_ideal = [x for x in quat if x]


initial_population =[]
param_list = [3,3,150,100,2.0,808,608,4.8e-06,13.0,0.036,2.22e-15,1e-4,1.2,8876,224792,0.9999999999926209,0.990026120824787,0.5,35,80]

for i in range(10):
   poplist = [] 
   #poplist.append(int(param_list[0]+r.randint(-1,1)))
   #poplist.append(int(param_list[1]+r.randint(-1,1)))
   #poplist.append(param_list[2]+r.randint(-10,10))
   #poplist.append(param_list[3]+r.randint(-10,10))
   #poplist.append(param_list[4]+r.randint(-1,1))
   #poplist.append(int(param_list[5]))
   #poplist.append(int(param_list[6]))
   #poplist.append(param_list[7])
   #poplist.append(param_list[8]+r.randint(-1,1))
   #poplist.append(param_list[9])
   poplist.append(2.22e-15+r.uniform(0,0.05)*2.22e-15)
   poplist.append(1e-4+r.uniform(0,0.05)*1e-4)
   poplist.append(1.2+r.uniform(0,0.05)*1.2)
   #poplist.append(param_list[13])
   #poplist.append(param_list[14])
   #poplist.append(param_list[15])
   #poplist.append(param_list[16])
   poplist.append(0.5+r.uniform(0,0.05)*0.5)
   poplist.append(35+r.randint(-1,1))
   poplist.append(80+r.randint(-1,1))
   initial_population.append(poplist)
   poplist = []
   
   
   
   
   
   
    

# Define the fitness function
def fitness_function(ga_instance,solution, solution_idx):
  
   param_list = [3,3,150,100,2.0,808,608,4.8e-06,13.0,0.036,solution[0],solution[1],solution[2],8876,224792,0.9999999999926209,0.990026120824787,solution[3],solution[4],solution[5]]
   #print(param_list)
   header_content = f'''\
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

// RGA constants
#define THRESHOLD {param_list[0]}
#define STAR_MIN_PIXEL {param_list[1]}
#define STAR_MAX_PIXEL {param_list[2]}
#define MAX_STARS {param_list[3]}
#define SKIP_PIXELS {param_list[4]}
#define LENGTH {param_list[5]}
#define BREADTH {param_list[6]}
#define PIXEL_WIDTH {param_list[7]}
#define NUM_MAX_STARS {param_list[8]}

// SM constants
#define FOCAL_LENGTH {param_list[9]}
#define EPSILON {param_list[10]}
#define DELTA {param_list[11]}
#define ANG_DIST_TOLERANCE {param_list[12]}
#define N_GC {param_list[13]}
#define N_KVEC_PAIRS {param_list[14]}
#define Y_MAX {param_list[15]}
#define Y_MIN {param_list[16]}
#define TOL {param_list[17]}
#define P1 {param_list[18]}
#define P2 {param_list[19]}

'''

   header_file_path = 'D:\GitHub\STADS-AlgoTesting\ORION\constants.h'  # Path to the header file
   

   with open(header_file_path, 'w') as file:
     file.write(header_content)
   c_code_file = '/mnt/d/GitHub/STADS-AlgoTesting/ORION/main.c'

   subprocess.run(['wsl', 'gcc', c_code_file, '-o', 'output', '-lm'],creationflags=subprocess.CREATE_NO_WINDOW)
   output_file = 'D:\GitHub\STADS-AlgoTesting\ORION\output.txt'
# Execute the compiled C program
#subprocess.run('/path/to/c_program/myprogram', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
   
   with open(output_file, 'w') as file:
    subprocess.run(['wsl', './output'], stdout=file, creationflags=subprocess.CREATE_NO_WINDOW)
   output_values = []
   with open(output_file, 'r') as file:
    for line in file:
        value = line.strip()
        output_values.append(value)

   quat = output_values[1:]
   #print(quat)
   if quat and  quat_ideal != []:
    s = 0
    for i in range(4):
       s += (float(quat_ideal[i])-float(quat[i]))**2
    print(s)   
    if s:    
     return 1/s
    else:
       return 2**32 
   else:
       return 0
# Create the genetic algorithm object
ga_instance = pygad.GA(
    num_generations=10,
    num_parents_mating=len(initial_population),
    fitness_func=fitness_function,
    sol_per_pop=len(initial_population),
    initial_population = initial_population,
)

# Run the genetic algorithm
ga_instance.run()
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))




