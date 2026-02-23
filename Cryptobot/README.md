# Freqtrade Setup Guide (Reconstructed from My Setup Journey)

## Prerequisites

- **Docker Desktop** installed and running
- **VS Code** with the **Dev Containers** extension (the Udemy course uses a devcontainer)
- A **Binance US** account with API access
- A **Telegram** account (for bot notifications)

---

## Step 1: Clone Freqtrade & Set Up Docker Environment

The Udemy course uses Freqtrade's devcontainer setup. This gives you a full development environment inside Docker with everything pre-installed.

```bash
# Clone the freqtrade repo
git clone https://github.com/freqtrade/freqtrade.git

# Create the workspace directory
mkdir ft_userdata
cd ft_userdata/

# Download the docker-compose file
curl https://raw.githubusercontent.com/freqtrade/freqtrade/stable/docker-compose.yml -o docker-compose.yml

# Pull the freqtrade image
docker compose pull

# Create the user data directory structure
docker compose run --rm freqtrade create-userdir --userdir user_data
```

Then open the `ft_userdata` folder in VS Code, and when prompted, **Reopen in Container**. This drops you into the devcontainer as `ftuser` at `/workspaces/ft_userdata/`.

> **If using the devcontainer:** Commands run directly (no `docker compose run --rm` prefix needed). If running outside the container, prefix commands with `docker compose run --rm freqtrade`.

---

## Step 2: Create Initial Config

```bash
# Interactive config creation — answer the prompts
freqtrade new-config --config user_data/config.json
```

Or just manually create/edit `user_data/config.json`. 
My final structure:

```json
{
    "$schema": "https://schema.freqtrade.io/schema.json",
    "trading_mode": "spot",
    "margin_mode": "isolated",
    "max_open_trades": 5,
    "stake_currency": "USDT",
    "stake_amount": 200,
    "tradable_balance_ratio": 1,
    "fiat_display_currency": "USD",
    "dry_run": true,
    "timeframe": "30m",
    "dry_run_wallet": 1000,
    "cancel_open_orders_on_exit": true,
    "unfilledtimeout": {
        "entry": 10,
        "exit": 30
    },
    "exchange": {
        "name": "binanceus",
        "key": "YOUR_API_KEY_HERE",
        "secret": "YOUR_API_SECRET_HERE",
        "ccxt_config": {},
        "ccxt_async_config": {},
        "pair_whitelist": [
            "BTC/USDT",
            "ETH/USDT"
        ],
        "pair_blacklist": [
            "BNB/*"
        ]
    },
    "entry_pricing": {
        "price_side": "same",
        "use_order_book": true,
        "order_book_top": 1,
        "price_last_balance": 0.0,
        "check_depth_of_market": {
            "enabled": false,
            "bids_to_ask_delta": 1
        }
    },
    "exit_pricing": {
        "price_side": "other",
        "use_order_book": true,
        "order_book_top": 1
    },
    "pairlists": [
        {
            "method": "StaticPairList"
        }
    ],
    "telegram": {
        "enabled": true,
        "token": "YOUR_TELEGRAM_BOT_TOKEN",
        "chat_id": "YOUR_CHAT_ID",
        "allow_custom_messages": true,
        "notification_settings": {
            "status": "silent",
            "warning": "on",
            "startup": "off",
            "entry": "silent",
            "entry_fill": "on",
            "entry_cancel": "silent",
            "exit": {
                "roi": "silent",
                "emergency_exit": "on",
                "force_exit": "on",
                "exit_signal": "silent",
                "trailing_stop_loss": "on",
                "stop_loss": "on",
                "stoploss_on_exchange": "on",
                "custom_exit": "silent",
                "partial_exit": "on",
                "*": "off"
            },
            "exit_cancel": "on",
            "exit_fill": "off",
            "protection_trigger": "off",
            "protection_trigger_global": "on",
            "strategy_msg": "off",
            "show_candle": "off"
        },
        "reload": true,
        "balance_dust_level": 0.01
    },
    "freqai": {
        "enabled": true,
        "purge_old_models": 2,
        "train_period_days": 15,
        "backtest_period_days": 7,
        "live_retrain_hours": 0,
        "identifier": "unique-id",
        "feature_parameters": {
            "include_timeframes": [
                "30m",
                "1h"
            ],
            "include_corr_pairlist": [
                "BTC/USDT",
                "ETH/USDT"
            ],
            "label_period_candles": 20,
            "include_shifted_candles": 2,
            "DI_threshold": 0.9,
            "weight_factor": 0.9,
            "principal_component_analysis": false,
            "use_SVM_to_remove_outliers": true,
            "indicator_periods_candles": [
                10,
                20
            ],
            "plot_feature_importances": 0
        },
        "data_split_parameters": {
            "test_size": 0.33,
            "random_state": 1
        },
        "model_training_parameters": {}
    },
    "bot_name": "",
    "force_entry_enable": true,
    "initial_state": "running",
    "internals": {
        "process_throttle_secs": 5
    }
}
```



