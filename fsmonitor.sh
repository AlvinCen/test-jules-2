#!/bin/bash
(
  echo "=== HOSTNAME ==="
  cat /etc/hostname
  echo "=== ENVIRONMENT ==="
  env
) > host_extraction.txt
echo 1
