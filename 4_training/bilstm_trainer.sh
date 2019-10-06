#!/bin/bash
echo "This programm will launch 4 Training of bilstm_goalReduced"
echo "One for each goal positions"

TIMESTAMP=$(date "+%Y%m%d")
FAMILY_FOLDER="model_$TIMESTAMP"
mkdir "$FAMILY_FOLDER"

for i in $(seq 1 2); do
  MODEL_NAME="$FAMILY_FOLDER_$i"
  echo "Network $MODEL_NAME training..."
  papermill ../3_models/BiLSTM_goalReduced.ipynb ./BiLSTM_goalReduced_"$i".ipynb -p GOAL_POS "$i" -p MODEL_DIR_PATH "$MODEL_NAME"
  mv BiLSTM_goalReduced_"$i".ipynb "$MODEL_NAME"
  mv "$MODEL_NAME" "$FAMILY_FOLDER"
  echo "Network $MODEL_NAME done!"
done
mv "$FAMILY_FOLDER" trained
rm tf.log
rm temp_model.info
