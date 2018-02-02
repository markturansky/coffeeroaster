#!/usr/bin/env bash

kill $(ps aux | grep '[p]ython' | awk '{print $2}')
