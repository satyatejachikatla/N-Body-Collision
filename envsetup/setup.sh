#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
. $SCRIPT_DIR/common.sh

pip3 install virtualenv
python3 -m virtualenv $VENV_PATH

. $SCRIPT_DIR/env.sh
pip3 install -r $SCRIPT_DIR/requirements.txt
