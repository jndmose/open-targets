# Script to generate the overall association score for a given target-disease association
--Download our EVA evidence dataset in JSON format. This
dataset can be found in the `evidence/sourceId=eva/` directory. The files are available from
http://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/ . Please use the ‘21.11’
release files  and store the files in the same directory as the open-targets.py script file with the folder name eva-evidence

-- Also download targets and diseases datasets in JSON format and put them in the same directory with the script open-targets.py. Name the folders targets and diseases respectively.

-- The script has been written for python3 and so make sure you are using python3 for execution.

-- On the terminal or command line, issue the command :
python3 open-targets.py 
