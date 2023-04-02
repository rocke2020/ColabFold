#!/usr/bin/env bash
# start the server in local mode
# meaning both workers and server run from the same process
nohup ./msa-server -local -config config.json > log.log 2>&1 &
