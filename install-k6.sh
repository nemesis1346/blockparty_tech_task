#!/bin/bash
set -e  # Exit on error

# 1. Install Go (if missing)
if ! command -v go &> /dev/null; then
    echo "Installing Go..."
    brew install go  # For Mac
    # sudo apt install -y golang  # For Linux
fi

# 2. Set Go environment
export GOPATH="$HOME/go"
export PATH="$PATH:$GOPATH/bin"
export GO111MODULE=on

# 3. Install xk6 builder
echo "Installing xk6..."
go install go.k6.io/xk6/cmd/xk6@v0.16.1  # Specific stable version

# 4. Build k6 with Python support using the MAIN BRANCH
echo "Building k6 with Python extension..."
~/go/bin/xk6 build \
    --with github.com/grafana/xk6-python@main \
    --output ./k6

# 5. Verify
if [ -f "./k6" ]; then
    echo -e "\n\033[32mSuccess!\033[0m Custom k6 binary built at: $(pwd)/k6"
    ./k6 version
    echo -e "\nTest Python support with:"
    echo "  echo 'def default(): print(\"Python works!\")' | ./k6 run -"
else
    echo -e "\n\033[31mBuild failed!\033[0m Check errors above"
    exit 1
fi