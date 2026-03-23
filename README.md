# po_spectrum_dw

A data project on public opinion and rhetoric from different political stances, meant to serve in understanding public opinion regarding independent & concurrent political issues.

## Logger

New files should start like this:

```python
from src.utils.logger import get_logger

logger = get_logger(__name__)

def my_function():
    logger.info("Doing something cool...")
```

## Data Pipelines

### Market data (crypto prices)

- **Ingestion:** `python -m src.ingestion.producer` — fetches from CoinGecko, saves to `data/raw/`
- **Transformation:** `python -m src.processing.transformer` — cleans and flattens to `data/processed/`

### Reddit posts by keyword

- **Ingestion:** `python -m src.ingestion.reddit_producer <keyword>` — fetches Reddit posts via PRAW, saves to `data/raw/reddit_posts_{keyword}_{timestamp}.json`
- **Transformation:** `python -m src.processing.reddit_transformer` — flattens to `data/processed/reddit_posts_silver_{timestamp}.csv`

**Reddit producer options:**

```bash
python -m src.ingestion.reddit_producer inflation
python -m src.ingestion.reddit_producer healthcare -l 50 -t month
```

- `-l, --limit` — max posts to fetch (default: 100)
- `-t, --time` — time window: `hour`, `day`, `week`, `month`, `year`, `all` (default: week)

### Run full Reddit pipeline

Runs ingestion (inflation + healthcare), transformation, and dbt:

```bash
./scripts/run_reddit_pipeline.sh
```

or

```bash
bash scripts/run_reddit_pipeline.sh
```

## Setup

### Environment variables (`.env`)

```bash
# CoinGecko (market data)
API_URL=https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true

# dbt
DBT_PROFILES_DIR=./dbt_project

# Reddit API (create a script app at https://www.reddit.com/prefs/apps)
# Redirect URI: http://localhost:8080
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
# Optional: REDDIT_USER_AGENT, REDDIT_SUBREDDIT (default: all), REDDIT_LIMIT (default: 100), REDDIT_TIME_FILTER (default: week)
```

Reddit API access requires [approval](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy).

### dbt

```bash
cd dbt_project && dbt run
```

**Models:**

- `reddit_posts` — view over Reddit silver CSVs (from `raw_reddit_posts.stg_reddit_posts`)
