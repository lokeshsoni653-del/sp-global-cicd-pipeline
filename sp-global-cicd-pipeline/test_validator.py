"""
╔══════════════════════════════════════════════════════════════════════╗
║        S&P GLOBAL — FINANCIAL VALIDATOR TEST SUITE v2.0             ║
║        Zero-Touch CI/CD Pipeline | Automated Quality Gate           ║
╚══════════════════════════════════════════════════════════════════════╝

Test Coverage:
  ✅ Happy-path validation with real-world market data
  ❌ Rejection of negative prices
  ❌ Rejection of non-numeric / string values
  ❌ Rejection of empty datasets
  🔄 Batch validation across multiple tickers
  📊 Edge cases & boundary conditions
"""

import pytest

from validator import (
    EmptyDatasetError,
    InvalidPriceTypeError,
    NegativePriceError,
    validate_batch,
    validate_stock_prices,
)


# ═══════════════════════════════════════════════════════════════════════════════
#  FIXTURES — Shared test data simulating real S&P Global market feeds
# ═══════════════════════════════════════════════════════════════════════════════


@pytest.fixture
def valid_spgi_prices():
    """Real-world-like SPGI closing prices (USD)."""
    return [390.50, 392.00, 391.75, 393.10, 390.00]


@pytest.fixture
def valid_mixed_tickers():
    """Multi-asset price batch — all clean."""
    return {
        "SPGI": [390.50, 392.00, 391.75],
        "AAPL": [182.63, 183.50, 181.90],
        "MSFT": [417.20, 418.00, 416.75],
    }


