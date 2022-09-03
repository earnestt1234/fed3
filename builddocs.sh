#!/bin/bash

# try to find directory of this script
MAIN_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [[ ! -f ${MAIN_DIR}/builddocs.sh ]]
then
	# default to trying current working directory
	echo ""
	echo "Warning: Cannot find main 'builddocs.sh' script at ${MAIN_DIR}."
	echo "Setting to current working directory (PWD): ${PWD}"
	MAIN_DIR=$PWD
fi

# set some locations/variables
IMG_DIR=${MAIN_DIR}/img
DOCS_DIR=${MAIN_DIR}/docs
BRANCH='plots_docs'
URL_IMG_DIR="https://raw.githubusercontent.com/earnestt1234/fed3/${BRANCH}/img"

# locate notebook
IPYNB_NAME='plots_getting_started.ipynb'
SHORTNAME=$(basename $IPYNB_NAME .ipynb)
IPYNB="${DOCS_DIR}/${IPYNB_NAME}"

# convert ipynb to markdown
jupyter nbconvert $IPYNB --to markdown

# record conversion outputs
MARKDOWN=${DOCS_DIR}/${SHORTNAME}.md
IPYNB_FILES_DIR=${DOCS_DIR}/${SHORTNAME}_files

# copy all images to the img dir
IMG_DESTINATION=${IMG_DIR}/${SHORTNAME}
mkdir -p $IMG_DESTINATION
cp $IPYNB_FILES_DIR/* $IMG_DESTINATION

# replace links in markdown file - from local to URL
FINAL_URL=${URL_IMG_DIR}/${SHORTNAME}
SEARCH=${SHORTNAME}_files
REPLACE=${FINAL_URL}
sed -i --expression "s@${SEARCH}@${REPLACE}@" $MARKDOWN

# cleanup - remove original files
rm ${IPYNB_FILES_DIR}/*
rmdir ${IPYNB_FILES_DIR}

# finally, build with pdoc
pdoc --html -o docs fed3 --force