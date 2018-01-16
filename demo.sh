#!/bin/bash

rm py_out/*
./kernel_sneaker.py py_out/out.py Python python false
pipreqs py_out/

rm py_notebook_out/*
./kernel_sneaker.py py_notebook_out/out.ipynb Python python true
jupyter nbconvert --to script py_notebook_out/out.ipynb
pipreqs py_notebook_out/
