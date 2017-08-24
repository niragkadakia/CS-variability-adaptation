#!/bin/bash
#SBATCH --job-name=mu_Ss0-eps
#SBATCH --mem-per-cpu=6000 
#SBATCH --time=01:00:00      
#SBATCH --ntasks=1            
#SBATCH --nodes=1            
#SBATCH --output=out.txt
#SBATCH --open-mode=append

#module restore py2.7.6

specs_file=mu_Ss0-epsilon

bin=../scripts/calculate_errors.py
python $bin $specs_file

bin=../scripts/plot_errors.py
python $bin $specs_file

bin=../scripts/plot_optimal_decoding_variables.py
python $bin $specs_file

exit 0