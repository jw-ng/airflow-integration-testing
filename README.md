# Airflow Integration Tests

This project demonstrates how we can use docker-compose with pytest to run an integration test suite for Airflow DAGs.

## Running the integration tests

### Running all integration tests automatically

Use the following command to run all integration tests automatically

```sh
make integration_test
```

A non-zero exit code from the above command implies that there are failing integration tests.

### Running tests manually (via the test-runner container)

1. Use the following command to start the necessary containers, and have the `test-runner` container ready for manual 
   inputs
   ```sh
   make manual_testing
   ```
2. Open an interactive shell into the `test-runner` container to start inputting your test commands
   ```sh
   docker exec -it test-runner bash
   ```
