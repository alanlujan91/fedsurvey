Analyzing SCF Data
=================

The ``fedsurvey.analysis`` module provides comprehensive tools for analyzing Survey of 
Consumer Finances data.

Key Features
-----------

- Wealth distribution analysis
- Demographic comparisons
- Time series analysis
- Inequality measures
- Wealth composition analysis

Wealth Distribution
------------------

Calculate various measures of wealth distribution and inequality:

.. code-block:: python

    import fedsurvey.analysis as analysis
    
    # Calculate percentiles
    percentiles = analysis.calculate_percentiles(
        df,
        "networth",
        weights="wgt",
        percentiles=[10, 25, 50, 75, 90]
    )
    
    # Calculate Gini coefficient
    gini = analysis.gini_coefficient(
        df["networth"].values,
        df["wgt"].values
    )

Demographic Analysis
------------------

Analyze wealth distribution across demographic groups:

.. code-block:: python

    from fedsurvey.analysis.demographics import wealth_by_education, racial_wealth_gap
    
    # Analyze wealth by education level
    education_wealth = wealth_by_education(
        df,
        measures=['networth', 'financial_assets'],
        normalize=True
    )
    
    # Calculate racial wealth gaps
    gaps = racial_wealth_gap(
        df,
        base_group="White non-Hispanic",
        measures=['networth', 'income']
    )

Time Series Analysis
------------------

Analyze trends over time:

.. code-block:: python

    from fedsurvey.analysis.trends import wealth_growth_rates
    
    # Calculate growth rates
    growth = wealth_growth_rates(
        df,
        measures=['networth', 'financial_assets'],
        percentiles=[10, 50, 90]
    )

API Reference
------------

.. automodule:: fedsurvey.analysis.wealth
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: fedsurvey.analysis.demographics
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: fedsurvey.analysis.trends
   :members:
   :undoc-members:
   :show-inheritance: