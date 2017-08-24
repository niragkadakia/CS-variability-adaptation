#!/bin/bash
#SBATCH --job-name=mu_Ss0-eps
#SBATCH --mem-per-cpu=6000 
#SBATCH --time=01:00:00      
#SBATCH --ntasks=1            
#SBATCH --nodes=1            
#SBATCH --array=0-1000
#SBATCH --output=out.txt
#SBATCH --open-mode=append

#module restore py2.7.6

specs_file=mu_Ss0-epsilon
bin=../scripts/CS_run.py 
nDiv_bot_var=500

mu_Ss0=$(($SLURM_ARRAY_TASK_ID / $nDiv_bot_var));
epsilon=$(($SLURM_ARRAY_TASK_ID % $nDiv_bot_var));

echo $mu_Ss0;
echo $epsilon;

python $bin $specs_file $mu_Ss0 $epsilon

exit 0
