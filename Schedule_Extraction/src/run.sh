#!/bin/bash

GREEN=$(tput setaf 2)
RED=$(tput setaf 1)
YELLOW=$(tput setaf 3)
NC=$(tput sgr0)

echo "${YELLOW}Starting the Schedule Extraction Process ${NC}"
START_TIME=$(date +%s)

DATA_DIR="../data"

find "$DATA_DIR" -maxdepth 1 -type f -name "*.txt" | while read -r filepath; do
    
    filename=$(basename "$filepath")
    
    courseName="${filename%.txt}"
    
    echo "\n $filename (Using Course Code: $courseName)"
    
    python3 main.py --path "$filepath" --courseName "$courseName"
    
    # Check if the Python script failed
    if [ $? -ne 0 ]; then
        echo "${RED} FAILED to process $filename.${NC}"
        continue
    fi
    
done

END_TIME=$(date +%s)
ELAPSED_TIME=$((END_TIME - START_TIME))
echo "\n${GREEN}✅ All files processed successfully in ${ELAPSED_TIME} seconds.${NC}"