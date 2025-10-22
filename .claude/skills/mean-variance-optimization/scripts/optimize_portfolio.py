"""
Mean-Variance Portfolio Optimization Script

This script calculates the tangency portfolio (maximum Sharpe ratio portfolio)
given asset characteristics: expected returns, standard deviations, correlations,
and the risk-free rate. Short sales are allowed.
"""

import numpy as np
import sys


def get_positive_float(prompt):
    """Get a positive float from user input."""
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Error: Value must be positive. Please try again.")
        except ValueError:
            print("Error: Please enter a valid number.")


def get_float(prompt):
    """Get a float from user input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Please enter a valid number.")


def get_correlation(prompt):
    """Get a correlation coefficient from user input."""
    while True:
        try:
            value = float(input(prompt))
            if -1 <= value <= 1:
                return value
            print("Error: Correlation must be between -1 and 1. Please try again.")
        except ValueError:
            print("Error: Please enter a valid number.")


def get_positive_int(prompt):
    """Get a positive integer from user input."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Error: Value must be positive. Please try again.")
        except ValueError:
            print("Error: Please enter a valid integer.")


def build_covariance_matrix(std_devs, correlations):
    """
    Build covariance matrix from standard deviations and correlations.

    Parameters:
    -----------
    std_devs : array-like
        Standard deviations of assets
    correlations : dict
        Dictionary mapping (i, j) pairs to correlation coefficients

    Returns:
    --------
    numpy.ndarray
        Covariance matrix
    """
    n = len(std_devs)
    cov_matrix = np.zeros((n, n))

    # Fill diagonal with variances
    for i in range(n):
        cov_matrix[i, i] = std_devs[i] ** 2

    # Fill off-diagonal with covariances
    for i in range(n):
        for j in range(i + 1, n):
            covariance = correlations[(i, j)] * std_devs[i] * std_devs[j]
            cov_matrix[i, j] = covariance
            cov_matrix[j, i] = covariance  # Symmetric

    return cov_matrix


def is_positive_definite(matrix):
    """Check if a matrix is positive definite."""
    try:
        np.linalg.cholesky(matrix)
        return True
    except np.linalg.LinAlgError:
        return False


def calculate_tangency_portfolio(expected_returns, cov_matrix, risk_free_rate):
    """
    Calculate tangency portfolio weights.

    Parameters:
    -----------
    expected_returns : array-like
        Expected returns of assets
    cov_matrix : numpy.ndarray
        Covariance matrix
    risk_free_rate : float
        Risk-free rate

    Returns:
    --------
    numpy.ndarray
        Portfolio weights
    """
    n = len(expected_returns)
    mu = np.array(expected_returns)
    ones = np.ones(n)

    # Calculate excess returns
    excess_returns = mu - risk_free_rate * ones

    # Compute tangency portfolio weights
    # w = Σ^(-1) × (μ - r_f × 1) / [1^T × Σ^(-1) × (μ - r_f × 1)]
    cov_inv = np.linalg.inv(cov_matrix)
    numerator = cov_inv @ excess_returns
    denominator = ones @ cov_inv @ excess_returns

    weights = numerator / denominator

    return weights


def calculate_portfolio_stats(weights, expected_returns, cov_matrix, risk_free_rate):
    """
    Calculate portfolio statistics.

    Parameters:
    -----------
    weights : numpy.ndarray
        Portfolio weights
    expected_returns : array-like
        Expected returns of assets
    cov_matrix : numpy.ndarray
        Covariance matrix
    risk_free_rate : float
        Risk-free rate

    Returns:
    --------
    tuple
        (expected_return, std_dev, sharpe_ratio)
    """
    mu = np.array(expected_returns)

    # Portfolio expected return
    portfolio_return = weights @ mu

    # Portfolio variance and standard deviation
    portfolio_variance = weights @ cov_matrix @ weights
    portfolio_std = np.sqrt(portfolio_variance)

    # Sharpe ratio
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_std

    return portfolio_return, portfolio_std, sharpe_ratio


def print_matrix(matrix, label="Matrix"):
    """Print a matrix in a formatted way."""
    print(f"\n{label}:")
    print("-" * 60)
    for row in matrix:
        print("  " + "  ".join(f"{val:10.6f}" for val in row))
    print("-" * 60)


