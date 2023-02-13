#!/bin/bash
#store the number of files from the command line argument
number_files=$1
for ((i=0; i<number_files; i++))
do
  for ((j=i+1; j<number_files; j++))
  do
    # Store the names of the two files to be compared
    file1="../noeud${i}_blockchain.json"
    file2="../noeud${j}_blockchain.json"
    # Store the difference between the two files
    diff_files=$(diff "$file1" "$file2") > /dev/null 2>&1 # This is used to suppress any error messages and redirect to /dev/null
    if [ $? -ne 0 ]
    then
      echo "The contents of $file1 and $file2 are different."
      echo $diff_files
      exit 1
    fi
  done
done

echo "The contents of all the files are identical."
#remove all the files
rm -r ../noeud*_blockchain.json
exit 0