@pytest.fixture
def invalid_batch():
    """Mixed batch — some clean, some dirty."""
    return {
        "SPGI": [390.50, 392.00],        # PASS
        "BAD1": [-15.0, 100.0],           # FAIL — negative
        "BAD2": [100.0, "N/A", 200.0],   # FAIL — string
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  GROUP 1 — VALID DATA (Happy Path)
# ═══════════════════════════════════════════════════════════════════════════════


class TestValidData:
    """Suite: All inputs are well-formed and should pass validation."""

    def test_standard_positive_prices(self, valid_spgi_prices):
        """
        GIVEN a list of positive float prices (SPGI market data)
        WHEN  validate_stock_prices() is called
        THEN  it must return True without raising any exception.
        """
        result = validate_stock_prices(valid_spgi_prices)
        assert result is True, "Expected True for a clean price feed."

    def test_single_price_entry(self):
        """A single valid price must pass validation."""
        assert validate_stock_prices([100.0]) is True

    def test_integer_prices(self):
        """Integer prices (no decimal) must be accepted alongside floats."""
        assert validate_stock_prices([100, 200, 300]) is True

    def test_very_large_prices(self):
        """Handles high-value instruments like BRK.A (> $600,000/share)."""
        assert validate_stock_prices([600000.0, 601500.5, 599999.99]) is True

    def test_very_small_positive_prices(self):
        """Penny stocks (e.g., $0.01) must be accepted as valid."""
        assert validate_stock_prices([0.01, 0.05, 0.99]) is True

    def test_large_dataset_performance(self):
        """Validator handles large feeds (10,000 prices) without issue."""
        large_feed = [float(i + 1) for i in range(10_000)]
        assert validate_stock_prices(large_feed) is True


# ═══════════════════════════════════════════════════════════════════════════════
#  GROUP 2 — INVALID DATA (Rejection Tests)
# ═══════════════════════════════════════════════════════════════════════════════


class TestInvalidData:
    """Suite: Malformed inputs that must be rejected by the validator."""

    def test_negative_price_raises_error(self):
        """
        GIVEN a list containing a negative stock price
        WHEN  validate_stock_prices() is called
        THEN  a NegativePriceError must be raised.
        """
        with pytest.raises(NegativePriceError) as exc_info:
            validate_stock_prices([100.0, -50.0, 200.0])
        assert "-50.0" in str(exc_info.value)

    def test_all_negative_prices(self):
        """A feed with all negative values must raise NegativePriceError."""
        with pytest.raises(NegativePriceError):
            validate_stock_prices([-10.0, -20.0, -30.0])

    def test_zero_price_rejected_by_default(self):
        """
        Zero is not a valid market price (default allow_zero=False).
        Expect NegativePriceError for any price <= 0.
        """
        with pytest.raises(NegativePriceError) as exc_info:
            validate_stock_prices([0.0, 100.0])
        assert "0.0" in str(exc_info.value)

    def test_zero_price_allowed_when_flag_set(self):
        """When allow_zero=True, zero prices must be accepted."""
        assert validate_stock_prices([0.0, 100.0], allow_zero=True) is True

    def test_string_price_raises_error(self):
        """
        GIVEN a list containing a non-numeric string value
        WHEN  validate_stock_prices() is called
        THEN  an InvalidPriceTypeError must be raised.
        """
        with pytest.raises(InvalidPriceTypeError) as exc_info:
            validate_stock_prices([100.0, "N/A", 200.0])
        assert "N/A" in str(exc_info.value)

    def test_none_value_raises_error(self):
        """None values (e.g., missing data from API) must be rejected."""
        with pytest.raises(InvalidPriceTypeError):
            validate_stock_prices([100.0, None, 200.0])

    def test_boolean_values_rejected(self):
        """
        Booleans are a subclass of int in Python but are semantically
        invalid as stock prices; they must be rejected.
        """
        with pytest.raises(InvalidPriceTypeError):
            validate_stock_prices([True, False, 100.0])

    def test_mixed_invalid_types(self):
        """Feeds with both strings and None must surface both offenders."""
        with pytest.raises(InvalidPriceTypeError) as exc_info:
            validate_stock_prices([100.0, "ERR", None, 200.0])
        error_msg = str(exc_info.value)
        assert "ERR" in error_msg or "None" in error_msg

    def test_empty_list_raises_error(self):
        """
        GIVEN an empty list
        WHEN  validate_stock_prices() is called
        THEN  an EmptyDatasetError must be raised.
        """
        with pytest.raises(EmptyDatasetError):
            validate_stock_prices([])

    def test_negative_and_invalid_type_precedence(self):
        """
        Type errors take precedence over sign errors.
        InvalidPriceTypeError raised before NegativePriceError.
        """
        with pytest.raises(InvalidPriceTypeError):
            validate_stock_prices([-5.0, "CORRUPTED"])


# ═══════════════════════════════════════════════════════════════════════════════
#  GROUP 3 — BATCH VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════


class TestBatchValidation:
    """Suite: Multi-ticker batch processing through validate_batch()."""

    def test_all_clean_batch_passes(self, valid_mixed_tickers):
        """All tickers in a clean batch must report True."""
        report = validate_batch(valid_mixed_tickers)
        for ticker, result in report.items():
            assert result is True, f"{ticker} unexpectedly failed."

    def test_mixed_batch_separates_pass_and_fail(self, invalid_batch):
        """
        A batch with both clean and dirty feeds must correctly
        mark passing tickers as True and failing ones with error strings.
        """
        report = validate_batch(invalid_batch)
        assert report["SPGI"] is True
        assert isinstance(report["BAD1"], str), "BAD1 should return an error message."
        assert isinstance(report["BAD2"], str), "BAD2 should return an error message."

    def test_empty_batch_returns_empty_report(self):
        """An empty batch dict must return an empty report."""
        report = validate_batch({})
        assert report == {}

    def test_batch_result_count_matches_input(self, valid_mixed_tickers):
        """Report must contain exactly one entry per input ticker."""
        report = validate_batch(valid_mixed_tickers)
        assert len(report) == len(valid_mixed_tickers)


# ═══════════════════════════════════════════════════════════════════════════════
#  GROUP 4 — CUSTOM THRESHOLD
# ═══════════════════════════════════════════════════════════════════════════════


class TestCustomThreshold:
    """Suite: Validation with a custom minimum price floor."""

    def test_prices_above_custom_threshold_pass(self):
        """Prices strictly above a custom threshold must pass."""
        assert validate_stock_prices([10.0, 20.0, 30.0], threshold=5.0) is True

    def test_prices_at_or_below_threshold_fail(self):
        """Prices at or below the custom threshold must raise NegativePriceError."""
        with pytest.raises(NegativePriceError):
            validate_stock_prices([5.0, 10.0, 20.0], threshold=5.0)
