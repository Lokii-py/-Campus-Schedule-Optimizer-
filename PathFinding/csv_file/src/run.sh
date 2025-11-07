#!/bin/bash

GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
YELLOW=$(tput setaf 3)
NC=$(tput sgr0) # No Color (to reset the text color)

# Start the Script
echo "${YELLOW} Starting the MST Pathfinding Data Pipeline ${NC}"
START_TIME=$(date +%s)

#the main code
python3 main.py --config "../config.yaml"


if [ $? -eq 0 ]; then
    END_TIME=$(date +%s)
    ELAPSED_TIME=$((END_TIME - START_TIME))
    echo "${GREEN} Pipeline finished successfully in ${ELAPSED_TIME} seconds.${NC}"
else
    echo "${RED} Pipeline failed. Please check the error messages above.${NC}"
    exit 1
fi