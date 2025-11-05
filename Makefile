# PowerShell als Shell
SHELL := powershell.exe
.SHELLFLAGS := -NoLogo -NoProfile -ExecutionPolicy Bypass -Command
.ONESHELL:

# Static Variables
LEAN_EXE := C:\Users\chris\pipx\venvs\lean\Scripts\lean.exe

.PHONY: push backtest copy

all: test

copy:
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		$$current = Get-Location; \
		$$parent = Split-Path -Parent $$current; \
		$$projectName = Split-Path -Leaf $$current; \
		$$deployName = $$projectName -replace '_DEV$$', '_DEPLOY'; \
		$$deployPath = Join-Path $$parent $$deployName; \
		Write-Host 'Copying essential files from DEV to DEPLOY...'; \
		if (!(Test-Path $$deployPath)) { New-Item -ItemType Directory -Path $$deployPath -Force }; \
		Copy-Item -Path 'main.py' -Destination \"$$deployPath\\main.py\" -Force; \
		Copy-Item -Path 'config.json' -Destination \"$$deployPath\\config.json\" -Force; \
		if (Test-Path 'research.ipynb') { Copy-Item -Path 'research.ipynb' -Destination \"$$deployPath\\research.ipynb\" -Force }; \
		Write-Host \"Files copied successfully to $$deployPath\" \
	"

logs:
	python "D:\QC\create_readable_logs.py"
	
push: copy
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		$$current = Get-Location; \
		$$parent = Split-Path -Parent $$current; \
		$$projectName = Split-Path -Leaf $$current; \
		$$deployName = $$projectName -replace '_DEV$$', '_DEPLOY'; \
		Write-Host \"Pushing $$deployName to QuantConnect...\"; \
		Set-Location -LiteralPath $$parent; \
		& '$(LEAN_EXE)' cloud push --project $$deployName \
	"

backtest:
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		$$current = Get-Location; \
		$$parent = Split-Path -Parent $$current; \
		$$projectName = Split-Path -Leaf $$current; \
		$$deployName = $$projectName -replace '_DEV$$', '_DEPLOY'; \
		Write-Host \"Running backtest for $$deployName...\"; \
		Set-Location -LiteralPath $$parent; \
		& '$(LEAN_EXE)' cloud backtest $$deployName \
	"

backtest-with-summary: backtest
	python extract_performance.py

backtest-enhanced:
	python backtest_with_analysis.py

results:
	python extract_performance.py

calculate-performance:
	python calculate_performance.py