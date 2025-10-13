parameters = {
    "data-subset": {
        "type": "feature-list-multi",
        "label": "Data subset",
        "description": "Features of the dataset subset to be passed to autocombat for harmonization.",
    },
    "features-to-harmonize": {
        "type": "feature-list-multi",
        "label": "Features to harmonize",
        "description": "Features to harmonize excluding covariates and site indicator.",
    },
    "batch-list-harmonisations": {
        "type": "feature-list-multi",
        "label": "Batch list harmonisations",
        "description": "List of batch variables for nested ComBat.",
    },
    "covariates": {
        "type": "feature-list-multi",
        "label": "Covariates",
        "description": "Covariates to control for during harmonization.",
    },
    "discrete-covariates": {
        "type": "feature-list-multi",
        "label": "Discrete covariates",
        "description": "Discrete covariates to control for during harmonization.",
    },
    "continuous-covariates": {
        "type": "feature-list-multi",
        "label": "Continuous covariates",
        "description": "Continuous covariates to control for during harmonization.",
    },
    "numerical-covariates": {
        "type": "feature-list-multi",
        "label": "Numerical covariates",
        "description": "Numerical covariates for CovBat harmonization.",
    },
    "discrete-covariates-to-remove": {
        "type": "feature-list-multi",
        "label": "Discrete covariates to remove",
        "description": "Discrete covariates to remove with Combat++.",
    },
    "continuous-covariates-to-remove": {
        "type": "feature-list-multi",
        "label": "Continuous covariates to remove",
        "description": "Continuous covariates to remove with Combat++.",
    },
    "smooth-terms": {
        "type": "feature-list-multi",
        "label": "Smooth terms",
        "description": "Names of columns to include as smooth, nonlinear terms.",
    },
    "discrete-cluster-features": {
        "type": "feature-list-multi",
        "label": "Discrete cluster features",
        "description": "Target site features which are categorical to one-hot encode for clustering.",
    },
    "continuous-cluster-features": {
        "type": "feature-list-multi",
        "label": "Continuous cluster features",
        "description": "Target site features which are continuous to scale for clustering.",
    },
    "metric": {
        "type": "str",
        "label": "Metric",
        "description": "Metric to define the optimal number of clusters.",
    },
    "features-reduction": {
        "type": "str",
        "label": "Features reduction",
        "description": "Method for reduction of the embedded space with n_components.",
    },
    "feature-reduction-dimensions": {
        "type": "int",
        "label": "Feature reduction dimensions",
        "description": "Dimension of the embedded space for features reduction.",
    },
    "empirical-bayes": {
        "type": "bool",
        "label": "Empirical bayes",
        "description": "Whether to use empirical Bayes estimates of site effects.",
    },
    "mean-only": {
        "type": "bool",
        "label": "Mean only",
        "description": "Whether to perform mean-only adjustment.",
    },
    "parametric": {
        "type": "bool",
        "label": "Parametric",
        "description": "Whether to use parametric adjustments.",
    },
    "return-extended": {
        "type": "bool",
        "label": "Return extended",
        "description": "Whether to return extended outputs (intermediate dataframes).",
    },
    "use-gmm": {
        "type": "bool",
        "label": "Use GMM",
        "description": "Whether to use Gaussian Mixture Model (GMM) for grouping.",
    },
    "site-indicator": {
        "type": "feature-list-single",
        "label": "Site indicator",
        "description": "Feature that differentiates different sites.",
    },
    "patient-identifier": {
        "type": "feature-list-single",
        "label": "Patient identifier",
        "description": "Column name identifying each patient.",
    },
    "intermediate-results-path": {
        "type": "str",
        "label": "Intermediate results path",
        "description": "Path to save intermediate results.",
    },
}
