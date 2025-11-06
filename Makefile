# PowerShell als Shell
SHELL := powershell.exe
.SHELLFLAGS := -NoLogo -NoProfile -ExecutionPolicy Bypass -Command
.ONESHELL:

# Static Variables
LEAN_EXE := C:\Users\chris\pipx\venvs\lean\Scripts\lean.exe

.PHONY: push backtest copy switch-spy switch-vola list-strategies

all: test

copy:
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		$$current = Get-Location; \
		$$parent = Split-Path -Parent $$current; \
		$$deployPath = Join-Path $$parent 'QC_Trading_Framework_DEPLOY'; \
		Write-Host 'Copying essential files from DEV to DEPLOY...'; \
		if (!(Test-Path $$deployPath)) { New-Item -ItemType Directory -Path $$deployPath -Force }; \
		Copy-Item -Path 'main.py' -Destination \"$$deployPath\\main.py\" -Force; \
		Copy-Item -Path 'active_strategy.py' -Destination \"$$deployPath\\active_strategy.py\" -Force; \
		Copy-Item -Path 'framework' -Destination \"$$deployPath\\framework\" -Recurse -Force; \
		Copy-Item -Path 'config.json' -Destination \"$$deployPath\\config.json\" -Force; \
		if (Test-Path 'research.ipynb') { Copy-Item -Path 'research.ipynb' -Destination \"$$deployPath\\research.ipynb\" -Force }; \
		Write-Host \"Files copied successfully to $$deployPath\" \
	"

# Strategy switching commands
switch-spy:
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		Copy-Item -Path 'strategies\\spy_ema_strategy.py' -Destination 'active_strategy.py' -Force; \
		Write-Host 'Switched to SPY EMA Strategy'; \
		Write-Host 'Run \"make push\" to deploy to QuantConnect' \
	"

switch-vola:
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		if (Test-Path 'strategies\\vola_breakout_strategy.py') { \
			Copy-Item -Path 'strategies\\vola_breakout_strategy.py' -Destination 'active_strategy.py' -Force; \
			Write-Host 'Switched to Vola Breakout Strategy'; \
			Write-Host 'Run \"make push\" to deploy to QuantConnect' \
		} else { \
			Write-Host 'ERROR: strategies\\vola_breakout_strategy.py not found' \
		} \
	"

list-strategies:
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		Write-Host 'Available Strategies:'; \
		Write-Host '=================='; \
		Get-ChildItem -Path 'strategies\\*.py' | ForEach-Object { \
			Write-Host ('  - ' + $$_.BaseName) \
		}; \
		Write-Host ''; \
		Write-Host 'Current Active Strategy:'; \
		if (Test-Path 'active_strategy.py') { \
			$$content = Get-Content 'active_strategy.py' -Head 10; \
			$$strategyLine = $$content | Where-Object { $$_ -match 'class.*Strategy' } | Select-Object -First 1; \
			if ($$strategyLine) { \
				$$className = ($$strategyLine -split 'class ')[1] -split '\\(' | Select-Object -First 1; \
				Write-Host ('  Active: ' + $$className) \
			} else { \
				Write-Host '  Active: Unknown' \
			} \
		} else { \
			Write-Host '  Active: None (active_strategy.py not found)' \
		} \
	"

logs:
	python "D:\QC\create_readable_logs.py"
	
push: copy
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		$$parent = Split-Path -Parent (Get-Location); \
		Write-Host \"Pushing QC_Trading_Framework_DEPLOY to QuantConnect...\"; \
		Set-Location -LiteralPath $$parent; \
		& '$(LEAN_EXE)' cloud push --project QC_Trading_Framework_DEPLOY \
	"

backtest:
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		$$parent = Split-Path -Parent (Get-Location); \
		Write-Host \"Running backtest for QC_Trading_Framework_DEPLOY...\"; \
		Set-Location -LiteralPath $$parent; \
		& '$(LEAN_EXE)' cloud backtest QC_Trading_Framework_DEPLOY \
	"

backtest-with-summary: backtest
	python extract_performance.py

backtest-enhanced:
	python backtest_with_analysis.py

results:
	python extract_performance.py

calculate-performance:
	python calculate_performance.py