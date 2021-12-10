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
2. Wait for the good-to-go from test-runner
   ```sh
   docker logs test-runner -f
   ```
   - If you see this as the last line in the logs, wait a while more:
     ```
     🕐       Waiting for Airflow Web server to be ready...
     ```
   - Once you see this, we're good to go (`CTRL+C` to exit log-watching mode)
      ```
      Airflow Web server is good to go!
      ```
4. Open an interactive shell into the `test-runner` container to start inputting your test commands
   ```sh
   docker exec -it test-runner bash
   ```
