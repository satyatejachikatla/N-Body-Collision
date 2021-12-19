#!/bin/bash

export SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export TOPDIR=`realpath $SCRIPT_DIR/..`
export VENV_PATH=$TOPDIR/venv