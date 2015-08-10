#!/bin/bash

Ratio() {
    running=$(qstat | grep $1 | grep -c " R ")
    total=$(qstat | grep -c $1)
    if [ $total -eq 0 ]; then
        echo $1 : 0 / 0  Queue Empty!
    else
        echo $1 : $running / $total $(bc -l <<< $running/$total)
    fi
}

date
total=`qstat | wc -l`
totalR=`qstat | grep -c " R "`
echo "Total:  $totalR / $total  " `bc -l <<< $totalR/$total  `

Ratio "ishared"
Ratio "ishared_large"
Ratio "ishared_short"
Ratio "mem48g"
Ratio "dist"
Ratio "dist_ivy"
Ratio "dist_big"
Ratio "dist_small"
Ratio "dist_fast"
Ratio "dist_short"
Ratio "nehalem"
Ratio "ib"
