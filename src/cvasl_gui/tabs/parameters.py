parameters = {
    "data-subset": {
        "type": "feature-list-multi",
        "label": "Data Subset",
        "description": "Features of the dataset subset to be passed to autocombat for harmonization.",
    },
    "features-to-harmonize": {
        "type": "feature-list-multi",
        "label": "Features To Harmonize",
        "description": "Features to harmonize excluding covariates and site indicator.",
    },
    "batch-list-harmonisations": {
        "type": "feature-list-multi",
        "label": "Batch List Harmonisations",
        "description": "List of batch variables for nested ComBat.",
    },
    "covariates": {
        "type": "feature-list-multi",
        "label": "Covariates",
        "description": "Covariates to control for during harmonization.",
    },
    "discrete-covariates": {
        "type": "feature-list-multi",
        "label": "Discrete Covariates",
        "description": "Discrete covariates to control for during harmonization.",
    },
    "continuous-covariates": {
        "type": "feature-list-multi",
        "label": "Continuous Covariates",
        "description": "Continuous covariates to control for during harmonization.",
    },
    "numerical-covariates": {
        "type": "feature-list-multi",
        "label": "Numerical Covariates",
        "description": "Numerical covariates for CovBat harmonization.",
    },
    "discrete-covariates-to-remove": {
        "type": "feature-list-multi",
        "label": "Discrete Covariates To Remove",
        "description": "Discrete covariates to remove with Combat++.",
    },
    "continuous-covariates-to-remove": {
        "type": "feature-list-multi",
        "label": "Continuous Covariates To Remove",
        "description": "Continuous covariates to remove with Combat++.",
    },
    "smooth-terms": {
        "type": "feature-list-multi",
        "label": "Smooth Terms",
        "description": "Names of columns to include as smooth, nonlinear terms.",
    },
    "discrete-cluster-features": {
        "type": "feature-list-multi",
        "label": "Discrete Cluster Features",
        "description": "Target site features which are categorical to one-hot encode for clustering.",
    },
    "continuous-cluster-features": {
        "type": "feature-list-multi",
        "label": "Continuous Cluster Features",
        "description": "Target site features which are continuous to scale for clustering.",
    },
    "metric": {
        "type": "str",
        "label": "Metric",
        "description": "Metric to define the optimal number of clusters.",
    },
    "features-reduction": {
        "type": "str",
        "label": "Features Reduction",
        "description": "Method for reduction of the embedded space with n_components.",
    },
    "feature-reduction-dimensions": {
        "type": "int",
        "label": "Feature Reduction Dimensions",
        "description": "Dimension of the embedded space for features reduction.",
    },
    "empirical-bayes": {
        "type": "bool",
        "label": "Empirical Bayes",
        "description": "Whether to use empirical Bayes estimates of site effects.",
    },
    "mean-only": {
        "type": "bool",
        "label": "Mean Only",
        "description": "Whether to perform mean-only adjustment.",
    },
    "parametric": {
        "type": "bool",
        "label": "Parametric",
        "description": "Whether to use parametric adjustments.",
    },
    "return-extended": {
        "type": "bool",
        "label": "Return Extended",
        "description": "Whether to return extended outputs (intermediate dataframes).",
    },
    "use-gmm": {
        "type": "bool",
        "label": "Use GMM",
        "description": "Whether to use Gaussian Mixture Model (GMM) for grouping.",
    },
    "site-indicator": {
        "type": "feature-list-single",
        "label": "Site Indicator",
        "description": "Feature that differentiates different sites.",
    },
    "patient-identifier": {
        "type": "feature-list-single",
        "label": "Patient Identifier",
        "description": "Column name identifying each patient.",
    },
    "intermediate-results-path": {
        "type": "str",
        "label": "Intermediate Results Path",
        "description": "Path to save intermediate results.",
    },
}
