#!/bin/bash
mkdir -p workdir
git clone https://github.com/B2R2-org/B2R2.git
dotnet build -c Release ./B2R2
