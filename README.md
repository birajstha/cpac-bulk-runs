## C-PAC bulk run scripts

1. [job.sh](./job.sh) - This script generates and submits bash scripts to run CPAC parallel for all subjects at the same time.
2. [make_report.py](./make_report.py) - checks the slurm*.out files and parses all lines to check which sub/sessions completes and makes a CSV file.
3. [incomplete_jobs.py](./incomplete_jobs.py) - submits the job for subjects that didnot complete CPAC runs