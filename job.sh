#!/bin/bash

# Set your variables
CONFIG=ANTS_FSL_noBBR_strict
MED="/ocean/projects/med220004p"
HOME="${MED}/bshresth"
DATA=/ocean/projects/med220004p/jclucas/data/vannucci/bids_raw
OUTPUT="${HOME}/vannucci/all_runs/scripts/outputs/$CONFIG"
mkdir -p "$OUTPUT"
IMAGE=/ocean/projects/med220004p/bshresth/code/images/cpac_nightly.sif
PIPELINE="${HOME}/vannucci/all_runs/configs/$CONFIG.yml"
SUBJECTS_FOLDER="${DATA}"

# Iterate through subjects and submit batch jobs
for PARTICIPANT in $(ls "$SUBJECTS_FOLDER" | sort -V)
do

    echo "Submitting job for participant: $PARTICIPANT"

    # Create a SLURM job script
    JOB_SCRIPT="${HOME}/vannucci/all_runs/scripts/${CONFIG}/jobs/job_${PARTICIPANT}.sh"
    
    echo "#!/bin/bash" > "$JOB_SCRIPT"
    echo "#SBATCH --mem=30G" >> "$JOB_SCRIPT"    
    source ~/.bashrc
    echo "#SBATCH -N 1" >> "$JOB_SCRIPT"
    echo "#SBATCH -p RM-shared" >> "$JOB_SCRIPT"
    echo "#SBATCH -t 60:00:00" >> "$JOB_SCRIPT"
    echo "#SBATCH --ntasks-per-node=20" >> "$JOB_SCRIPT"
    echo "" >> "$JOB_SCRIPT"
    echo "MED=\"$MED\"" >> "$JOB_SCRIPT"
    echo "HOME=\"$HOME\"" >> "$JOB_SCRIPT"
    echo "DATA=\"$DATA\"" >> "$JOB_SCRIPT"
    echo "OUTPUT=\"$OUTPUT\"" >> "$JOB_SCRIPT"
    echo "IMAGE=\"$IMAGE\"" >> "$JOB_SCRIPT"
    echo "PIPELINE=\"$PIPELINE\"" >> "$JOB_SCRIPT"
    echo "PARTICIPANT=\"$PARTICIPANT\"" >> "$JOB_SCRIPT"
    echo "" >> "$JOB_SCRIPT"
    echo "" >> "$JOB_SCRIPT"
    echo "singularity run -B $HOME/code/C-PAC/CPAC/nuisance/utils/compcor.py:/code/CPAC/nuisance/utils/compcor.py -B \$DATA:\$DATA -B \$OUTPUT:\$OUTPUT \$IMAGE \$DATA \$OUTPUT participant --num_ants_threads 5 --skip_bids_validator --save_working_dir --n_cpus 2 --mem_gb 50 --participant-label \$PARTICIPANT --pipeline-file \$PIPELINE" >> "$JOB_SCRIPT"

    # Submit the job
    sbatch "$JOB_SCRIPT"
    
done

echo "Job submissions complete."
