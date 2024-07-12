#!/bin/bash

# Check if IPFS daemon is running
if ipfs swarm peers &> /dev/null; then
  echo "IPFS daemon is already running."
else
  # Start IPFS daemon if not running
  echo "Starting IPFS daemon..."
  ipfs daemon &
  sleep 5 # Give the daemon some time to start
fi

# Now check again if IPFS daemon is running and display peers
if ipfs swarm peers &> /dev/null; then
  echo "Connected Peers:"
  ipfs swarm peers
else
  echo "Error: Unable to start IPFS daemon."
fi

