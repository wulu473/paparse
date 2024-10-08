
EXAMPLES := $(shell find examples -name '*.py')

.PHONY: tests
tests:
	pytest .

.PHONY: lint
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

.PHONY: examples
examples: $(EXAMPLES)

.PHONY: $(EXAMPLES)
$(EXAMPLES):
	python $@

.PHONY: debug
debug:
	@echo $(EXAMPLES)
