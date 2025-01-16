#!/bin/bash

set -e
set -v
set -x

cd "$(dirname "$0")"

export BUILDER_VENV=.venv
export TEST_VENV=.venv-tests
export SERVER_VENV=.venv-server
export PYTHON_VERSION=${PYTHON_VERSION:-python3}

OAREPO_VERSION=${OAREPO_VERSION:-12}


initialize_server_venv() {

  if [ -d $SERVER_VENV ] ; then
    rm -rf $SERVER_VENV
  fi

  $PYTHON_VERSION -m venv $SERVER_VENV
  source $SERVER_VENV/bin/activate

  $SERVER_VENV/bin/pip install -U setuptools pip wheel nrp-devtools
  $SERVER_VENV/bin/nrp-devtools proxy 120 &
  $SERVER_VENV/bin/pip install "oarepo[tests, rdm]==${OAREPO_VERSION}.*" --index-url "http://127.0.0.1:4549/simple" --extra-index-url https://pypi.org/simple
  $SERVER_VENV/bin/pip install -e complex-model --index-url "http://127.0.0.1:4549/simple" --extra-index-url https://pypi.org/simple
  $SERVER_VENV/bin/pip uninstall oarepo-runtime
  $SERVER_VENV/bin/pip install ~/cesnet/25/oarepo-runtime/
}

initialize_builder_venv() {

  if test -d $BUILDER_VENV ; then
    rm -rf $BUILDER_VENV
  fi

  $PYTHON_VERSION -m venv $BUILDER_VENV
  . $BUILDER_VENV/bin/activate
  $BUILDER_VENV/bin/pip install -U setuptools pip wheel
  $BUILDER_VENV/bin/pip install -e '.[tests]'
}

initialize_client_test_venv() {

  if test -d $TEST_VENV ; then
    rm -rf $TEST_VENV
  fi

  $PYTHON_VERSION -m venv $TEST_VENV

  $TEST_VENV/bin/pip install -U setuptools pip wheel
  $TEST_VENV/bin/pip install requests PyYAML pytest
}

run_builder_tests() {
  pytest tests
}

create_server() {

  if test -d complex-model ; then
    rm -rf complex-model
  fi

  $BUILDER_VENV/bin/oarepo-compile-model ./tests/complex-model.yaml --output-directory complex-model -vvv

}

start_server() {
  (
    initialize_server_venv

    source $SERVER_VENV/bin/activate
    if [ ! -d $SERVER_VENV/var/instance ] ; then
      mkdir -p $SERVER_VENV/var/instance
    fi
    cat <<EOF >$SERVER_VENV/var/instance/invenio.cfg
RECORDS_REFRESOLVER_CLS="invenio_records.resolver.InvenioRefResolver"
RECORDS_REFRESOLVER_STORE="invenio_jsonschemas.proxies.current_refresolver_store"
RATELIMIT_AUTHENTICATED_USER="200 per second"
FILES_REST_DEFAULT_STORAGE_CLASS="L"
FILES_REST_STORAGE_CLASS_LIST = {
    "L": "Local",
    "F": "Fetch",
    "R": "Remote",
}
BABEL_DEFAULT_LOCALE = "en"
BABEL_DEFAULT_TIMEZONE = "Europe/Prague"
I18N_LANGUAGES = [
    ("cs", "Czech"),
]


RATELIMIT_GUEST_USER = "5000 per hour;500 per minute"
RATELIMIT_AUTHENTICATED_USER = "200000 per hour;2000 per minute"

EOF

    invenio db destroy --yes-i-know || true
    invenio db create
    invenio index destroy --yes-i-know || true
    invenio index init --force
    invenio files location create --default default ./simple-server/files

    invenio users create -a -c test@test.com --password testtest
    invenio tokens create -n test -u test@test.com >.token

    (
      export FLASK_DEBUG=1
      invenio run --cert tests/certs/test.crt --key tests/certs/test.key  2>&1 &
      echo "$!" >.invenio.pid
    ) | tee tmp.error.log &
    echo "Waiting for server to start"
    sleep 5
  )
}

stop_server() {
  $SERVER_VENV/bin/invenio db destroy --yes-i-know || true
  $SERVER_VENV/bin/invenio index destroy --yes-i-know || true

  set +e

  if [ -f .invenio.pid ] ; then
    kill "$(cat .invenio.pid)" || true
    sleep 2
    kill -9 "$(cat .invenio.pid)" || true
    rm .invenio.pid || true
  fi
}

#
# entrypoint here
#

initialize_builder_venv
run_builder_tests

create_server

if [ "$1" == "--create" ] ; then
  exit 0
fi



# start server and schedule cleanup
start_server
trap stop_server EXIT

initialize_client_test_venv

if [ "$1" == "--server" ] ; then
  echo "Running at https://127.0.0.1:5000/api/complex-model/. Press enter to stop the server"
  read -r
  exit 0
fi

cat complex-model/data/sample_data.yaml
$TEST_VENV/bin/pytest tests-model


echo "All tests succeeded"
