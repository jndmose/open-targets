# Script to generate the overall association score for a given target-disease association
--Download our EVA evidence dataset in JSON format. This
dataset can be found in the `evidence/sourceId=eva/` directory. The files are available from
http://ftp.ebi.ac.uk/pub/databases/opentargets/platform/21.11/output/etl/ . Please use the ‘21.11’
release files  and store the files in the same directory as the open-targets.py script file with the folder name **eva-evidence**

-- Also download targets and diseases datasets in JSON format and put them in the same directory with the script open-targets.py. Name the folders **targets** and **diseases** respectively.

-- **The script has been written for python3 and so make sure you are using python3 for execution.**

-- On the terminal or command line, issue the command :
```
python3 open-targets.py 
```
-- The process on my machine to run the whole script takes more than an hour as outlined below:
```
Started importing Eva data
--- 26.952093362808228 seconds --- importing eva data
--- 5.822963237762451 seconds --- importing targets data
--- 3.3567192554473877 seconds --- importing disease data
Done importing!
Looping over eva data now
--- 3507.968894958496 seconds --- indexing and giving results
Started Join on targets
Started Join on diseases
Started sorting
Started exporting to json
--- 0.7050304412841797 seconds --- for exporting to json
Started the target target pairs
```

-- The output file with ‘targetId’, ‘diseaseId’, ‘median’, ‘top3’,
‘approvedSymbol’, ‘name’. is the file **evadata.json** .

The number of target-target pairs that share a connection to at least two diseases for the first 4 files from eva-evidence folder is 6947.
However running with the whole data set , my script never finishes. Could be an edge case am ot considering or my machine power is not good enough to run this. 


##  Improvements
--The script takes more than one hour with my machine which is a 7th Gen core i7 machine. Improvements on this sript should focus on a solution that employs multi processing. Do parallel computing when looping over the imported data and also when calculating target-target pairs that share a connection to atleast two diseases.
-- In my opinion The library **deco** https://github.com/alex-sherman/deco is a good option to start with.
