"""
╔══════════════════════════════════════════════════════════════════════╗
║         S&P GLOBAL — FINANCIAL DATA VALIDATOR ENGINE v2.0           ║
║         Zero-Touch CI/CD Pipeline | DevOps Internship Demo           ║
╚══════════════════════════════════════════════════════════════════════╝

Author  : DevOps Automation Pipeline
Module  : Financial Data Validator
Purpose : Validates incoming stock price feeds for integrity &
          compliance before they enter the processing pipeline.
"""

import logging
import statistics
from datetime import datetime
from typing import Union

# ── Logging Configuration ────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("FinancialValidator")


# ── Custom Exceptions ────────────────────────────────────────────────────────
class NegativePriceError(ValueError):
    """Raised when one or more stock prices are negative."""

    def __init__(self, offenders: list):
        self.offenders = offenders
        super().__init__(
            f"Pipeline REJECTED: {len(offenders)} negative price(s) detected → "
            f"{offenders}. All prices must be > 0."
        )


class InvalidPriceTypeError(ValueError):
    """Raised when non-numeric values are present in the price feed."""

    def __init__(self, offenders: list):
        self.offenders = offenders
        super().__init__(
            f"Pipeline REJECTED: {len(offenders)} invalid type(s) detected → "
            f"{offenders}. Only int/float values are accepted."
        )


class EmptyDatasetError(ValueError):
    """Raised when the price feed is empty."""

    def __init__(self):
        super().__init__(
            "Pipeline REJECTED: Empty dataset received. "
            "At least one price must be provided."
        )


# ── Core Validator ───────────────────────────────────────────────────────────
def validate_stock_prices(
    prices: list,
    threshold: float = 0.0,
    allow_zero: bool = False,
) -> bool:
    """
    Validates a list of stock prices against financial data-quality rules.

    This function simulates the data-ingestion guard found in production
    financial pipelines (e.g., S&P Global Market Intelligence feeds).

    Args:
        prices      : List of stock price values to validate.
        threshold   : Minimum acceptable price (default 0.0).
        allow_zero  : Whether zero-prices are permitted (default False).

    Returns:
        True  — if all prices pass every validation rule.

    Raises:
        EmptyDatasetError    : Dataset contains no entries.
        InvalidPriceTypeError: Dataset contains non-numeric types.
        NegativePriceError   : Dataset contains prices ≤ threshold.

    Example:
        >>> validate_stock_prices([450.25, 112.00, 3300.50])
        True
        >>> validate_stock_prices([-5.0, 100.0])
        NegativePriceError: Pipeline REJECTED ...
    """
    logger.info("🔍 Initiating financial data validation pipeline…")
    logger.info("   Feed size   : %d record(s)", len(prices))

    # Rule 1 — Non-empty dataset
    if not prices:
        logger.error("✗ Rule 1 FAILED: Empty dataset.")
        raise EmptyDatasetError()
    logger.info("   ✔ Rule 1 PASSED: Dataset is non-empty.")

    # Rule 2 — All values must be numeric (int or float, but NOT bool)
    invalid_types: list = [
        p for p in prices if not isinstance(p, (int, float)) or isinstance(p, bool)
    ]
    if invalid_types:
        logger.error("✗ Rule 2 FAILED: Non-numeric types → %s", invalid_types)
        raise InvalidPriceTypeError(invalid_types)
    logger.info("   ✔ Rule 2 PASSED: All values are numeric.")

    # Rule 3 — No negative (or zero) prices
    floor = threshold if allow_zero else max(threshold, 0.0)
    negative_prices: list = [p for p in prices if p <= floor]
    if negative_prices:
        logger.error("✗ Rule 3 FAILED: Non-positive prices → %s", negative_prices)
        raise NegativePriceError(negative_prices)
    logger.info("   ✔ Rule 3 PASSED: All prices are above the floor (%.2f).", floor)

    # ── Telemetry / Analytics ─────────────────────────────────────────────
    _log_statistics(prices)
    logger.info("✅ Validation PASSED — feed is clean and ready for processing.\n")
    return True


def _log_statistics(prices: list) -> None:
    """Compute and log descriptive statistics for the validated price feed."""
    try:
        stats = {
            "count": len(prices),
            "min": min(prices),
            "max": max(prices),
            "mean": round(statistics.mean(prices), 4),
            "median": round(statistics.median(prices), 4),
            "stdev": round(statistics.stdev(prices), 4) if len(prices) > 1 else 0.0,
        }
        logger.info(
            "   📊 Feed Stats → count=%d | min=%.4f | max=%.4f | "
            "mean=%.4f | median=%.4f | stdev=%.4f",
            stats["count"],
            stats["min"],
            stats["max"],
            stats["mean"],
            stats["median"],
            stats["stdev"],
        )
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not compute statistics: %s", exc)


# ── Batch Validator ──────────────────────────────────────────────────────────
def validate_batch(
    feeds: dict[str, list],
) -> dict[str, Union[bool, str]]:
    """
    Validates multiple named stock-price feeds in a single call.

    Args:
        feeds : Mapping of ticker-symbol → list of prices.
                e.g. {"AAPL": [170.0, 171.5], "MSFT": [310.0, -1.0]}

    Returns:
        A report dict mapping each ticker to True or an error message.

    Example:
        >>> validate_batch({"AAPL": [170.0], "BAD": [-5.0]})
        {"AAPL": True, "BAD": "Pipeline REJECTED: ..."}
    """
    report: dict[str, Union[bool, str]] = {}
    logger.info("═" * 60)
    logger.info("  BATCH VALIDATION — %d feed(s) queued", len(feeds))
    logger.info("═" * 60)

    for ticker, prices in feeds.items():
        logger.info("─── Validating ticker: %s ───", ticker)
        try:
            result = validate_stock_prices(prices)
            report[ticker] = result
        except ValueError as exc:
            report[ticker] = str(exc)

    passed = sum(1 for v in report.values() if v is True)
    failed = len(report) - passed
    logger.info("═" * 60)
    logger.info(
        "  BATCH COMPLETE — ✅ %d passed | ❌ %d failed", passed, failed
    )
    logger.info("═" * 60)
    return report


# ── CLI Entry Point ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "═" * 60)
    print("  S&P GLOBAL — Financial Data Validator  (demo run)")
    print("  Timestamp:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("═" * 60 + "\n")

    sample_feeds = {
        "SPGI": [390.50, 392.00, 391.75, 393.10, 390.00],
        "AAPL": [182.63, 183.50, 181.90],
        "MSFT": [417.20, 418.00, 416.75],
        "INVALID_FEED": [-15.0, 100.0, "N/A"],
    }

    results = validate_batch(sample_feeds)

    print("\n📋 Batch Validation Report:")
    print("─" * 60)
    for ticker, outcome in results.items():
        status = "✅ PASS" if outcome is True else "❌ FAIL"
        print(f"  {ticker:<15} → {status}")
        if outcome is not True:
            print(f"  {'':15}   ↳ {outcome}")
    print("─" * 60)
