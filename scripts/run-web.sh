#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
exec flutter run -d web-server --web-port 4006 --web-hostname 127.0.0.1 "$@"
