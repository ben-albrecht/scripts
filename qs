#!/bin/bash

Ratio() {
    running=$(qstat | grep $1 | grep -c " R ")
    total=$(qstat | grep -c $1)
    echo $1 : $running / $total $(bc -l <<< $running/$total)
}

date
total=`qstat | wc -l`
totalR=`qstat | grep -c " R "`
echo "Total:  $totalR / $total  " `bc -l <<< $totalR/$total  `

Ratio "shared"
Ratio "shared_large"
Ratio "mem48g"
Ratio "dist"
Ratio "dist_ivy"
Ratio "dist_big"
Ratio "dist_small"
Ratio "dist_fast"
Ratio "nehalem"
Ratio "ib"
