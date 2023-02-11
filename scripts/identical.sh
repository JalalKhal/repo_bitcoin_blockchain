#!/bin/bash

number_files=2000

for ((i=0; i<number_files; i++))
do
  for ((j=i+1; j<number_files; j++))
  do
    file1="../tests/noeud${i}_blockchain.json"
    file2="../tests/noeud${j}_blockchain.json"
    diff_files=$(diff "$file1" "$file2")
    $diff_files > /dev/null 2>&1 #(explications:https://www.security-helpzone.com/2019/09/22/pourquoi-utiliser-dev-null-2-1/)
    if [ $? -ne 0 ]
    then
      echo "The contents of $file1 and $file2 are different."
      echo $diff_files
      exit 0
    fi
  done
done

echo "The contents of all the files are identical."
exit 1



