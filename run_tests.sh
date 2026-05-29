#!/bin/bash

set -e

VERSIONS="3.8 3.9 3.10 3.11 3.12 3.13 3.14"
FAILED=""

for v in $VERSIONS; do
    echo "=== Python $v ==="
    if uv run --python "$v" --with pytest,pytest-cov,requests \
        pytest tests/ --cov=matterhook --cov-report=term-missing; then
        echo "=== Python $v: OK ==="
    else
        echo "=== Python $v: FAILED ==="
        FAILED="$FAILED $v"
    fi
    echo
done

if [ -n "$FAILED" ]; then
    echo "FAILED versions:$FAILED"
    exit 1
else
    echo "All versions passed."
fi
