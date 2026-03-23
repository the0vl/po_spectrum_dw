#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "Running Reddit ingestion (inflation)..."
python -m src.ingestion.reddit_producer inflation

echo "Running Reddit ingestion (healthcare)..."
python -m src.ingestion.reddit_producer healthcare -l 50 -t month

echo "Transforming to silver..."
python -m src.processing.reddit_transformer

echo "Running dbt..."
cd dbt_project && dbt run
