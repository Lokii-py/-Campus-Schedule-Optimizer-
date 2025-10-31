#!/bin/bash

GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
YELLOW=$(tput setaf 3)
NC=$(tput sgr0)

echo "${YELLOW}Starting the Schedule Extraction Process ${NC}"
START_TIME=$(date +%s)

#main code
python3 main.py --path '../data/schedule.txt' --courseName 'ENG MGT'

if [ $? -eq 0 ]; then
    END_TIME=$(date +%s)
    ELAPSED_TIME=$((END_TIME - START_TIME))
    echo "${GREEN}Task completed succesfully in ${ELAPSED_TIME} seconds.${NC}"
else
    echo "${RED}FAILED. Please check the error messages above.${NC}"
    exit 1
fi