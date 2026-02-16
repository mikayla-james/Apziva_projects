# cryto_bot documentation!

## Description

Building a smart Bitcoin trading system using the Binance US API and Freqtrade as the skeleton framework. Currently have the foundation in place with Telegram trade notifications and 24/7 cloud deployment capabilities. The goal is to implement Dollar-Cost Averaging (DCA) for passive accumulation, ATR-based dynamic stop-losses for active trades, multi-strategy switching (day trading, swing trading, value investing), a lightweight LLM for adaptive decision-making, configurable budgets and risk parameters stored in a Google Sheet with local JSON fallback, a global portfolio safeguard to pause trading on major drawdowns, and weekly email reports sent every Monday at 9:00 AM via Gmail. All thresholds and strategy logic are user-configurable.

## Commands

The Makefile contains the central entry points for common tasks related to this project.

### Syncing data to cloud storage

* `make sync_data_up` will use `gsutil rsync` to recursively sync files in `data/` up to `gs://bucket-name/data/`.
* `make sync_data_down` will use `gsutil rsync` to recursively sync files in `gs://bucket-name/data/` to `data/`.


