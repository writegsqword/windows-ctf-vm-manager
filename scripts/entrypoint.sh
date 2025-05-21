#!/bin/bash

cd "$(dirname "$0")"
unshare -n bash setup.sh "$@"