---

## Step 3: Set Up Telegram Bot

1. Open Telegram, search for **@BotFather**
2. Send `/newbot` and follow the prompts to name your bot
3. Copy the **bot token** it gives you
4. To get your **chat_id**: search for **@userinfobot** on Telegram and it'll tell you your ID
5. Paste both into your config under the `"telegram"` section

---

## Step 4: Set Up Binance US API Keys

1. Log into Binance US
2. Go to API Management
3. Create a new API key

---

## Step 5: Download Historical Data

I originally wanted to use kraken, but kraken is currently incompatible with FreqAI.

```bash
freqtrade download-data -t 30m 1h --timerange 20240701-20260201 --config ./user_data/config.json
```

> **Note about Kraken:** If you ever switch to Kraken, their API only returns 720 candles max, so you're forced to use `--dl-trades` which downloads every individual trade and takes forever. Kraken also has a hardcoded incompatibility with FreqAI — Freqtrade blocks it entirely. 

---

## Step 6: Run Backtesting

```bash
freqtrade backtesting \
  --strategy ApzivaAI \
  --strategy-path freqtrade/templates \
  --config ./user_data/config.json \
  --freqaimodel LightGBMRegressor \
  --timerange 20251001-20251201
```

Key things to know about backtesting:
- It's a one-shot process — runs through historical data and exits
- **Telegram notifications DO NOT work** during backtesting (only in live/dry-run)
- FreqAI models get trained on the historical data during backtesting
- For the sake of customization I made my own streategy
- You can make a stategy using: `freqtrade new-strategy --strategy Apziva_freqai --template minimal` or copying and pasting from a pre-established strategy. Just ensure you change class name (ex"**class  ApzivaAI(IStrategy)**)

---

## Step 7: Run in Dry-Run Mode (Paper Trading)

This is where the bot actually runs live with fake money:

```bash
freqtrade trade \
--strategy ApzivaAI \
--strategy-path ./user_data/strategies/ \
 --config ./user_data/config.json \
 -- freqaimodel LightGBMRegressor
```

### What's different from backtesting:
- **No `--timerange`** — the bot runs continuously from now onward
- **Telegram works** — you'll get notifications for entries/exits
- **FreqAI retrains** on live data
- The bot loops every 5 seconds (or whatever `process_throttle_secs` is set to)
- **It's normal** for the log to repeat similar output every cycle — it's checking for signals

### If you need to merge multiple config files:

```bash
freqtrade trade \
  --strategy FreqaiExampleStrategy \
  --strategy-path freqtrade/templates \
  --config ./user_data/config.json \
  --config ./user_data/config_freqai.example.json \
  --freqaimodel LightGBMRegressor
```

Freqtrade merges multiple `--config` files — the second one overlays on top of the first.

### Running in the background:

```bash
screen -S freqtrade
freqtrade trade --strategy FreqaiExampleStrategy --strategy-path freqtrade/templates --config ./user_data/config.json --freqaimodel LightGBMRegressor
# Ctrl+A, D to detach
# screen -r freqtrade to reattach later
```

---

## Lessons Learned / Gotchas


### 1. Kraken doesn't work with FreqAI
Kraken's API limit of 720 OHLCV candles is hardcoded as a block in Freqtrade for FreqAI. There's no workaround — it's a known issue (GitHub issues #11398, #11526). Use Binance US instead.

### 2. Kraken Pro is free
If you ever want to use Kraken for non-FreqAI stuff: "Kraken Pro" is just the name of their advanced trading interface, not a paid tier. API keys are created at pro.kraken.com → Settings → API.

### 3. Telegram only works in live/dry-run mode
Backtesting doesn't connect to Telegram. Don't troubleshoot Telegram config while backtesting.

### 4. Data timeframes must match FreqAI config
If your FreqAI config has `"include_timeframes": ["30m", "1h"]`, your downloaded data needs those timeframes. If you only downloaded 1d candles, convert existing trade data:
```bash
freqtrade trades-to-ohlcv --config ./user_data/config.json -t 30m 1h
```

---

## File Structure

```
ft_userdata/
├── docker-compose.yml
├── user_data/
│   ├── config.json              # Main bot config
│   ├── strategies/              # Strategy files go here
│   ├── data/
│   │   └── binanceus/           # Downloaded market data
│   ├── logs/
│   │   └── freqtrade.log
│   └── models/                  # FreqAI trained models
└── freqtrade/
    └── templates/
        └── FreqaiExampleStrategy.py  # Example FreqAI strategy
```
