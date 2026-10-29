#!/bin/bash
echo "=== Test 1: Minimal VFS ==="
./run.sh --vfs tests/test_vfs_minimal.json \
    --script tests/test_script1.sh

echo -e "\n=== Test 2: Complex VFS ==="
./run.sh --vfs tests/test_vfs_complex.json \
    --script tests/test_all.sh

echo -e "\n=== Test 3: VFS not found ==="
./run.sh --vfs tests/nonexistent.json

echo -e "\n=== Test 4: Invalid JSON ==="
echo "not json {" > tests/invalid.json
./run.sh --vfs tests/invalid.json
rm -f tests/invalid.json

echo -e "\n=== All tests completed ==="
