#!/bin/bash


ACTION=${1:-combine-data}


if [[ "$ACTION" != 'reset'* ]]; then
    echo "Waiting for 5 seconds..."
    sleep 5
    echo "Done."
    docker logs -t $(docker ps --filter "name=${ACTION}" --format "{{.ID}}")
else
    docker rmi $(docker images -a --filter "reference=*${ACTION}*" --format "{{.ID}}")

    if [[ "$ACTION" == 'reset-combine-data' ]]; then
        cd 3-combine-data/n otebooks
    elif [[ "$ACTION" == 'reset-filter-data' ]]; then
        cd 4-filter-data/notebooks
    elif [[ "$ACTION" == 'reset-process-data' ]]; then
        cd 5-process-data/notebooks
    elif [[ "$ACTION" == 'reset-split-data' ]]; then
        cd 6-split-data/notebooks
    elif [[ "$ACTION" == 'reset-train' ]]; then
        cd 7-train/notebooks
    elif [[ "$ACTION" == 'reset-inference' ]]; then
        cd 8-inference/notebooks
    elif [[ "$ACTION" == 'reset-assess' ]]; then
        cd 8-assess/notebooks
    fi

    rm -rf .ipynb_checkpoints/
fi
