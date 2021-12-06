# Automated-running-of-multiple-SESSA-files-XPS-AES
Automated running of multiple SESSA (simulation of electron spectra for surface analysis, NIST) simulations

The scripts were adapted from the work of Yung-Chen Wang, where they kindly put the script in their PhD thesis (https://mobt3ath.com/uplode/books/book-82574.pdf)
I added options for varying thickness (with various options), varying photon energy, added the planar geometry morphology option, and removed some bugs in both scripts.

Essentially the first script will look at an excel file were you outlined what you want to do in the simulations (how many with what varying inbetween them) + everything else sessa needs to know. It then writes session files (one per simulation) for sessa to read with these details in each. The second script opens sessa and gets it to run each session file one by one, and stores the results in a new excel file so you can compare all simulations easily at the end.

Note you will need python and SESSA installed. I usually ran the scripts from batch files I will also upload examples. You need to tell that the path to your python and the script.

Put all the details for the sample, and the values you want to vary between in the different runs, in the excel file. This should be fairly self explanatory when you look at the file (more details below)

Also note that to speed up my simulations I removed all Auger peaks by setting AES_THRESHOLD to 1 (line 403 of the generator script). Comment out that line if you want to have augers included, but it will increase run times.

How to use sessa simulation automater:

Part I:
Make an excel csv file with name "SESSA_sample_def.csv" with the set up parameters for what you want to simulate.

The key advantage of using this is that you can vary the following things and all the simulations will get run:
Thickness of layers 
Density of layers
Photon energy (only when you have chosen 4 for synchrotron radiation)

The experiment Geometry is set up for SpAnTeX at KMC1 (https://www.sciencedirect.com/science/article/pii/S0039602821001072) with grazing incidence of 5 degrees. 
NOTE This will be very different if you are losing a laboratory X-ray source or a soft X-ray beamline so make sure to put the right geometry settings here.
Sample geometry you can currently choose either planar (put 1 in C4) or layered spheres (put 5 in C4), if you want to run layered spheres but keep the total diameter CONSTANT put 6 in C4.

Type of source - 1 is Al Kalpha, 2 MgKalpa, 3 ZrMz, and 4 for synchrotron photons.
	If you put 4, you need to set the energy. Go to B18. If you only want to simulate with ONE photon energy,
	put this number in B18. e.g. 3000 for 3000 eV.
	If you want to VARY the photon energy, you need to enter an upper (A18) and lower (B18) bound, and increment size (C18)
	for example you want 2000 eV, 3000 eV, 4000 eV. Then put 4000 in A18, 2000 in B18, and 1000 in C18.
	The kinetic energy range will stay fixed for each photon energy.
	
Sample composition, always write it with a slash between elements e.g. for water H2/O. 
It is case sensitive too e.g. Gold is Au.
If you have multiple layers with the same element in you can label it them, for example H2/O[1] H2/O[2] etc.

Things necessary to set up:
	Substrate composition in box C21. e.g. Si
	Number of shells (for layered sphere) or "number of layers - 1". Note this doesn't include the substrate.
		e.g. if you have Si subsrate + 3 layers of water on top put 2 in this box. 
	Then go to F4 where you can enter the compostion  and thickness for the layers on top of the substrate.
		Note you must have a thickness in column G even if you are varying this.
		Set density to Default if you are not entering a special density.
		In column O you can put a custom band gap. If you want the band gap from the SESSA database leave this blank.

How to vary layer thickness/density
	For thickness in columns I J and K insert an upper (I) lower (J) and increment size (K)
	Note that this is in ANGSTROMS not nanometres.
	e.g. if you want to simulate the first layer for thicknesses of 20 nm, 25 nm, 30 nm, 35 nm, 40 nm 
	then put I4 400, J4 200, K4 50. 
	If you don't want to vary the thickness of a layer, leave these cells blank.
	
	For density, do the same thing but in columns L, M, and N.
	Note that this is already * 1E22. So if you want 3.2E23, enter 32.
	
Note that you can vary multiple things in one go if you want. e.g. two layer thicknesses, or layer thicknesses and photon energy. It will make session files for all the possible combinations. It can be less nice to look at the resulting excel file this way though so I would recommend varying one thing at a time.


You can set the BINDING energy range in B27 and C27 to include all the core levels you need.
You can change the convergence factor in C39. The smaller this is the longer the simulations will take and the more accurate they will be. 1E-4 should be good enough.

Part II:
Put your SESSA_sample_def.csv in the same folder with the 4 files I have given you. (2 .bat files and 2 .py files)

Part III:
Run first_sessa_script.bat (or the SESSAautomaterscript1_generatingsessionfiles.py)
Follow instructions in the cmd window that opens (press enter etc).
This makes a new folder called "session files + date + time"
Inside will be text files that can be read by SESSA
The cmd window will tell you how many variables are varied and how many files are created.

Part IV:
Run second_sessa_script.bat (or SESSAautomaterscript2_runningthesessionfiles.py)
This relies on the session file folder that you created in Part III being the most recently modified folder.
If it's not working but Part III worked try running part III again.

When running, it will open SESSA. (It still seems to work if you already have SESSA open).
After each simulation for a set of coniditons has run it will ask you if you want to close SESSA, click yes.
Note that this can sometimes be hidden behind other windows on your computer. Especially if you did anything else while the simulation is running.
My best advice is to run with the sound of your computer on, so you can hear when this window pops up and then find it by minimzing windows until you see it.

Please note the simulations can take a very long time if you have a lot of elements and have a convergence factor lower than 1E-4

Part V:
Once all simulations are run, you get an excel file created in a results folder inside the session files folder. 
The left hand column is the state of all the variables for that situation (layer thickness, densities and photon energies)
	e.g. the first simulation will be the lower bounds of everything.
The rows show the core level / auger (and label if applicable) 
Now you can make the ratios you're interested in! 

Note: If you want to check that the simulation did what you want, e.g. that the sample layers are correct, you can open one of the session files directly in session (project>>load>>session... , make all files visible and choose a text file.)

Enjoy!

Pip C J Clark
