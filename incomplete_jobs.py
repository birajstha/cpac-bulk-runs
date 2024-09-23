import pandas as pd
import subprocess
import os

# Open the CSV file
df = pd.read_csv("remaining.csv")
os.makedirs('incomplete_jobs', exist_ok=True)
# Iterate over the first column of the CSV file
for index, row in df.iterrows():
    subject = row['Subject']
    remaining = row['Remaining']
    if remaining == "[]":
        continue
    #convert string to list
    remaining = remaining[1:-1].split(', ')
    #strip ('' from the list)
    remaining = [x.strip("'") for x in remaining]

    # if the remaining list is empty, skip to the next subject
    if len(remaining) == 0:
        continue
    subprocess.run(["sbatch", f"jobs/job_{subject}.sh"])
    print(f"Job submitted for {subject}")





    
    # for sess in remaining:
    #     print(subject, sess)
        
#         # Create a new bash script file for each subject and session
#         with open(f'incomplete_jobs/job_{subject}_{sess}.sh', 'w') as bash_file:
#             # Write the modified job02.sh script into the new file
#             bash_file.write(f"""#!/bin/bash
# #SBATCH --mem=30G
# #SBATCH -N 1
# #SBATCH -p RM-shared
# #SBATCH -t 60:00:00
# #SBATCH --ntasks-per-node=20

# PARTICIPANT="{subject}"
# session="{sess}"
# to_run="$PARTICIPANT"

# MED="/ocean/projects/med220004p"
# HOME="/ocean/projects/med220004p/bshresth"
# DATA="/ocean/projects/med220004p/jclucas/data/vannucci/bids_raw"
# OUTPUT="/ocean/projects/med220004p/bshresth/vannucci/all_runs/scripts/outputs/ANTS_FSL_noBBR_strict"
# IMAGE="/ocean/projects/med220004p/bshresth/code/images/cpac_nightly.sif"
# PIPELINE="/ocean/projects/med220004p/bshresth/vannucci/all_runs/configs/ANTS_FSL_noBBR_strict.yml"



# singularity run -B /ocean/projects/med220004p/bshresth/code/C-PAC/CPAC/nuisance/utils:/code/CPAC/nuisance/utils -B $MED -B $DATA:$DATA -B $OUTPUT:$OUTPUT $IMAGE $DATA $OUTPUT participant --num_ants_threads 5 --skip_bids_validator --save_working_dir --n_cpus 2 --mem_gb 50 --participant-label $PARTICIPANT --pipeline-file $PIPELINE

# """)

        # submitting the above job to the cluster
        # subprocess.run(["sbatch", f"incomplete_jobs/job_{subject}_{sess}.sh"])
        #print(f"Job submitted for {subject} {sess}")