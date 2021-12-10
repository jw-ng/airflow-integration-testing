clean:
	source .envrc && docker-compose -f docker-compose.yml down --remove-orphans --volumes

run_integration_tests:
	source .envrc && docker-compose -f docker-compose.yml up --exit-code-from test-runner

integration_test: clean run_integration_tests

run_test_runner_in_manual_mode:
	source .envrc && docker-compose -f docker-compose.yml -f docker-compose-manual-testing.yml up -d

manual_testing: clean run_test_runner_in_manual_mode
