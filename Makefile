#################################################################################
# GLOBALS                                                                       #
#################################################################################

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Run lint checks manually
lint:
	@echo "+ $@"
	@if [ ! -d .git ]; then git init && git add .; fi;
	@tox -e lint
.PHONY: lint

## Run combine data service
combine-data:
	@echo "+ $@"
	@docker compose up combine-data --detach
.PHONY: combine-data

## Run filter data service
filter-data:
	@echo "+ $@"
	@docker compose up filter-data --detach
.PHONY: filter-data

## Run process data service
process-data:
	@echo "+ $@"
	@docker compose up process-data --detach
.PHONY: process-data

## Run split data service
split-data:
	@echo "+ $@"
	@docker compose up split-data --detach
.PHONY: split-data

## Run train service
train:
	@echo "+ $@"
	@docker compose up train --detach
.PHONY: train

## Run inference service
inference:
	@echo "+ $@"
	@docker compose up inference --detach
.PHONY: inference

## Get logs for combine data service
combine-data-logs:
	@echo "+ $@"
	@./utils.sh "combine-data"
.PHONY: combine-data-logs

## Get logs for filter data service
filter-data-logs:
	@echo "+ $@"
	@./utils.sh "filter-data"
.PHONY: filter-data-logs

## Get logs for process data service
process-data-logs:
	@echo "+ $@"
	@./utils.sh "process-data"
.PHONY: process-data-logs

## Get logs for split data service
split-data-logs:
	@echo "+ $@"
	@./utils.sh "split-data"
.PHONY: split-data-logs

## Get logs for train service
train-logs:
	@echo "+ $@"
	@./utils.sh "train"
.PHONY: train-logs

## Get logs for inference service
inference-logs:
	@echo "+ $@"
	@./utils.sh "inference"
.PHONY: inference-logs

## Remove Service(s)
down:
	@echo "+ $@"
	@docker compose down
.PHONY: down

## Cleanup combine-data service
reset-combine-data:
	@echo "+ $@"
	@./utils.sh "reset-combine-data"
.PHONY: reset-combine-data

## Cleanup filter-data service
reset-filter-data:
	@echo "+ $@"
	@./utils.sh "reset-filter-data"
.PHONY: reset-filter-data

## Cleanup process-data service
reset-process-data:
	@echo "+ $@"
	@./utils.sh "reset-process-data"
.PHONY: reset-process-data

## Cleanup split-data service
reset-split-data:
	@echo "+ $@"
	@./utils.sh "reset-split-data"
.PHONY: reset-split-data

## Cleanup train service
reset-train:
	@echo "+ $@"
	@./utils.sh "reset-train"
.PHONY: reset-train

## Cleanup inference service
reset-inference:
	@echo "+ $@"
	@./utils.sh "reset-inference"
.PHONY: reset-inference

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