def main():
    print("=" * 70)
    print("MEAN-VARIANCE PORTFOLIO OPTIMIZATION")
    print("=" * 70)
    print("\nThis script calculates the tangency portfolio (maximum Sharpe ratio)")
    print("Short sales are allowed (weights can be negative).\n")

    # Get number of assets
    n_assets = get_positive_int("How many assets do you want to include? ")
    print()

    # Get expected returns and standard deviations
    expected_returns = []
    std_devs = []

    for i in range(n_assets):
        print(f"--- Asset {i + 1} ---")
        ret = get_float(f"Expected return for Asset {i + 1} (decimal, e.g., 0.10 for 10%): ")
        std = get_positive_float(f"Standard deviation for Asset {i + 1} (decimal, e.g., 0.20 for 20%): ")
        expected_returns.append(ret)
        std_devs.append(std)
        print()

    # Get risk-free rate
    risk_free_rate = get_float("What is the risk-free rate? (decimal, e.g., 0.03 for 3%): ")
    print()

    # Get correlations
    n_correlations = n_assets * (n_assets - 1) // 2
    print(f"--- Correlations ---")
    print(f"For {n_assets} assets, I need {n_correlations} correlation coefficients.\n")

    correlations = {}
    for i in range(n_assets):
        for j in range(i + 1, n_assets):
            corr = get_correlation(f"Correlation between Asset {i + 1} and Asset {j + 1}: ")
            correlations[(i, j)] = corr

    print("\n" + "=" * 70)
    print("CALCULATIONS")
    print("=" * 70)

    # Build covariance matrix
    cov_matrix = build_covariance_matrix(std_devs, correlations)
    print_matrix(cov_matrix, "Covariance Matrix")

    # Check if positive definite
    if not is_positive_definite(cov_matrix):
        print("\nERROR: The covariance matrix is not positive definite!")
        print("This means the correlation structure is inconsistent.")
        print("Please check your inputs and try again.")
        sys.exit(1)

    print("\nThe covariance matrix is positive definite. Proceeding with optimization...")

    # Calculate tangency portfolio
    weights = calculate_tangency_portfolio(expected_returns, cov_matrix, risk_free_rate)

    # Calculate portfolio statistics
    port_return, port_std, sharpe = calculate_portfolio_stats(
        weights, expected_returns, cov_matrix, risk_free_rate
    )

    # Display results
    print("\n" + "=" * 70)
    print("TANGENCY PORTFOLIO RESULTS")
    print("=" * 70)

    print("\n--- Portfolio Weights ---")
    print(f"{'Asset':<10} {'Weight':<15} {'Position':<15}")
    print("-" * 40)
    for i, w in enumerate(weights):
        position = "Long" if w > 0 else "Short" if w < 0 else "Zero"
        print(f"Asset {i + 1:<4} {w:>10.4f}      {position:<15}")
    print("-" * 40)
    print(f"{'Total':<10} {sum(weights):>10.4f}")

    print("\n--- Portfolio Statistics ---")
    print(f"Expected Return:     {port_return:.4f} ({port_return * 100:.2f}%)")
    print(f"Standard Deviation:  {port_std:.4f} ({port_std * 100:.2f}%)")
    print(f"Sharpe Ratio:        {sharpe:.4f}")

    print("\n--- Long and Short Positions ---")
    long_positions = [(i + 1, w) for i, w in enumerate(weights) if w > 0]
    short_positions = [(i + 1, w) for i, w in enumerate(weights) if w < 0]

    if long_positions:
        print("\nLong Positions:")
        for asset_num, weight in long_positions:
            print(f"  Asset {asset_num}: {weight:.4f} ({weight * 100:.2f}%)")

    if short_positions:
        print("\nShort Positions:")
        for asset_num, weight in short_positions:
            print(f"  Asset {asset_num}: {weight:.4f} ({weight * 100:.2f}%)")

    if not short_positions:
        print("\nNo short positions (all weights are non-negative).")

    print("\n" + "=" * 70)
    print("OPTIMIZATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
