#!/usr/bin/env bash
set -u

BASE_URL="${BASE_URL:-http://localhost:8080}"

if [[ -z "${ADMIN_USERNAME:-}" || -z "${ADMIN_PASSWORD:-}" ]]; then
  echo "Set ADMIN_USERNAME and ADMIN_PASSWORD in your shell before running this script."
  echo 'Example: source .env'
  exit 2
fi

pass=0
fail=0

check() {
  local name="$1"
  local expected="$2"
  local actual="$3"

  if [[ "$actual" == "$expected" ]]; then
    echo "PASS: $name ($actual)"
    pass=$((pass + 1))
  else
    echo "FAIL: $name (expected $expected, got $actual)"
    fail=$((fail + 1))
  fi
}

status="$(curl -s -o /dev/null -w '%{http_code}' "$BASE_URL/")"
check "Public application reachable through reverse proxy" "200" "$status"

status="$(curl -s -o /dev/null -w '%{http_code}' "$BASE_URL/health")"
check "Public health route works through reverse proxy" "200" "$status"

status="$(curl -s -o /dev/null -w '%{http_code}' "$BASE_URL/admin/")"
check "Protected admin blocks unauthenticated request" "401" "$status"

status="$(curl -s -o /dev/null -w '%{http_code}' -u "$ADMIN_USERNAME:$ADMIN_PASSWORD" "$BASE_URL/admin/")"
check "Protected admin allows authenticated request" "200" "$status"

echo
echo "Results: $pass passed, $fail failed"

if (( fail > 0 )); then
  exit 1
fi
