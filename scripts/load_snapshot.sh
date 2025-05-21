#!/bin/bash
snapshot=$1
mon_sock=$2



echo "loadvm $snapshot" | ncat -U $mon_sock