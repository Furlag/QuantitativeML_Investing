# QuantitativeML_Investing — Project Analysis

> **Date:** February 17, 2026  
> **Scope:** Deep technical audit of the entire codebase, architecture review, comparison with industry benchmarks, and a roadmap for future work.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Architecture Overview](#2-architecture-overview)
3. [Component Deep-Dive](#3-component-deep-dive)
   - 3.1 [Data Pipeline (`Database/`)](#31-data-pipeline)
   - 3.2 [Custom Library (`furlag_qlib`)](#32-custom-library-furlag_qlib)
   - 3.3 [Research / Test Workshop](#33-research--test-workshop)
   - 3.4 [Production Workshop](#34-production-workshop)
4. [Technical Stack & Dependencies](#4-technical-stack--dependencies)
5. [Feature Engineering Analysis](#5-feature-engineering-analysis)
6. [Model Architecture Analysis](#6-model-architecture-analysis)
7. [Strategy & Risk Management Analysis](#7-strategy--risk-management-analysis)
8. [Backtesting & Evaluation Analysis](#8-backtesting--evaluation-analysis)
9. [Comparison with Related Projects](#9-comparison-with-related-projects)
10. [Identified Issues & Technical Debt](#10-identified-issues--technical-debt)
11. [Roadmap: What Needs to Be Done Next](#11-roadmap-what-needs-to-be-done-next)
12. [Appendix A: File Map](#appendix-a-file-map)

---

## 1. Executive Summary

**QuantitativeML_Investing** is a quantitative trading research and production system built on top of Microsoft's **Qlib** framework (v0.9.7). The project applies machine‑learning models — primarily an Attention‑LSTM (ALSTM) with GRU backbone and LightGBM — to predict short‑term stock returns and convert those predictions into executable trading orders via a custom Kelly Criterion‑based portfolio strategy with ATR‑based stop‑loss risk management.

**Markets covered:** Spanish equities (IBEX 35 constituents and mid‑caps via Madrid Stock Exchange tickers `*.MC`) and US equities (S&P 500 / S&P 400 via `yfinance`/`yahooquery`).

**Current state of the project:**
- The **Spanish market pipeline** has reached a production-ready state with Train → Test → Predict notebooks, serialized artifacts, and order generation (including stop‑loss thresholds).
- The **US market pipeline** is still in the research/test phase with no production notebooks.
- A comprehensive **custom library** (`furlag_qlib`) has been developed with ~4,500 lines of code providing feature engineering (6 dataset variants with 50–175+ features), technical indicators, custom ALSTM model with epoch‑level checkpoint support, two trading strategies (Basic and Kelly Criterion), ATR‑based stop‑loss logic, custom data processors, and data filters.
- The **data pipeline** supports downloading, normalizing, and dumping data into Qlib's binary format from Yahoo Finance.
- **No automated execution**, **no CI/CD**, **no unit tests**, **no config-driven workflows**, and **no model registry** are in place yet.

---

## 2. Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                         Database/                            │
│  ┌──────────────┐   ┌──────────────────┐   ┌──────────────┐ │
│  │  yfinance /   │──▶│ CSV Source Files  │──▶│  dump_bin.py │ │
│  │  yahooquery   │   │  (per ticker)     │   │  (Qlib .bin) │ │
│  │  collectors   │   └──────────────────┘   └──────┬───────┘ │
│  └──────────────┘                                  │         │
│                                                    ▼         │
│  ┌──────────────────────────────────────────────────────────┐│
│  │           qlib_data_US / Qdata/SPAIN (Qlib binary DB)   ││
│  │  instruments/  calendars/  features/ (OHLCV .bin files)  ││
│  └──────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
                              │
                   Qlib init(provider_uri)
                              │
┌──────────────────────────────────────────────────────────────┐
│                  .Lib/furlag_qlib/ (Custom Library)           │
│  ┌─────────────┐ ┌───────────┐ ┌────────────┐ ┌───────────┐ │
│  │ qdatasets.py │ │qfilters.py│ │indicators.py│ │qprocessors│ │
│  │ (6 feature  │ │ (ES / US  │ │ (20+ TA    │ │.py        │ │
│  │  sets)      │ │  filters) │ │  indicators)│ │           │ │
│  └─────────────┘ └───────────┘ └────────────┘ └───────────┘ │
│  ┌─────────────┐ ┌───────────┐ ┌─────────────────────────┐  │
│  │strategies.py│ │stop_loss  │ │ model/                  │  │
│  │(Basic/Kelly)│ │.py (ATR)  │ │  pytorch_alstm_ts.py    │  │
│  │             │ │           │ │  pytorch_transformer_ts │  │
│  │             │ │           │ │  pytorch_tra.py         │  │
│  └─────────────┘ └───────────┘ └─────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Workshop/                                     │
│  ┌───────────────────────────────┐                              │
│  │        Test/                   │ Research notebooks           │
│  │  SPAIN/ (RNN, GB, StopLoss)   │ hyperparameter sweeps,       │
│  │  US/    (RNN, GB)             │ loop‑backtests per epoch      │
│  └───────────────────────────────┘                              │
│  ┌───────────────────────────────┐                              │
│  │     Production/                │ Deployable notebooks        │
│  │  SPAIN/D2D1/     (no SL)      │ Train → Test → Predict      │
│  │  SPAIN/D2D1_HSL/ (hard SL)    │ Orders.csv output           │
│  └───────────────────────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Deep-Dive

### 3.1 Data Pipeline

**Location:** `Database/scripts/data_collector/`

The data ingestion layer is a fork/adaptation of **Qlib's official data collectors** with custom extensions.

| Component | File | Purpose |
|-----------|------|---------|
| Base Collector | `base.py` (440 lines) | Abstract base class for all collectors. Handles multi‑threading, retry logic, CSV caching, parallel downloads via `joblib`. |
| Yahoo Collector | `yahoo/collector.py` (1018 lines) | Full‑featured collector using `yahooquery`. Supports 1min and 1d intervals, timezone conversion, index data. Originally from Qlib's contrib, contains US/CN/IN/BR market support. |
| yfinance Collector | `yfinance/collector.py` (~100 lines) | Simpler custom collector using `yfinance`. Downloads data in batches, supports appending market index columns (`*_idx` suffix), saves CSV files. |
| US Index Collector | `us_index/collector.py` (282 lines) | Scrapes Wikipedia for S&P 500 / S&P 400 / DJIA / NASDAQ‑100 constituent changes. Tracks index additions/removals over time. |
| Dump Bin | `dump_bin.py` (542 lines) | Converts CSV data into Qlib's proprietary binary format (`.bin`). Supports three modes: `dump_all` (fresh build), `dump_update` (append‑only), `dump_fix` (overwrite). |
| Update Script | `yfinance/update_database_us.py` | End‑to‑end update pipeline: reads instrument lists, downloads last 5 days of data, dumps to Qlib binary format. |

**Instrument Universe:**
- **US:** 504 S&P 500 tickers + 401 S&P 400 tickers (tab‑delimited instrument files with `1999-01-01` to `2099-12-31` date ranges)
- **Spain:** ~43 Spanish tickers hard-coded in `qfilters.py` (IBEX 35 + selected mid-caps)

**Key observations:**
- The US database at `Database/qlib_data_US/` currently only has `instruments/` directory — the actual feature `.bin` files are not committed (likely `.gitignore`‑d or stored separately).
- The Spain database lives at an external path `C:\Projects\Investing\QuantitativeML_Investing\Database\Qdata/SPAIN` (hardcoded in notebooks), not in this workspace.
- No automated scheduling (cron/task scheduler) for daily updates.
- Index constituent changes scraping (`us_index/collector.py`) is implemented but not integrated into the daily update workflow.

---

### 3.2 Custom Library (`furlag_qlib`)

**Location:** `.Lib/furlag_qlib/` (11 files, ~8,500+ lines total)

This is the core intellectual property of the project — a custom extension library on top of Qlib.

#### 3.2.1 Feature Engineering (`qdatasets.py` — 2,825 lines)

Six pre-built feature set functions, each returning `(fields, names)` tuples compatible with Qlib's expression engine:

| Function | Features | Used In | Description |
|----------|----------|---------|-------------|
| `dataset_features()` | ~175 | Not directly used | Base feature set (non‑time-series) |
| `dataset_features_ts()` | ~175 | Not found (alias reference `_ts_175`) | Time‑series version with lagged features |
| `dataset_features_ts_100_v1()` | ~100 | US GB (referenced as `_ts_100`) | Reduced feature set v1 |
| `dataset_features_ts_100_v2()` | ~100 | - | Reduced feature set v2 |
| `dataset_features_ts_50_v1()` | ~50 | US RNN | Minimal feature set v1 |
| `dataset_features_ts_50_v2()` | ~50 | - | Minimal feature set v2 |

**Feature categories (from largest set):**

| Category | Count (est.) | Examples |
|----------|-------------|----------|
| Basic OHLC ratios | ~12 | HIGH/CLOSE, OPEN/CLOSE, KBAR features |
| EMA-based (7 windows) | ~35 | Price vs EMA, EMA change, EMA acceleration, EMA cross ratios |
| SMA-based (7 windows) | ~35 | Price vs Mean, Mean change, Mean acceleration, Mean cross ratios |
| Statistical | ~15 | Std, Beta (Slope), Residuals, Quantiles, Rank |
| Directional count | ~20 | CNTP, CNTN, CNTD, SUMP |
| Technical indicators | ~25 | MACD, Bollinger, Stochastic, RSI, Aroon, CCI, ADX, CHOP, ATR, Bulls/Bears Power, MFI |
| OBV-based | ~4 | OBV change, OBV acceleration |
| Volume-based | ~15 | Volume variation, VMA, VSTD, CORRV, WVMA, CORDV |
| Market index | ~10 (opt) | Index SMA variations and cross ratios |

Every feature uses **ratio-based normalization** (e.g., `$close/EMA($close, 20)` rather than raw EMA) making features scale‑invariant across stocks — a well-designed practice.

Most features include 3 variants: *level*, *first derivative (change)*, and *second derivative (acceleration)* — providing the model with momentum and curvature information.

#### 3.2.2 Technical Indicators (`indicators.py` — 539 lines)

A `CommonIndicators` class providing Qlib expression‑language implementations of 20+ standard indicators:

- **Oscillators:** ROC, MACD, Stochastic Oscillator, Williams %R, RSI, Aroon (Up/Down/Oscillator), CCI
- **Trend:** Bollinger Bands, Ichimoku Cloud (5 components), ADX (+DI, -DI), CHOP
- **Volatility:** ATR, Bulls/Bears Power
- **Volume:** MFI, OBV, AD Line

Each indicator supports a `d` offset parameter for time-series lagged variants and an `adapt` mode that converts absolute indicators to ratio-based ones suitable for ML.

#### 3.2.3 Strategies (`strategies.py` — 546 lines)

Two trading strategies extending Qlib's `BaseStrategy`:

**`BasicStrategy`:**
- Fixed portfolio allocation (`investment_percentage = 10%` per position)
- Simple threshold-based buy/sell signals
- Buys top-scoring unheld stocks, sells held stocks below threshold
- 90% risk degree (max portfolio utilization)

**`KellyCriterionStrategy`** (primary strategy, ~350 lines):
- **Position sizing via Kelly Criterion adaptation:** Uses ATR-based stop-loss distance to determine position size. The formula: `cash_spend = (max_account_value_loss / max_per_stock_cash_loss) × close_price` — effectively sizing positions so the maximum loss per position (if stop-loss triggers) equals `investment_risk_degree × account_value` (default 1%).
- **Stop-loss integration:** Supports hard stop-loss (intra-day execution simulation), soft stop-loss (end-of-day signal), and trailing stop-loss.
- **Min/max investment caps:** Configurable as absolute amounts or percentage of portfolio.
- **Fractional shares support.**
- **Stock validation:** Optional liquidity filter (80-day average dollar volume > $3M).
- **Order generation:** Produces Qlib `Order` objects with direction, amount, time range, and factor.

#### 3.2.4 Stop-Loss System (`stop_loss.py` — 444 lines)

A full-featured stop-loss management system:

- **`StopLoss` class:** Maintains a dictionary of active stop-loss thresholds per stock. Uses two Qlib `DataHandler` instances: one for market data (OHLC), one for threshold computations.
- **`StopLossLogics` class:** Factory for stop-loss threshold expressions. Currently provides ATR-based stop-loss with configurable parameters:
  ```
  close - diff × ATR(r)
  ```
  Plus pre-built templates: `normal_atr`, `high_atr`, `low_atr`, `bollinger_band`.
- **Features:**
  - Initialize thresholds on position open
  - Update thresholds (trailing) — only ratchets up, never down (unless `down_trailing=True`)
  - Check for threshold breaches (hard: simulates intra-day sell at stop price; soft: signals end-of-day)
  - Persist/load thresholds via JSON
  - Theorical threshold computation for position sizing

#### 3.2.5 Models (`model/` — 3 models)

| Model | File | Lines | Status |
|-------|------|-------|--------|
| **ALSTM** | `pytorch_alstm_ts.py` | 383 | **Actively used** — Primary model for production and research |
| **Transformer** | `pytorch_transformer_ts.py` | 321 | Available but not used in any notebook |
| **TRA** (Temporal Routing Adaptor) | `pytorch_tra.py` | 936 | Available but not used in any notebook |

**ALSTM Architecture (in use):**
```
Input → FC(d_feat → hidden_size) → Tanh → GRU/LSTM(hidden_size, num_layers) → Attention → FC(2×hidden_size → 1)
```
- Input: `(batch, seq_len=20, d_feat=175)` for Spain, `(batch, seq_len=10, d_feat=50)` for US
- Attention mechanism: `FC(hidden_size → hidden_size/2) → Tanh → FC(hidden_size/2 → 1) → Softmax`
- Final output concatenates last hidden state and attention-weighted sum

**Custom additions to the Qlib ALSTM:**
- `train_n_epochs()`: Trains exactly N epochs and stores every epoch's state_dict (no early stopping), enabling post-training epoch selection.
- `load_model_at_epoch()`: Load any previously trained epoch's weights.
- `state_dicts` list: Complete checkpoint history for epoch-level model selection.

This is a clever design that allows loop-backtesting every epoch to find the optimal stopping point empirically — a form of **model selection via backtesting validation**.

#### 3.2.6 Data Processors (`qprocessors.py` — 26 lines)

- `DropLabelOutliners`: Custom processor that clips label values beyond a configurable threshold (symmetric or asymmetric). Currently commented out in most notebooks.

#### 3.2.7 Data Filters (`qfilters.py` — 88 lines)

- **Spain filter:** 3 rules — (1) 60+ trading days with volume > 0 in last 60 days, (2) exclude indices, (3) explicit whitelist of ~43 Spanish tickers
- **US filter:** 2 rules — (1) exclude ^GSPC index, (2) 120+ trading days with volume > 0 in last 120 days
- **Label filter generator:** Utility to create expression-based filters for extreme label values

**Note:** The notebooks reference `filters.basic` which doesn't exist in the current `qfilters.py` — this is a **bug or missing code**.

--- 
| `US_RNN_` | US | ALSTM (GRU) | 50 | EMA(5d fwd close)/EMA(5d close) - 1 | No |
| `US_GB` | US | LightGBM | 100 | EMA(7d fwd close)/EMA(7d close) - 1 | No |

**Key research patterns:**
- **Loop backtesting:** Trains N epochs, then loops through each epoch's model running full backtest + portfolio analysis, saving all metrics to `results.csv`. This allows visual inspection of overfitting and optimal epoch selection.
- **Hyperparameter tuning:** LightGBM notebooks use **Optuna** with SuccessiveHalving pruner for automated hyperparameter search.
- **Feature importance analysis:** LightGBM notebooks plot feature importances via seaborn.
- **Multiple label targets explored:**
  - `(Ref($open, -2) / Ref($open, -1)) - 1` → Day 2 open / Day 1 open return (D2D1)
  - `(EMA(Ref($open, -5), 5) / Ref($open, -1)) - 1` → EMA-smoothed 5d forward open return
  - `(EMA(Ref($close, -5), 5) / EMA($close, 5)) - 1` → EMA-smoothed 5d forward/backward close change

**Results (from `results.csv` — Spain RNN, 75 epoch sweep):**
- Best excess return without cost: ~14% annualized (epoch 27)
- Best information ratio without cost: ~1.08 (epoch 27)
- Best excess return with cost: ~4.9% annualized (epoch 27)
- Max drawdown range: -10% to -30% depending on epoch
- This validates that epoch selection materially impacts strategy performance.

---

### 3.4 Production Workshop

**Location:** `Workshop/Production/SPAIN/`

Two production-ready setups for the Spanish market:

#### D2D1 (Day 2 / Day 1 — without stop-loss execution)
- **Label:** `(Ref($open, -2) / Ref($open, -1)) - 1` — predicts the return from tomorrow's open to the next day's open
- **Model:** ALSTM (GRU), hidden=128, layers=2, batch=2048, lr=0.0001, seed=42
- **Features:** 175 time-series features, step_len=20
- **Training:** 2000–2018 (train), 2019–2021 (valid), 2019–2022 (test)
- **Epoch:** 26 (manually selected from loop backtest results)
- **Strategy:** Kelly Criterion, max_invest=25%, min_invest=€250, no active stop-loss execution
- **Artifacts:** Serialized dataset, datahandler, model, strategy (pickle)

#### D2D1_HardStopLoss (Same + hard stop-loss)
- Identical to D2D1 except:
  - **`hard_stop_loss = True`** — simulates intra-day stop-loss execution
  - **Epoch:** 9 (different optimal epoch due to different backtest dynamics)

**Predict.ipynb Workflow:**
1. Load pickled artifacts (model, dataset, strategy, datahandler)
2. Refresh data handler with current market data
3. Create new dataset for recent date range
4. Load account state from Excel (position + cash) or create fresh account
5. Set up exchange, signal, calendar infrastructure
6. Generate trade decision → list of buy/sell orders
7. Export to `Orders.csv` with stop-loss thresholds

**Orders.csv output format:**
```
stock_id, amount, start_time, end_time, direction, factor, stop_loss
SLR.MC, 83.0, 2022-03-23, ..., 1, , 18.12
MTS.MC, 68.0, 2022-03-23, ..., 1, , 25.92
```

---

## 4. Technical Stack & Dependencies

| Category | Technology | Version |
|----------|-----------|---------|
| Language | Python | 3.10.19 |
| ML Framework | PyTorch | (via pip) |
| Quant Framework | Qlib (pyqlib) | 0.9.7 |
| Gradient Boosting | LightGBM | 4.6.0 |
| Data Science | pandas, numpy, scipy, scikit-learn | 2.3.3, 2.2.6, 1.15.3, 1.7.2 |
| Data Source | yfinance, yahooquery | 1.1.0, 2.4.1 |
| Hyperparameter Tuning | Optuna | (via pip) |
| Experiment Tracking | MLflow | 3.9.0 |
| Visualization | Plotly, matplotlib, seaborn | (via pip) |
| Portfolio Optimization | CVXPY, Clarabel | 1.7.5, 0.11.1 |
| Model Serialization | skops | 0.13.0 |
| Web Scraping | BeautifulSoup4, fake-useragent | 4.14.3, 2.2.0 |
| Environment | Conda (miniconda3) | `qml` env |

**Notable:** MLflow is installed but **not actively used** — only Qlib's native `R` (Recorder) system is used for experiment tracking. CVXPY is installed but not used in any notebook (likely for future portfolio optimization).

---

## 5. Feature Engineering Analysis

### Strengths
- **Scale-invariant features:** All features are expressed as ratios or normalized values, eliminating the need for per-stock price scaling.
- **Multi-resolution:** Features span short-term (5-day) to long-term (200-day) windows.
- **Derivative features:** Systematic inclusion of change (1st derivative) and acceleration (2nd derivative) for all moving-average features — giving models momentum and curvature signals.
- **Comprehensive indicator coverage:** 20+ standard technical indicators adapted for ML (ratio-based where possible).
- **Multiple feature set sizes:** 50/100/175 feature variants allow matching complexity to data availability.

### Weaknesses
- **No fundamental/alternative data:** Purely price/volume based. No earnings, sentiment, macro, or sector data.
- **No cross-sectional features:** No relative strength vs sector/market, no rank-normalized features across the universe.
- **Hardcoded feature sets:** Each variant is a separate 300-500 line function with lots of code duplication. No composability or configuration.
- **Missing `dataset_features_ts_175()`:** Referenced in all production and RNN notebooks but not defined in the codebase — likely in a version not committed or a renamed function.
- **Missing `filters.basic`:** Referenced in Spain notebooks' filter pipe but not defined — will cause runtime errors.

---

## 6. Model Architecture Analysis

### ALSTM (Primary Model)

**Architecture quality:** The Attention-LSTM is a solid choice for time-series stock prediction, similar to what academic papers in quantitative finance have validated. The attention mechanism helps the model focus on relevant time steps.

**Hyperparameter choices (Spain production):**
| Parameter | Value | Assessment |
|-----------|-------|------------|
| hidden_size | 128 | Reasonable for 175 features |
| num_layers | 2 | Standard |
| dropout | 0 | **Risky** — no regularization for a model with ~60K+ parameters on limited data |
| batch_size | 2048 | Large — may reduce gradient noise too much |
| lr | 0.0001 | Conservative Adam learning rate |
| step_len | 20 | 20 trading days lookback (1 month) |
| loss | MSE | Standard for regression |

**Hyperparameter choices (US research):**
| Parameter | Value | Assessment |
|-----------|-------|------------|
| hidden_size | 32 | Much smaller — appropriate for 50 features |
| step_len | 10 | 2 weeks lookback |
| lr | 0.001 | 10x higher than Spain — may cause instability |

### LightGBM (Secondary Model)

Used in research notebooks with Optuna tuning. Well-configured with proper early stopping and validation-based tuning. Feature importance analysis is a good practice.

### Available but Unused Models

- **Transformer:** Full implementation exists but no notebook uses it. Transformers have shown strong results in recent financial ML literature.
- **TRA (Temporal Routing Adaptor):** Advanced architecture from Qlib research with router-based multi-state predictions. Not used.

---

## 7. Strategy & Risk Management Analysis

### Kelly Criterion Position Sizing

The implementation is a practical adaptation of the Kelly Criterion:
- Instead of using win/loss probabilities, it uses ATR-based risk management
- Position size = `(1% of portfolio value / ATR distance to stop) × close price`
- This means each position risks at most 1% of portfolio value if stop-loss triggers

**Assessment:** This is an industry-standard approach (not pure Kelly, but fixed-fractional risk). The 1% per-trade risk with 25% max position size is conservative and appropriate.

### Stop-Loss System

**Strengths:**
- Three modes (hard/soft/trailing) provide flexibility
- ATR-based thresholds adapt to volatility
- Proper intra-day simulation for hard stop-loss (checks if low price crossed threshold)
- Gap-down handling (uses open price if stop-loss > open)
- JSON persistence for live tracking

**Weaknesses:**
- **Slippage not modeled:** Hard stop-loss assumes execution at exact threshold price, which is unrealistic for illiquid Spanish mid-caps
- **No time-based stops:** No mechanism to exit after N days regardless of P&L
- **Single stop-loss per position:** No support for partial position exits or scaling out

---

## 8. Backtesting & Evaluation Analysis

### Methodology
- **Walk-forward:** Training period 2000–2018, validation 2019–2021, test 2019–2022. This is proper temporal splitting.
- **Cost modeling:** 5bps open + 5bps close + €2 minimum — realistic for Spanish retail brokerage.
- **Benchmark:** IBEX 35 (Spain), S&P 500 (US)
- **Metrics:** Excess return (with/without cost), information ratio, max drawdown, annualized return

### Concerns
- **Overlap between validation and test periods (2019–2021):** The validation set is used for early stopping / epoch selection, and then the same period is included in the test set. This is **leakage** — the effective out-of-sample period is only Oct 2021 to Oct 2022.
- **No cross-validation:** Single train/valid/test split. Rolling‑window or combinatorial purged cross‑validation would be more robust.
- **Survivorship bias:** The instrument universe uses current S&P 500/400 constituents with fixed date ranges (1999–2099), not accounting for delisted or removed stocks.
- **No transaction realism:** Orders assume infinite liquidity at deal price. No market impact model.

---

## 9. Comparison with Related Projects

### 9.1 Microsoft Qlib (Base Framework)

| Aspect | Qlib Default | This Project |
|--------|-------------|--------------|
| Feature sets | Alpha158 / Alpha360 | Custom 50/100/175 sets with derivatives |
| Models | LSTM, GRU, TabNet, ALSTM, TRA, etc. | Custom ALSTM (forked), LightGBM, Transformer, TRA |
| Strategy | TopK-DropK | Kelly Criterion with ATR stop-loss |
| Position sizing | Equal weight | Risk-based (Kelly/ATR) |
| Stop-loss | Not included | Full implementation (hard/soft/trailing) |
| Data | CN A-shares (built-in) | Spain + US custom |
| Workflow | YAML-config + CLI | Jupyter notebooks |

**Assessment:** This project has significantly enhanced Qlib's strategy layer with realistic risk management. The feature engineering is comparable but differently structured. The main gap is workflow automation.

### 9.2 FinRL (Deep Reinforcement Learning for Finance)

FinRL uses RL agents (PPO, A2C, DDPG) for portfolio allocation. Compared to this project:
- FinRL handles the action space (buy/sell/hold amounts) end-to-end via RL
- This project separates prediction (ML) from execution (rule-based strategy) — a more interpretable approach
- FinRL has better integration with live trading (Alpaca, Interactive Brokers)
- This project has more sophisticated risk management (stop-loss, Kelly sizing)

### 9.3 Zipline / Backtrader

Traditional event-driven backtesting frameworks:
- More mature backtesting infrastructure with proper event handling
- Less ML integration
- This project benefits from Qlib's factor expression engine, which is more ML-friendly than Zipline's pipeline API

### 9.4 QuantConnect / LEAN

Professional-grade platform:
- Full brokerage integration, live trading, multi-asset
- Cloud execution, backtesting-as-a-service
- This project is more research-oriented but has more custom ML components

### 9.5 Academic Comparisons

Recent papers on ML for stock prediction show:
- **Attention-LSTM** architectures similar to this project achieve ~0.05 IC (information coefficient) on Chinese A-shares
- **Key missing technique:** Cross-sectional momentum features, market-regime detection, and ensemble methods
- **Graph Neural Networks** (e.g., Qlib's RSR model) that model inter-stock relationships are a rising approach
- **Temporal Fusion Transformers (TFT)** show state-of-the-art results for multi-horizon forecasting

---

## 10. Identified Issues & Technical Debt

### Critical Issues

| # | Issue | Impact | Location |
|---|-------|--------|----------|
| 1 | **Missing `dataset_features_ts_175()` function** | All Spain production + test notebooks will fail | Referenced in 5 notebooks, not in `qdatasets.py` |
| 2 | **Missing `filters.basic` attribute** | All Spain notebooks reference it, not defined in `qfilters.py` | All Spain notebooks |
| 3 | **Hardcoded absolute paths** | `C:\Projects\Investing\QuantitativeML_Investing\...` won't work on any other machine | All notebooks |
| 4 | **Validation/test overlap** | Overly optimistic performance estimates | All notebooks (valid 2019–2021, test 2019–2022) |

### Code Quality Issues

| # | Issue | Impact |
|---|-------|--------|
| 5 | No unit tests for any component | Regressions go undetected |
| 6 | No type hints in custom library | Reduces IDE support and readability |
| 7 | Deprecated `df.append()` used in loop backtests | Will break with pandas ≥ 2.0 |
| 8 | `%` string formatting instead of f-strings | Minor readability issue |
| 9 | No docstrings on most functions in `qdatasets.py` | 2,825 lines with minimal documentation |
| 10 | Pickle serialization for artifacts | Security concern + fragile across library versions |

### Architecture Debt

| # | Issue | Impact |
|---|-------|--------|
| 11 | No configuration management (YAML/TOML) | Every experiment requires editing notebooks |
| 12 | No model registry or versioning | Can't track which model version generated which orders |
| 13 | No data validation pipeline | Corrupt data will silently propagate |
| 14 | No automated database updates | Manual process required |
| 15 | No logging framework integration | Print statements for debugging |
| 16 | Massive code duplication across notebooks | 6 notebooks share 80%+ identical code |
| 17 | MLflow installed but not used | Wasted dependency, missing experiment tracking benefits |

---

## 11. Roadmap: What Needs to Be Done Next

### Phase 1: Critical Fixes (Priority: Immediate)

1. **Fix missing functions/attributes:**
   - Add `dataset_features_ts_175()` function to `qdatasets.py` (likely an alias for `dataset_features_ts()`)
   - Add `basic` attribute to `Filters` class in `qfilters.py` (likely an empty list `[]`)
   
2. **Fix hardcoded paths:**
   - Use `pathlib.Path` with relative paths throughout
   - Use environment variables or config file for database paths
   - The US notebooks already partially do this with `Path().resolve().split("QuantitativeML_Investing")`

3. **Fix validation/test overlap:**
   - Separate validation (2019–2020) and test (2021–2022+) periods
   - Or use walk-forward validation

### Phase 2: Code Quality & Refactoring (Priority: High)

4. **Create configuration system:**
   - YAML/TOML config files per experiment (market, features, model, strategy, dates)
   - Single parameterized train/test/predict script instead of duplicated notebooks
   
5. **Consolidate notebooks into Python scripts:**
   - `train.py --config config/spain_d2d1.yaml`
   - `test.py --config config/spain_d2d1.yaml`
   - `predict.py --config config/spain_d2d1.yaml`
   
6. **Add unit tests:**
   - Feature engineering: verify feature count, no NaN in output
   - Strategy: verify order generation logic
   - Stop-loss: verify threshold calculations
   - Model: verify forward pass shapes
   
7. **Replace pickle with safer serialization:**
   - Use `torch.save()` for models (already done internally)
   - Use ONNX for cross-platform model deployment
   - Use Parquet for dataset state

8. **Integrate MLflow properly:**
   - Log hyperparameters, metrics, and artifacts
   - Model registry for production models
   - Compare experiments across markets/configurations

### Phase 3: Feature Enhancements (Priority: Medium)

9. **Expand to US production:**
   - Create `Workshop/Production/US/` with Train/Test/Predict notebooks
   - Adapt strategy parameters for US market characteristics (higher liquidity, different cost structure)

10. **Add cross-sectional features:**
    - Rank within sector
    - Relative strength vs market/sector
    - Cross-sectional momentum

11. **Add fundamental data:**
    - P/E, P/B, EV/EBITDA from Yahoo Finance
    - Earnings surprise
    - Analyst consensus

12. **Add alternative data:**
    - Sentiment (news/social media)
    - Macro indicators (VIX, yield curve, PMI)
    - Sector rotation indicators

13. **Explore unused models:**
    - Benchmark Transformer model against ALSTM
    - Try TRA architecture for multi-state regime detection
    - Ensemble methods (stack ALSTM + LightGBM + Transformer)

14. **Improve backtesting realism:**
    - Market impact model (e.g., Almgren-Chriss)
    - Slippage estimation based on bid-ask spread
    - Partial fill simulation
    - Transaction tax modeling

### Phase 4: Production & Automation (Priority: Medium-High)

15. **Automated daily pipeline:**
    - Scheduled task to update database daily
    - Auto-run prediction notebook
    - Email/Telegram alerts for generated orders
    
16. **Live trading integration:**
    - Broker API integration (Interactive Brokers, Degiro for Spain)
    - Order management system
    - Real-time position tracking
    - Stop-loss order placement with broker

17. **Monitoring & alerting:**
    - Model performance degradation detection
    - Data quality checks (missing data, stale prices)
    - Portfolio risk monitoring (drawdown, exposure, correlation)

### Phase 5: Advanced Research (Priority: Low-Medium)

18. **Walk-forward optimization:**
    - Rolling-window retraining with purged cross-validation
    - Model selection via out-of-sample Sharpe ratio
    
19. **Regime detection:**
    - Hidden Markov Model for market regime classification
    - Regime-conditional model selection or strategy parameters
    
20. **Portfolio optimization:**
    - Replace simple Kelly sizing with mean-variance optimization (CVXPY is already installed)
    - Risk parity, hierarchical risk parity (HRP)
    - Multi-objective optimization (return vs drawdown vs turnover)

21. **Graph-based models:**
    - Stock relationship graphs (co-movement, supply chain)
    - GNN architectures like Qlib's RSR/HIST models

22. **Multi-horizon forecasting:**
    - Predict multiple horizons simultaneously (1d, 5d, 20d)
    - Use Temporal Fusion Transformer (TFT) architecture

---

## Appendix A: File Map

```
QuantitativeML_Investing/
├── _utils.ipynb                          # Utility: export conda environment
├── environment.yml                       # Conda environment (221 lines, 100+ packages)
├── QuantitativeML_Investing.code-workspace
├── README.md                             # Empty
│
├── .Lib/furlag_qlib/                     # Custom library (core IP)
│   ├── __init__.py                       # Empty
│   ├── qdatasets.py                      # Feature engineering (2,825 lines, 6 variants)
│   ├── qfilters.py                       # Data filters (88 lines, Spain/US)
│   ├── qprocessors.py                   # Custom processors (26 lines)
│   ├── indicators.py                    # Technical indicators (539 lines, 20+ indicators)
│   ├── strategies.py                    # Trading strategies (546 lines, Basic/Kelly)
│   ├── stop_loss.py                     # Stop-loss system (444 lines)
│   └── model/
│       ├── pytorch_utils.py             # Model utilities (35 lines)
│       ├── pytorch_alstm_ts.py          # Attention-LSTM (383 lines) ★ Primary model
│       ├── pytorch_transformer_ts.py    # Transformer (321 lines) — Unused
│       └── pytorch_tra.py              # TRA (936 lines) — Unused
│
├── Database/
│   ├── scripts/
│   │   ├── dump_bin.py                  # CSV → Qlib binary converter (542 lines)
│   │   └── data_collector/
│   │       ├── base.py                  # Abstract base collector (440 lines)
│   │       ├── utils.py                 # Collector utilities
│   │       ├── index.py                 # Index base class
│   │       ├── yahoo/
│   │       │   ├── collector.py         # Yahoo Finance collector (1018 lines)
│   │       │   └── create_database.ipynb
│   │       ├── yfinance/
│   │       │   ├── collector.py         # yfinance collector (~100 lines)
│   │       │   ├── update_database_us.py # US update script
│   │       │   └── create_database_us.ipynb
│   │       └── us_index/
│   │           └── collector.py         # S&P 500/400 scraper (282 lines)
│   └── qlib_data_US/
│       └── instruments/
│           ├── sp500_only_new.txt       # 504 tickers
│           └── sp400_only_new.txt       # 401 tickers
│
└── Workshop/
    ├── Test/                            # Research notebooks
    │   ├── SPAIN/
    │   │   ├── SPAIN_GB.ipynb           # LightGBM + Optuna
    │   │   ├── SPAIN_RNN_.ipynb         # ALSTM baseline
    │   │   ├── SPAIN_RNN_StopLoss.ipynb # ALSTM + hard stop-loss
    │   │   ├── SPAIN_RNN_TrailingStopLoss.ipynb # ALSTM + trailing stop-loss
    │   │   └── results.csv              # Epoch sweep results (75 rows)
    │   └── US/
    │       ├── US_GB.ipynb              # LightGBM for US
    │       └── US_RNN_.ipynb            # ALSTM for US
    │
    └── Production/                      # Deployable workflows
        └── SPAIN/
            ├── D2D1/                    # Day-to-day returns, no active stop-loss
            │   ├── Train.ipynb
            │   ├── Test.ipynb
            │   ├── Predict.ipynb        # → Orders.csv
            │   ├── Orders.csv           # Latest generated orders
            │   └── artifacts/           # Serialized model/strategy (gitignored)
            └── D2D1_HardStopLoss/       # Same + hard stop-loss execution
                ├── Train.ipynb
                ├── Test.ipynb
                ├── Predict.ipynb
                ├── Orders.csv
                └── artifacts/
```

---

*This document was generated through comprehensive analysis of 30+ source files totaling ~15,000+ lines of code, including custom library modules, data pipeline scripts, research notebooks, and production workflows.*
