# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 11:34:19 2020

@author: Pip Clark, 
"""

# Goal: generate session files automatically for SESSA software V2.0. Python version 3
from datetime import datetime
import os.path
import sys
import csv
import itertools

# ---------Welcome message---------#
# print('')
# print('Hello! This is a program that generates SESSA V2.1 session files')
# print('This program is especially helpful if you need to generate lots of similar files!\n')
# print('You can choose planar layers, spheres, or layered spheres\n. Currently no support for roughness and islands morphologies')


# defining some functions for use later in the code
def read_cell(x, y):
    with open('SESSA_sample_def.csv', 'r') as f:
        reader = csv.reader(f)
        y_count = 0
        for n in reader:
            if y_count == y:
                cell = n[x]
                return cell
            y_count += 1
def read_layered_spheres_information(): #or all information for whichever type
    #note for planar the core is the first layer above substrate, and shells are layers above it
    s_type = int(read_cell(2, 3)) # sample_type
    x_s = int(read_cell(2, 6)) # x_ray source type
    x_r = float(read_cell(2, 8)) # x_ray_incident angle, theta
    x_rphi = float(read_cell(2, 9)) # x_ray_incident angle, phi
    pol_theta = float(read_cell(2,7))
    a_axis = float(read_cell(2, 10)) # analysis axis angle
    s_phi = float(read_cell(2, 11)) # sample phi angle
    s_surface = float(read_cell(2, 12)) # sample surface theta (angle)
    a_angle = float(read_cell(2, 14)) # aperture angle
    c_substrate = read_cell(2, 20)
    c_composition = read_cell(5, 3) # core composition
    c_diameter = read_cell(6, 3) # core diameter
    n_of_shells = int(read_cell(2, 22)) # number of additional shells
    single = read_cell(2, 30)
    trans = read_cell(2, 32)
    sla = read_cell(2, 34)
    rsa = float(read_cell(2, 36))
    convergence_fact = read_cell(2, 38)
    BE_low = read_cell(1,  26)
    BE_high = read_cell(2, 26)
    return s_type, x_s, x_r, x_rphi, pol_theta, a_axis, s_phi, s_surface, a_angle, c_substrate, c_composition, c_diameter, n_of_shells, \
     single, trans, sla, rsa, convergence_fact, BE_low, BE_high,
     
def increment_calc(incre, upper, lower):
 total_dis = float(upper) - float(lower)
 result = total_dis // float(incre)
 if total_dis % float(incre) == 0.0:
 
     result -= 1
 vary_list = []
 for nn in range(int(result) + 1):

     vary_list.append(float(lower) + (nn * float(incre)))
 vary_list.append(float(upper))
 return vary_list
# ---------Welcome message---------#
print('Before we begin, please define your sample parameters using the template excel file: SESSA_sample_def')
print('Save the file as a CSV (comma separated value file) in the current directory as "SESSA_sample_def.csv"\n')
input('Enter any key to continue...\n')
# Check if the proper CSV file exist, else return an error message
if os.path.isfile('SESSA_sample_def.csv') is False:    
    print('CSV file not found in the current directory.')
    sys.exit('Please make sure the CSV file exist in the current directory and restart the script')
# Read the sample information from the CSV file for layered sphere sample
sample_type, x_source, x_ray_incident, x_ray_phi, x_ray_poltheta, analysis_axis, sample_phi, sample_surface, aperture_angle, sub_comp, core_composition\
, core_diameter, number_of_shells, single_particle_TF, transport_approx_TF, sla_TF, rsa_value, convergence_factor, BElow, BEhigh\
 = read_layered_spheres_information()
# ---Read values of the additional layers, including possible variation in thickness & density----#
# Read shell composition based on the user input of the number of shells
#print(core_diameter)
shell_comp_list = []
for n in range(4, 4 + number_of_shells):
    shell_comp_list.append(read_cell(5, n))
# Read shell thickness based on the user input of the number of shells
shell_thick_list = []
if sample_type == 5:
    for n in range(4, 4 + number_of_shells):
        shell_thick_list.append(float(read_cell(6, n))*2) # For layered spheres, shell thickness need to be doubled
    
            
if sample_type ==6:
    total_diameter = core_diameter # needs to be before loop!
    for n in range(4, 4 + number_of_shells):
        shell_thick_list.append(float(read_cell(6, n))*2) # For layered spheres, shell thickness need to be doubled        
        core_diameter = str(float(core_diameter) - (sum(shell_thick_list))/2)
                

if sample_type == 1:
    for n in range(4, 4 + number_of_shells):
        shell_thick_list.append(float(read_cell(6, n))) #doesn't need to be double for planar
        
# Read shell density based on the user input of the number of shells
density_list = []
for n in range(3, 4 + number_of_shells):
 density_list.append(read_cell(7, n))

#%%
if x_source == 4:
    vary_photonE_TF = False #defalt assuming no photon E variation
    nested_photonE_list = [] # list for varying the photon energy
    vary_photonE_TF_list = []
    temp_list = []
    nested_KErange = []
    for z in range(0,3): #will do z = 0, 1, 2
        if read_cell(z,17) != '':
            temp_list.append(float(read_cell(z,17)))
            #print(read_cell(z,17))
        elif read_cell(z+1,17) != '': #for when photon energy is not varied
            photonE = read_cell(z+1,17) #only lower bound is set as photon E
            break
        else:
            print('you selected synchrotron source but have not set an energy. Please enter it in the lower bound box')
            sys.exit('you selected synchrotron source but have not set an energy. Please enter it in the lower bound box')
    if  read_cell(0, 17) != '':
       vary_photonE_TF = True #because the cell isn't empty we are varying PE!
       nested_photonE_list.append(temp_list)   
       
#now make the list with the full range of photon energies in it       

if vary_photonE_TF is False: # No action if that layer isn't varying
    nested_photonE = []
    photonE_list = [photonE]
    pass
else:
     nested_photonE = []    
     for n in range(0,1):
        upper_bound = nested_photonE_list[0][0] # upper limit
        lower_bound = nested_photonE_list[0][1] # lower limit
        increment = nested_photonE_list[0][2] # increment
        if upper_bound < lower_bound: # upper & lower value check
            sys.exit('The upper boundary of photon energy in the CSV file is smaller than the lower boundary')
        temp_list = increment_calc(increment, upper_bound, lower_bound) #don't need the temporary list and append because only do it once
        photonE_list = temp_list
        nested_photonE.append(temp_list)
        
        
for p in range(len(photonE_list)):
            vary_photonE_TF_list.append(True)        
            #also need to make a str list of the KE ranges
            photonE = str(photonE_list[p])
            lowlimstr = photonE + '-' + BElow #makes a string that is the KE1 lim equation
            highlimstr = photonE + '-' + BEhigh #makes a string that is the KE2 lim equation
            KEhighlim = eval(lowlimstr) # does the math in thouse strings
            KElowlim = eval(highlimstr)
            KErange = str(KElowlim) + ':' +str(KEhighlim) #turns it back into a string that is the KE range
            nested_KErange.append(KErange)
 #%%
# Read the variable values (if exist) thickness first, followed by density, including the boundaries and increments
nested_variable_thick = []
vary_thick_TF = False # Default assuming no variation in thickness
vary_thick_TF_list = [False]
for p in range(number_of_shells):
    vary_thick_TF_list.append(False)
vary_density_TF = False # Default assuming no variation in density
vary_density_TF_list = [False]
for q in range(number_of_shells):
 vary_density_TF_list.append(False)

 
  #%%
# Read the thickness variation (and check if exist) and save to a nested list
for z in range(number_of_shells+1):
 temp_list = []
 for zz in range(8, 11):
 
     if read_cell(zz, z+3) != '' and z > 0: #condition for the shells and not the core
         if sample_type == 5:
             temp_list.append(float(read_cell(zz, z+3))*2)
         if sample_type == 6:
             temp_list.append(float(read_cell(zz, z+3))*2)    
         if sample_type == 1:
             temp_list.append(float(read_cell(zz, z+3)))
# For layered spheres, shell thickness need to be doubled hence *2
     elif read_cell(zz, z+3) != '' and z == 0: #this is for the core which doesn't need to be doubled i guess
         temp_list.append(float(read_cell(zz, z+3)))
     else:
         temp_list.append(read_cell(zz, z+3))
         
     if read_cell(zz, z+3) != '':
      vary_thick_TF = True
      vary_thick_TF_list[z] = True
 nested_variable_thick.append(temp_list)
 


 #%% 
# Similar to above, read the density variation information in a nested list
nested_variable_density = []
for i in range(number_of_shells+1):
    temp_list = []
    for ii in range(11, 14):
        if read_cell(ii, i+3) != '': #reading cell L4-L4+#shells
            temp_list.append(float(read_cell(ii, i+3)))
            vary_density_TF = True #gets turned true as soon as a cell has a number in it
            vary_density_TF_list[i] = True            
# Mark the shell that needs to be varied (density)
        else:
            temp_list.append(read_cell(ii, i+3)) # else case for no entry makes a blank list for this sample layer/row in the excel file
    nested_variable_density.append(temp_list)
# Count the number of varying layers ( including the core )
number_layer_variables = 0 # Holds the value of the numbers of total varying layers
for n in range(len(vary_density_TF_list)): # add up the total number of varying density layers
    if vary_density_TF_list[n] is True: 
        number_layer_variables += 1
for n in range(len(vary_thick_TF_list)):
    if vary_thick_TF_list[n] is True: 
        number_layer_variables += 1
if vary_photonE_TF is True:
    number_layer_variables +=1
# Method for creating nested list that contains the new parameters based on the potential variations
# First, take the upper and lower boundary and create a list of intermediate values
# Thickness first
nested_variable_thick_list = []
for n in range(len(nested_variable_thick)):
    if vary_thick_TF_list[n] is False: # No action if that layer isn't varying
         
         pass
    else:
 
        upper_bound = nested_variable_thick[n][0] # upper limit
        lower_bound = nested_variable_thick[n][1] # lower limit
        increment = nested_variable_thick[n][2] # increment
        if upper_bound < lower_bound: # upper & lower value check
            sys.exit('The upper boundary of a thickness in the CSV file is smaller than the lower boundary')
        temp_vary_thick_list = increment_calc(increment, upper_bound, lower_bound)
        nested_variable_thick_list.append(temp_vary_thick_list) # Save as a nested list that contains all values
# Similar concept for the density variation
# NOTE I changed this part to make it work for having no density variation. 
        #If it doesn't work with density varaiton change uncomment the 1st for and comment out the 2nd
nested_variable_density_list = []
for n in range(len(nested_variable_density)):
#for n in range(len(vary_density_TF_list)):
    #print(n)
    
    if vary_density_TF_list[n] is False:     
 #  if len(nested_variable_density) == 0:
        pass

    else: 
    #for n in range(len(nested_variable_density)):
        upper_bound = nested_variable_density[n][0] # upper limit
        lower_bound = nested_variable_density[n][1] # lower limit
        increment = nested_variable_density[n][2] # increment
        if upper_bound < lower_bound: # upper & lower value check 
            sys.exit('The upper boundary of a density in the CSV file is smaller than the lower boundary')
        temp_vary_density_list = increment_calc(increment, upper_bound, lower_bound)
        nested_variable_density_list.append(temp_vary_density_list)

    
     #%% for constant total D
if sample_type == 6:
    constantcore = True
    if sample_type == 6 and vary_thick_TF == True: #changing core diameter and setting total diameter 
        nested_totalD_list = nested_variable_thick_list[0]
        numberofcoresizes = 1
        for l in range(len(nested_variable_thick_list)-1): #calculating the number of core sizes
            numberofcoresizes *=  len(nested_variable_thick_list[l+1])
              #  nested_variable_thick_list[0][n] = nested_variable_thick_list[0][n] - (sum(nested_variable_thick_list[][n]))/2)
    if  sample_type == 6 and vary_thick_TF_list[0] == False:
        nested_totalD_list = [float(total_diameter)] #got to make it a list with integer inside
        for l in range(len(nested_variable_thick_list)-1): #calculating the number of core sizes
            numberofcoresizes *=  len(nested_variable_thick_list[l+1])
           
    shell_vary_list = [] 
    nested_variable_core_list = []
    for i in range(len(nested_variable_thick_list)):
        if vary_thick_TF_list[0] == True: #case for varying total diameter too
            i=+1
        shell_vary_list.append(nested_variable_thick_list[i])
    if len(shell_vary_list) >1:
        shell_vary_combos = list(itertools.product(*shell_vary_list)) #makes all possible combos
    else: 
        shell_vary_combos = [1]*len(shell_vary_list[0])
        for i in range(len(shell_vary_list[0])):
            shell_vary_combos[i] = shell_vary_list[0][i] #for cases when only one shell is varied in size
        for q in range(len(nested_totalD_list)): #does total diameter held first
            for i in range(len(shell_vary_list[0])): #and shell thickness changing for each one
                nested_variable_core_list.append(nested_totalD_list[q] - shell_vary_combos[i])
    
    if len(shell_vary_list) >1:
        for q in range(len(nested_totalD_list)):
            for i in range(len(shell_vary_combos)):
                nested_variable_core_list.append(nested_totalD_list[q] - (sum(shell_vary_combos[i])))
    if vary_thick_TF_list[0] == False: 
        nested_variable_thick_list.insert(0,[])
    vary_thick_TF_list[0] = True #now the core needs to be varied
    nested_variable_thick_list[0] = [1]*len(nested_variable_core_list) #putting the core sizes back into the first row of nested_variable_thick_list
    for i in range(len(nested_variable_core_list)):
        nested_variable_thick_list[0][i] = nested_variable_core_list[i]

#%% Count the total number of files that will be generated

total_generated_files = 1 # preset minimal of 1 file
for n in range(len(nested_variable_thick_list)):
    temp = len(nested_variable_thick_list[n]) # check the length of each nested list
    total_generated_files *= temp # multiply

for n in range(len(nested_variable_density_list)):
 temp = len(nested_variable_density_list[n])
 total_generated_files *= temp # multiply
for n in range(len(nested_photonE_list)):
    temp = len(nested_photonE[n])
    total_generated_files *= temp
    
#%%
    
print('Will vary a total of %i variables' % number_layer_variables)

print('A total of %i files will be generated\n' % total_generated_files)

# make nested_KErange repeat itself for the number of repeats needed
n_rep = int(total_generated_files - len(nested_KErange))
for n in range(n_rep):
    temp_list = nested_KErange[n]
    nested_KErange.append(temp_list)

 #%% Checking and adding band gaps
temp_list = []
nested_bandgap = []
set_bandgap_TF = False
set_bandgap_TF_list = [False]
for q in range(number_of_shells):
    set_bandgap_TF_list.append(False) #makes the list number of shells + core long

for n in range(number_of_shells+1):

    if read_cell(14, n+3) != '': #reading cell L4-L4+#shells
            temp_list.append(float(read_cell(14, n+3)))
            set_bandgap_TF = True
            set_bandgap_TF_list[n] = True
    else:
            set_bandgap_TF_list[n] = False
            temp_list.append('')
    
nested_bandgap.append(temp_list)

 #%%
# Generate a nested list that contains all the combination of variable values
total_variable_list = nested_variable_thick_list + nested_variable_density_list + nested_photonE
total_nested_variable_list = []
for l in itertools.product(*total_variable_list):
 total_nested_variable_list.append(list(l))
# Generate the session files
dt_now = str(datetime.now()) # grab the current time
dt_now = dt_now[:16] # only to the millisecond
dt = dt_now.replace(':', '-') # formatting
folder_name = 'session files ' + dt
# string for folder named session files + the current time
os.mkdir(folder_name) # generate such folder
current_folder_dir = str(os.getcwd()) + '\\' + folder_name
# define the directory of the current folder
 #%%
for n in range(total_generated_files):
 file_name = '_'.join(str(e) for e in total_nested_variable_list[n])
 if total_generated_files == 1:
 
     #first things that you want to be the SAME on each file
     file_name = 'SESSION FILE'
 with open(current_folder_dir + '\\%s.txt' % file_name, 'w') as session_file: 
     x_period = 0
     print('-- SESSA sessa files generated by session_file_mk2', file=session_file)
     print('-- Generated on {}\n'.format(dt), file=session_file)
     print('\\PROJECT RESET', file=session_file) # reset SESSA settings
     print('\\SAMPLE RESET', file=session_file) # reset SESSA settings
     print('\\GEOMETRY RESET', file=session_file) # reset SESSA settings
     print('\\SPECTROMETER RESET\n', file=session_file) # reset SESSA settings
     if x_source == 2: 
         print('\\SOURCE SET MGKA', file=session_file)
     if x_source == 3: 
         print('\\SOURCE SET ZRMZ', file=session_file)
     if x_source == 4:
         if vary_photonE_TF is False:
             print('\\SOURCE SET PHOTONS ENERGY {}'.format(photonE), file=session_file)
             print('\\SOURCE SET POLARIZATION FRACTION 1', file=session_file)#printing fixed photon E
             lowlimstr = photonE + '-' + BElow #makes a string that is the KE1 lim equation
             highlimstr = photonE + '-' + BEhigh #makes a string that is the KE2 lim equation
             KEhighlim = eval(lowlimstr) # does the math in thouse strings
             KElowlim = eval(highlimstr)
             KErange = str(KElowlim) + ':' +str(KEhighlim) #turns it back into a string that is the KE range
             print('\\SPECTROMETER SET RANGE {} REGION 1'.format(KErange), file=session_file) ### this needs to be unique to each photon energy!
         else:
             pass #changing photon E in a loop later
     print('\\GEOMETRY SET ANALYZER THETA {} GEOMETRY 1'.format(analysis_axis), file=session_file) #analyzer angle
     print('\\GEOMETRY SET SOURCE THETA {} GEOMETRY 1'.format(x_ray_incident), file=session_file) # source angle
     print('\\GEOMETRY SET SOURCE PHI {} GEOMETRY 1'.format(x_ray_phi), file=session_file) # source angle
     print('\\GEOMETRY SET SAMPLE PHI {} GEOMETRY 1'.format(sample_phi), file=session_file) #analyzer angle
     print('\\GEOMETRY SET SAMPLE THETA {} GEOMETRY 1'.format(sample_surface), file=session_file) # sample angle
     print('\\GEOMETRY SET APERTURE UTHETA {} GEOMETRY 1'.format(aperture_angle), file=session_file) #A. angle
     print('\\GEOMETRY SET SOURCE POLARIZATION THETA 90 GEOMETRY 1'.format(x_ray_poltheta), file=session_file) 
     print('\\PREFERENCES SET AES_THRESHOLD 1.000000', file=session_file) #should get rid of all auger peaks
 # separate this part out so you can have different morphologies 
     if sample_type ==1:
         print('\\SAMPLE MORPHOLOGY SET PLANAR\n', file=session_file) #default is planar
         #print("default is planar")
  
     if sample_type == 5: #layered spheres  
         #print(sample_type)
         print('\\SAMPLE MORPHOLOGY SET LAYERED_SPHERES\n', file=session_file)
         print('\\SAMPLE MORPHOLOGY SET X_PERIOD {}'.format(float(core_diameter) * 100), file=session_file)
         print('\\SAMPLE MORPHOLOGY SET Y_PERIOD {}\n'.format(float(core_diameter) * 100), file=session_file)
     if sample_type == 6: #layered spheres  
         #print(sample_type)
         print('\\SAMPLE MORPHOLOGY SET LAYERED_SPHERES\n', file=session_file)
         print('\\SAMPLE MORPHOLOGY SET X_PERIOD {}'.format(float(core_diameter) * 100), file=session_file)
         print('\\SAMPLE MORPHOLOGY SET Y_PERIOD {}\n'.format(float(core_diameter) * 100), file=session_file)
    
    
     if single_particle_TF == 'T':  #this might need to go with layered particles too
         print('\\Model set single true', file=session_file)
     if transport_approx_TF == 'T': #this part needed for all I believe
         print('\\MODEL SET TA true', file=session_file)
     if transport_approx_TF == 'F':
         print('\\MODEL SET TA false', file=session_file)
     if sla_TF == 'T': 
         print('\\MODEL SET SLA true', file=session_file) # set SLA setting
     if sla_TF == 'F':
           print('\\MODEL SET SLA false\n', file=session_file) # set SLA setting
     print('\\MODEL AUTO NCOL REGION 1', file=session_file) # set region
     print('\\SAMPLE MORPHOLOGY SET RSA {}'.format(rsa_value), file=session_file)
     print('\\MODEL SET CONVERGENCE {}\n'.format(convergence_factor), file=session_file) # set convergence factor
     if sample_type == 5:
         print('\\SAMPLE SET MATERIAL /{}/ LAYER 1'.format(core_composition), file=session_file) # set core comp.
         print('\\SAMPLE SET MATERIAL /{}/ LAYER 2'.format(sub_comp), file=session_file)
         print('\\SAMPLE SET THICKNESS {} LAYER 1\n'.format(core_diameter), file=session_file) # set core diameter.
     if sample_type == 6:
         print('\\SAMPLE SET MATERIAL /{}/ LAYER 1'.format(core_composition), file=session_file) # set core comp.
         print('\\SAMPLE SET MATERIAL /{}/ LAYER 2'.format(sub_comp), file=session_file)
         print('\\SAMPLE SET THICKNESS {} LAYER 1\n'.format(core_diameter), file=session_file) # 
     if sample_type ==1:
         print('\\SAMPLE ADD LAYER /{}/ THICKNESS {} ABOVE 0'.format(core_composition, core_diameter), file=session_file) #adds first layer        
         #print('\\SAMPLE SET MATERIAL {} LAYER 1'.format(core_composition), file=session_file) # set core comp.
         print('\\SAMPLE SET MATERIAL /{}/ LAYER 2'.format(sub_comp), file=session_file)
         #print('\\SAMPLE SET THICKNESS {} LAYER 1\n'.format(core_diameter), file=session_file) # set core diameter.
         

     
     if vary_thick_TF_list[0] is False:
         if sample_type ==5:
             x_period = float(core_diameter)
     if sample_type ==6:
             x_period = float(total_diameter)   
        # if sample_type ==1:
        #     shell_thick_list /= 2 #thickness of layers in planar sample don
     for nn in range(len(shell_comp_list)): # loop through all shells
         if shell_thick_list[nn] == 0: # adding this avoids sessa fails if a thickness limit is 0
             pass
         else:
             print('\\SAMPLE ADD LAYER /{}/ THICKNESS {} ABOVE 0'.format(shell_comp_list[nn], shell_thick_list[nn]),
                   file=session_file)
 
     print('', file=session_file) # spacer
     for nn in range(len(density_list)): # loop through all shells to set density
 
         if density_list[nn] != 'Default':
 
             print('\\SAMPLE SET DENSITY {}e+022 LAYER {}'.format(density_list[nn], len(density_list)-nn),
                   file=session_file) # set density for the desired shells

     for h in range(len(nested_bandgap[0])):
            if nested_bandgap[0][h] != '':
                
                print('\\SAMPLE SET EGAP {} LAYER {}'.format(nested_bandgap[0][h], len(nested_bandgap[0])-h), file=session_file)
 
    #Now things that you want to be DIFFERENT on each file
     print('', file=session_file) # spacer
     k = 0 # counter
     for kk in range(len(vary_thick_TF_list)):
 
         if vary_thick_TF_list[kk] is False and kk != 0: #when there's no thickness varaiton
 
             x_period += float(shell_thick_list[kk-1])
         if vary_thick_TF_list[kk] is True: # If a layer requires variations
              if total_nested_variable_list[n][k] == 0:
                  
                  print('\\SAMPLE DELETE LAYER {}'.format(abs(kk - len(vary_thick_TF_list))), file=session_file), 
                  x_period += shell_thick_list[k-1] # could be a potential error cause in future! 
                  k +=1
              else:
                  print('\\SAMPLE SET THICKNESS {} LAYER {}'.format((total_nested_variable_list[n][k]),
                        abs(kk - len(vary_thick_TF_list))), file=session_file)
                  
                  x_period += total_nested_variable_list[n][k]
                  k += 1
     d = 0 #counter for density             
     for dd in range(len(vary_density_TF_list)):
         #i think this won't work unless d is offset to be at the column in total nested variable list where the density variation starts!
         if vary_density_TF_list[dd] is True: 
             print('\\SAMPLE SET DENSITY {}e+022 LAYER {}'.format((total_nested_variable_list[n][d]),
                   abs(dd - len(vary_density_TF_list))), file=session_file)
             d += 1
     
     #for f in range(len(vary_photonE_TF_list)):
     if vary_photonE_TF is True: # note this just works because k is always at the column for photon energy at the end of the thickness loop above and therefore in the right place to call the photon energy :')
         #this might not work once density is in there, you might have to have k+d or something. maybe k+d-1
         
         
         print('\\SOURCE SET PHOTONS ENERGY {}'.format(total_nested_variable_list[n][k+d]), file=session_file)        
         print('\\SOURCE SET POLARIZATION FRACTION 1', file=session_file)
         print('\\SPECTROMETER SET RANGE {} REGION 1'.format(nested_KErange[n]), file=session_file)
        
     print('', file=session_file) # spacer
     #settings the core and substrate materials and thicknesses already set above delete these 3 lines that you falsely added :P
     #print('\\SAMPLE SET MATERIAL {} LAYER {}'.format(core_composition,number_of_shells+1),file=session_file) # set core comp.
     #print('\\SAMPLE SET MATERIAL {} LAYER {}'.format(sub_comp,number_of_shells+2), file=session_file)
     #print('\\SAMPLE SET THICKNESS {} LAYER {}\n'.format(core_diameter,number_of_shells+1), file=session_file) # set core diameter.
     if sample_type ==5:
         print('\\SAMPLE MORPHOLOGY SET X_PERIOD {}'.format(x_period), file=session_file) 
         print('\\SAMPLE MORPHOLOGY SET Y_PERIOD {}'.format(x_period), file=session_file)
         print('\\SAMPLE MORPHOLOGY SET Z_HEIGHT {}\n'.format(x_period / 2), file=session_file)
     if sample_type ==6:
         print('\\SAMPLE MORPHOLOGY SET X_PERIOD {}'.format(float(total_diameter)), file=session_file) 
         print('\\SAMPLE MORPHOLOGY SET Y_PERIOD {}'.format(float(total_diameter)), file=session_file)
         print('\\SAMPLE MORPHOLOGY SET Z_HEIGHT {}\n'.format(float(total_diameter) / 2), file=session_file) 
         #sample type 6 makes too many file combos so we have to delete if the total diameter isn't right 
         calcdiam = 0
         for p in range(len(total_nested_variable_list[0])):
             calcdiam += float(total_nested_variable_list[n][p])
         print(calcdiam)
         session_file.close()
         if calcdiam != float(total_diameter):
             delpath = os.path.join(current_folder_dir + '\\%s.txt' % file_name)
             print(delpath)
             os.remove(delpath)