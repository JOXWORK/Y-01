#!/usr/bin/env bash

set -e

echo "Run applying migrations"
alembic upgrade head
echo "Migration were successfully applied!"

exec "$@"