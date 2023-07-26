import random
import subprocess
import math

def initialize_population(num_bits_per_gene, num_individuals,num_genes=2):
    population = []
    for _ in range(num_individuals):
        individual = []
        for _ in range(num_genes):
            gene = [random.randint(0, 1) for _ in range(num_bits_per_gene)]
            individual.append(gene)
        population.append(individual)
    return population
def bits_to_decimal(population,num_bits_per_gene):
    
    val = 2**num_bits_per_gene - 1
    decimal_values_list = []
    for individual in population:
        gene_values = []
        for gene in individual:
            decimal_value = 0
            for bit in gene:
                decimal_value = (decimal_value << 1) | bit
            gene_values.append(decimal_value/val)
        decimal_values_list.append(gene_values)
    
    return decimal_values_list
def create_param(decimal_values_list,par_range):
    paramlist = []
    for ind in decimal_values_list:
        paramlist.append([par_range[0][0]+(par_range[0][1]-par_range[0][0])*ind[0],par_range[1][0]+(par_range[1][1]-par_range[1][0])*ind[1]])
    return paramlist    
def crossover(parent1, parent2):
    num_genes = len(parent1)
    num_bits_per_gene = len(parent1[0])
    crossover_points = [random.randint(1, num_bits_per_gene - 1) for _ in range(num_genes)]
    child1, child2 = [], []
    for gene_index, crossover_point in enumerate(crossover_points):
        child1_gene = parent1[gene_index][:crossover_point] + parent2[gene_index][crossover_point:]
        child2_gene = parent2[gene_index][:crossover_point] + parent1[gene_index][crossover_point:]
        child1.append(child1_gene)
        child2.append(child2_gene)

    return child1, child2
def mutate_individual(individual, mutation_rate):
    mutated_individual = []
    for gene in individual:
        mutated_gene = []
        for bit in gene:
            if random.random() < mutation_rate:
                mutated_bit = 1 - bit
            else:
                mutated_bit = bit
            mutated_gene.append(mutated_bit)
        mutated_individual.append(mutated_gene)
    return mutated_individual
def fitness(paramlist):
 fit =[]
 for individual in paramlist:
   #print(individual)  
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
#define EPSILON {individual[0]}
#define DELTA {individual[1]}
#define ANG_DIST_TOLERANCE 1.2
#define N_GC 8876
#define N_KVEC_PAIRS 224792
#define Y_MAX 0.9999999999926209
#define Y_MIN 0.9900261208247870
#define TOL 0.5
#define P1 35
#define P2 80


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
   #print('quat',quat)
   #print(quat_ideal)
   if quat and  quat_ideal != []:
    s = 0
    for i in range(4):
       s += (float(quat_ideal[i])-float(quat[i]))**2   
    if s:    
     fit.append(math.sqrt(1/s))
     #print(s)
    else:
       fit.append(2**32)
   else:
       fit.append(0)
 #print(fit)
 print('wpoch')      
 return fit    
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
    
        
        
        
        
    
num_genes = 2
num_bits_per_gene = 10
num_individuals = 100
par_range = [[0,1e-14],[1e-5,1e-3]]
num_generation = 100
population = initialize_population(num_bits_per_gene, num_individuals,num_genes=2)
for gen in range(num_generation):
   decimal_values_list = bits_to_decimal(population,num_bits_per_gene)
   paramlist = create_param(decimal_values_list,par_range)
   fit = fitness(paramlist)
   #print(paramlist)
   #print(fit)
   ih = fit.index(max(fit))
   print(paramlist[ih])
   #print()
   new_pop = [population[ih]]
   for i in range(num_individuals-1):
       parent = random.choices(population,weights = tuple(fit),k=2)
       child1, child2 = crossover(parent[0], parent[1])
       new_pop.append(child1)
       new_pop.append(child2)
   population = new_pop
print(paramlist[ih])
print()
   
   


