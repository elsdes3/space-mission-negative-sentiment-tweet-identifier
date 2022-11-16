#!/bin/bash


ACTION=${1:-combine-data}


if [[ "$ACTION" != 'reset'* ]]; then
    echo "Waiting for 5 seconds..."
    sleep 5
    echo "Done."
    docker logs -t $(docker ps --filter "name=${ACTION}" --format "{{.ID}}")
else
    docker rmi $(docker images -a --filter "reference=*${ACTION:6}*" --format "{{.ID}}")

    cd notebooks
    if [[ "$ACTION" == 'reset-combine-data' ]]; then
        cd 3-combine-data
    elif [[ "$ACTION" == 'reset-filter-data' ]]; then
        cd 4-filter-data
    elif [[ "$ACTION" == 'reset-process-data' ]]; then
        cd 5-process-data
    elif [[ "$ACTION" == 'reset-split-data' ]]; then
        cd 6-split-data
    elif [[ "$ACTION" == 'reset-train' ]]; then
        cd 7-train
    elif [[ "$ACTION" == 'reset-inference' ]]; then
        cd 8-inference
    fi

    cd notebooks
    rm -rf .ipynb_checkpoints/
fi
