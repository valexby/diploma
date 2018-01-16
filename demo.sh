#!/bin/bash

rm out/*
./kernel_sneaker.py out/out.py
pipreqs out/
less out/requirements.txt
