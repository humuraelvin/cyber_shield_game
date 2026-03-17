#!/usr/bin/env bash
set -e

# Development helper to run the full client wrapper on Linux.
# This lets you test the consent UI and background shell client.

python3 -m game_client.game_main
