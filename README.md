# web_scrapper

Assumptions I've made:
- While counting words in the title, punctuation should be ignored, so "note-taking app" is 3 words not 2
- In a meantime web links counts as a single word, so (da.vidbuchanan.co.uk) is 1 word, not 4
- News output type as well as filtering mode could be selected in script arguments
- Filtering thresholds and news number to parse are in config.ini file

Usage examples:
python3 main.py
This will run the script without any filtering or output file specified. Output will be made to stdinv.

python3 main.py --filtering_mode 1
This will run the script with filtering mode 1. (Filter all previous entries with more than five words in the title 
ordered by the number of comments first.)

python main.py --filtering_mode 2 --outputfile_name output.txt
This will run the script with filtering mode 2 (Filter all previous entries with less than or equal to five words in 
the title ordered by points.) and write the output to a file named output.txt.