from subprocess import Popen, PIPE
import pytest


# @pytest.fixture(scope="session", autouse=True)
def pytest_sessionstart(session):
    print("Starting the API for testing")
    psql_db_name = 'test'
    psql_db_user = 'test'
    psql_db_pass = 'test'
    psql_db_host = 'localhost'
    psql_db_port = '42421'
    # Start the Postgres database with docker
    psql_docker = Popen(['docker',
                         'run',
                         '-d',
                         '-p', psql_db_port + ':5432',
                         '-e', 'POSTGRES_DB=' + psql_db_name,
                         '-e', 'POSTGRES_USER=' + psql_db_user,
                         '-e', 'POSTGRES_PASSWORD=' + psql_db_pass,
                         '--name', 'psql_test',
                         'postgres:latest'], stdout=PIPE, stderr=PIPE)

    redis_port = '42422'
    # Start the Redis server with docker
    redis_docker = Popen(['docker', 'run', '-d', '-p', redis_port + ':6379', '--name', 'redis-test', 'redis:latest'], stdout=PIPE, stderr=PIPE)

    # Set env variables for the test
    import os
    os.environ['psql_db'] = psql_db_name
    os.environ['psql_user'] = psql_db_user
    os.environ['psql_pass'] = psql_db_pass
    os.environ['psql_host'] = psql_db_host
    os.environ['psql_port'] = psql_db_port
    os.environ['redis_host'] = 'localhost'
    os.environ['redis_port'] = redis_port

    # Wait for the docker containers to start
    import time
    time.sleep(2)

    new_env = {
        'psql_db': psql_db_name,
        'psql_user': psql_db_user,
        'psql_pass': psql_db_pass,
        'psql_host': psql_db_host,
        'psql_port': psql_db_port,
        'redis_host': 'localhost',
        'redis_port': redis_port
    }
    env = os.environ.copy()
    env.update(new_env)

    # Run the API
    _ = Popen(["uvicorn", "main:app", "--reload", "--port", "42423"], stdout=PIPE, stderr=PIPE, env=env)

    pytest.api_url = 'http://localhost:42423'
    time.sleep(2)

def pytest_sessionfinish(session, exitstatus):
    print("Tearing down the API")
    # Stop the docker containers
    _ = Popen(['docker', 'stop', 'psql_test', 'redis-test'], stdout=PIPE, stderr=PIPE)
    _ = Popen(['docker', 'rm', 'psql_test', 'redis-test'], stdout=PIPE, stderr=PIPE)
