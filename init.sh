#!/bin/bash
mkdir -p workdir
git clone https://github.com/B2R2-org/B2R2.git
dotnet build -c Release ./B2R2
wget https://github.com/ethereum/solidity/releases/download/v0.8.19/solc-static-linux
