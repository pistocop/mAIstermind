#!/bin/bash
STRATEGY=$1
NUM_PROCESSES=$2
NUM_CYCLES=$3
SAVE_LAP=$4
OPTIMAL_START=$5
SILENT_MODE=$6

echo "************"
echo "Strategy: "$STRATEGY
if [ "$OPTIMAL_START" = "true" ]; then
    echo "Optimal start enabled"
    OPTIMAL_START_CMD="--optimal_start"
else
    echo "Optimal start disabled"
    OPTIMAL_START_CMD=""
fi

if [ "$SILENT_MODE" = "true" ]; then
    echo "Silent mode enabled"
    SILENT_MODE_CMD="--silent"
else
    echo "Silent mode disabled"
    SILENT_MODE_CMD=""
fi
echo "Total matches to create: "$(($NUM_PROCESSES * $NUM_CYCLES * 1296))
echo "Databes will be updated each "$SAVE_LAP" matches"
echo "Logs of matches will be inside /logs folder"
mkdir logs

####################
ELABORATION_ID=`date "+%Y%m%d_%H%M%S"`
OUTPUT_PATH="../database/dbPlayers/"$STRATEGY"/chest/"$STRATEGY"_"$ELABORATION_ID"_"
echo "Note: the matches will be stored inside "$OUTPUT_PATH"N.csv"
echo "************"
####################

for i in `seq 1 $NUM_PROCESSES`;
do
    echo "Starting Nprocess="$i
	python -B db_creator.py \
	        --strategy $STRATEGY \
	        --output_path $OUTPUT_PATH$i".csv" \
	        --cut_history_path $OUTPUT_PATH$i"_cuts.csv" \
	        --saving_lap $SAVE_LAP \
	        --cycles $NUM_CYCLES \
	        "$OPTIMAL_START_CMD" \
	        "$SILENT_MODE_CMD" \
	        > "./logs/"$ELABORATION_ID"_"$i".log" &
	
	echo "Nprocess="$i" started"
done
