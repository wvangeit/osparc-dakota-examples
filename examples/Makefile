SHELL := /bin/bash

# List of example directories
EXAMPLES := simple simple_restart simple_batch adasampling moga efficient_global surrogate moga_mixedvar

# Directory for virtual environment
VENV_DIR := pyenv

# Clean target
.PHONY: clean
clean:
	@rm -rf $(VENV_DIR)
	@$(foreach dir,$(EXAMPLES),rm -rf $(dir)/output_tmp;)


.check-uv-installed:
		@echo "Checking if 'uv' is installed..."
		@if ! command -v uv >/dev/null 2>&1; then \
				curl -LsSf https://astral.sh/uv/install.sh | sh; \
		else \
				printf "\033[32m'uv' is installed. Version: \033[0m"; \
				uv --version; \
		fi
		# upgrading uv
		-@uv self --quiet update


.venv: .check-uv-installed
	@uv venv $@
	@echo "# upgrading tools to latest version in" && $@/bin/python --version
	@uv pip list



# Virtual environment target
.PHONY: devenv
devenv: clean .venv
	@uv pip install -r requirements.txt

# General target for examples
.PHONY: $(EXAMPLES)
$(EXAMPLES): clean devenv
	source .venv/bin/activate && \
	mkdir $@/output_tmp && \
	$(if $(filter simple_restart,$@),cp $@/dakota.rst $@/output_tmp &&) \
	cd $@/output_tmp && \
	python ../main.py

# Module-based targets
.PHONY: module-simple_batch module-adasampling
module-simple_batch module-adasampling: clean
	@module load litis-home/dakota && \
		mkdir $(patsubst module-%,%,$@)/output_tmp && \
		$(if $(filter module-simple_batch,$@),cp dakota.rst simple_batch/output_tmp &&) \
		cd $(patsubst module-%,%,$@)/output_tmp && \
		python ../main.py

# Default target
.DEFAULT_GOAL := all

# All target
.PHONY: all
all: $(EXAMPLES)
