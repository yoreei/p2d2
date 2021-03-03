#!/bin/bash
istabular () {
    for filename in $1; do
        local extension=${filename##*.}
        local lower=$(echo "${extension}" | tr '[:upper:]' '[:lower:]')
        echo extension "${lower}"
        if [[ "${lower}" != "csv" ]]; then
            echo "${lower}" is not csv
            return 1 #false
        fi
    done
    return 0 #true
}

rm tabularlist nontabularlist
readarray -d $'\0' zips < <(find ../data/kaggle -type f -name "*.zip" -print0)
for zipfile in "${zips[@]}"; do
    unzipout=$(unzip -l "${zipfile}")
    select=$(echo "$unzipout" | head -n -3 | tail -n+4)
    project=$(echo "$select" | awk '{print $4}')
    filename=$(basename "${zipfile}")
    if istabular "$project";  then
        echo "$filename" is tabular
        echo "$filename" >> tabularlist
    else
        echo "$filename" is nontabular
        echo "$filename" >> nontabularlist
        rm "${zipfile}"
    fi
done

find ../data/kaggle -type d -empty -delete
