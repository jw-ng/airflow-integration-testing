# Airflow Integration Tests

This project demonstrates how we can use docker-compose with pytest to run an integration test suite for Airflow DAGs.

## Setting up

This project uses a `.envrc` file to set up the necessary environment variables used for the integration test.

To begin, make a copy of the `.envrc.template` file and named the copy as `.envrc`:

```sh
cp .envrc.template .envrc
```

Next, replace the variables with value `<SECRET_STRING_TO_BE_FILLED_IN>` with actual value of your choice.
These secrets are used automatically in the set up by Docker Compose and within the pytest test suites. No secrets are 
needed to be checked in.

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
