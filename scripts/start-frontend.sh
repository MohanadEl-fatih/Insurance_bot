#!/bin/bash
# Start the Next.js frontend

cd "$(dirname "$0")/../frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Start the dev server
echo "Starting Next.js frontend on http://localhost:3000"
npm run dev

