#!/bin/bash

if [ -d py_out ]; then
    rm py_out/*
else
    mkdir py_out
fi
./kernel_sneaker.py py_out/out.py Python python false
pipreqs py_out/

if [ -d py_notebook_out ]; then
    rm py_notebook_out/*
else
    mkdir py_notebook_out
fi
./kernel_sneaker.py py_notebook_out/out.ipynb Python python true
jupyter nbconvert --to script py_notebook_out/out.ipynb
pipreqs py_notebook_out/

if [ -d r_out ]; then
    rm r_out/*
else
    mkdir r_out
fi
./kernel_sneaker.py r_out/out.R R r false
grep -oP 'library\(\K[\w\s]+' r_out/out.R > r_out/requirements.txt
