# PowerShell als Shell
SHELL := powershell.exe
.SHELLFLAGS := -NoLogo -NoProfile -ExecutionPolicy Bypass -Command
.ONESHELL:

.PHONY: push backtest copy switch-spy switch-vola list-strategies version-update backtest-enhanced dev-backtest test-table test

all: test

# Run unit tests
test:
	cd tests && python run_tests.py

# Version-controlled backtest with deployment verification
backtest-enhanced: copy push backtest-verify

version-update:
	@python make_version_update.py

backtest-verify:
	@python backtest_with_analysis.py

copy: version-update
	@python make_copy.py

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

switch-mtf:
	powershell -NoLogo -NoProfile -ExecutionPolicy Bypass -Command " \
		if (Test-Path 'strategies\\multi_timeframe_ema_strategy.py') { \
			Copy-Item -Path 'strategies\\multi_timeframe_ema_strategy.py' -Destination 'active_strategy.py' -Force; \
			Write-Host 'Switched to Multi-Timeframe EMA Strategy'; \
			Write-Host 'Run \"make push\" to deploy to QuantConnect' \
		} else { \
			Write-Host 'ERROR: strategies\\multi_timeframe_ema_strategy.py not found' \
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

pull:
	@python make_pull.py

push: copy
	@python make_push.py

backtest:
	@python backtest_with_analysis.py

dev-backtest:
	@python dev_backtest.py

test-table:
	@python test_table.py

results:
	@python extract_performance.py

calculate-performance:
	@python calculate_performance.py