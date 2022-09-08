#!/bin/bash

# Script to generate the documentation for fed3
# This accomplishes 2 main steps:
#  - Generates the markdown files which demonstrate plotting
#  - runs pdoc to generate the HTML

# This needs to have access to the following tools:
#  - jupyter nbconvert
#  - git
#  - sed
#  - pdoc

# NOTE: This is currently only geared towards generating the documentation
# that is hosted online.  It will not totally work in an offline environment,
# as markdown links are directed to the fed3 GitHub repo to retrieve images.

# # # # # # # # # # # # # #
# Check Dependencies
# # # # # # # # # # # # # #

SOFTWARE_NEEDED="jupyter git sed pdoc"

for tool in $SOFTWARE_NEEDED
do
	found=`command -v $tool`
	if [[ -z $found ]]
	then
		echo ""
		echo "Error; cannot find at least one required software dependency: $tool"
		echo "Exiting."
		echo ""
		exit 1
	fi
done

# specific check for nbconvert
NBCONVERT=$(jupyter --help | grep nbconvert)
if [[ -z $NBCONVERT ]]
then
	echo ""
		echo "Error; cannot find required dependency nbconvert."
		echo "Exiting."
		echo ""
		exit 1
fi

# # # # # # # # # # # # # #
# Locate Script
# # # # # # # # # # # # # # 

MAIN_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [[ ! -f ${MAIN_DIR}/builddocs.sh ]]
then
	# default to trying current working directory
	echo ""
	echo "Warning: Cannot find main 'builddocs.sh' script at ${MAIN_DIR}."
	echo "Setting to current working directory (PWD): ${PWD}"
	MAIN_DIR=$PWD
fi

# # # # # # # # # # # # # #
# Set Variables
# # # # # # # # # # # # # # 

# directories
IMG_DIR=${MAIN_DIR}/img
DOCS_DIR=${MAIN_DIR}/docs

# example notebook
IPYNB_NAME='plots_getting_started.ipynb'
SHORTNAME=$(basename $IPYNB_NAME .ipynb)
IPYNB="${DOCS_DIR}/${IPYNB_NAME}"

# conversion outputs
MARKDOWN=${DOCS_DIR}/${SHORTNAME}.md
IPYNB_FILES_DIR=${DOCS_DIR}/${SHORTNAME}_files

# git branch
IS_GIT=$(git rev-parse --is-inside-work-tree)
if [[ $IS_GIT == 'true' ]]
then
	BRANCH=$(git branch --show-current)
else
	BRANCH='main'
fi

# Online repo for retrieving images
URL_IMG_DIR="https://raw.githubusercontent.com/earnestt1234/fed3/${BRANCH}/img"

# # # # # # # # # # # # # #
# Report
# # # # # # # # # # # # # # 

echo ""
echo "--- fed3 documentation ---"
echo ""
echo "Date: $(date)"
echo ""
echo "VARIABLES"
echo "---------"
echo "MAIN_DIR: ${MAIN_DIR}"
echo "IPYNB: ${IPYNB}"
echo "MARKDOWN: ${MARKDOWN}"
echo "IPYNB_FILES_DIR: ${IPYNB_FILES_DIR}"
echo "BRANCH: ${BRANCH}"
echo "URL_IMG_DIR: ${URL_IMG_DIR}"

# # # # # # # # # # # # # #
# Notebook > Markdown
# # # # # # # # # # # # # # 

echo ""
echo " * * * Running notebook > markdown conversion * * * "
jupyter nbconvert $IPYNB --to markdown
echo " * * * End                                    * * * "

echo ""
echo " * * * Copying images to target directory     * * * "
IMG_DESTINATION=${IMG_DIR}/${SHORTNAME}
mkdir -p $IMG_DESTINATION
cp $IPYNB_FILES_DIR/* $IMG_DESTINATION
echo " * * * End                                    * * * "

echo ""
echo " * * * Replacing markdown links               * * * "
FINAL_URL=${URL_IMG_DIR}/${SHORTNAME}
SEARCH=${SHORTNAME}_files
REPLACE=${FINAL_URL}
sed -i --expression "s@${SEARCH}@${REPLACE}@" $MARKDOWN
echo " * * * End                                    * * * "

# cleanup - remove original files
rm ${IPYNB_FILES_DIR}/*
rmdir ${IPYNB_FILES_DIR}

# # # # # # # # # # # # # #
# Pdoc
# # # # # # # # # # # # # # 

echo ""
echo " * * * Starting pdoc                          * * * "
pdoc --html -o docs fed3 --force
echo " * * * End                                    * * * "