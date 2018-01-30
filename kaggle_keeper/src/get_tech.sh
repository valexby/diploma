#!/bin/bash

url=${1}
lang=${2}
notebook=${3}
tmp_dir="/tmp/converter_dir"

if [ -e ${tmp_dir} ]; then
    rm -rf ${tmp_dir}
fi

mkdir ${tmp_dir}
wget -i ${tmp_dir}/link -O "${tmp_dir}/downloaded" ${url} &> /dev/null

if [ ${notebook} = "True" ]; then
    jupyter nbconvert --to script "${tmp_dir}/downloaded" &> /dev/null
    mv $(ls ${tmp_dir}/downloade.*) "${tmp_dir}/downloaded"
fi

if [ ${lang} = "python" ]; then
    mv ${tmp_dir}/downloaded ${tmp_dir}/downloaded.py
    pipreqs "${tmp_dir}/"
    if [ -s ${tmp_dir}/requirements.txt ]; then
        grep -oP "\w+(?===)" ${tmp_dir}/requirements.txt
    fi
fi

if [ ${lang} = "markdown" ]; then
    HERE=$(pwd)
    cd ${tmp_dir}
    R -e "library(knitr);purl(\"${tmp_dir}/downloaded\")"  &> /dev/null
    mv downloaded.R downloaded
    cd ${HERE}
fi

if [ ${lang} = "r" ] || [ ${lang} = "markdown" ]; then
    grep -oP 'library\(\K[\w\s]+' ${tmp_dir}/downloaded
fi

rm -rf "${tmp_dir}"
