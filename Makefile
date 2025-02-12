.DEFAULT_GOAL := all

# Variables
MUTE_OUTPUT = 1>/dev/null
BACKEND_DIR := backend
NO_PRINT_FLAG := --no-print-directory

# Include backend Makefile
include $(BACKEND_DIR)/Makefile

.PHONY: backend-delete-venv
backend-delete-venv:
	@ $(MAKE) -C $(BACKEND_DIR) $(NO_PRINT_FLAG) delete_venv

.PHONY: backend-format
backend-format:
	@ $(MAKE) -C $(BACKEND_DIR) $(NO_PRINT_FLAG) format

.PHONY: backend-lint
backend-lint:
	@$(MAKE) -C $(BACKEND_DIR) $(NO_PRINT_FLAG) lint

.PHONY: backend-type-check
backend-type-check:
	@$(MAKE) -C $(BACKEND_DIR) $(NO_PRINT_FLAG) type-check

.PHONY: backend-test
backend-test:
	@$(MAKE) -C $(BACKEND_DIR) $(NO_PRINT_FLAG) test

.PHONY: backend-run-dev-server
backend-run-dev-server:
	@$(MAKE) -C $(BACKEND_DIR) $(NO_PRINT_FLAG) run-dev-server

.PHONY: backend-clean
backend-clean:
	@$(MAKE) -C $(BACKEND_DIR) $(NO_PRINT_FLAG) clean

.PHONY: backend-all
backend-all:
	@$(MAKE) -C $(BACKEND_DIR) $(NO_PRINT_FLAG) all
