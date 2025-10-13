parameters = {
    "data_subset": {
        "type": "feature-list-multi",
        "label": "Data subset",
        "description": "Features of the dataset subset to be passed to autocombat for harmonization.",
    },
    "features_to_harmonize": {
        "type": "feature-list-multi",
        "label": "Features to harmonize",
        "description": "Features to harmonize excluding covariates and site indicator.",
    },
    "batch_list_harmonisations": {
        "type": "feature-list-multi",
        "label": "Batch list harmonisations",
        "description": "List of batch variables for nested ComBat.",
    },
    "covariates": {
        "type": "feature-list-multi",
        "label": "Covariates",
        "description": "Covariates to control for during harmonization.",
    },
    "discrete_covariates": {
        "type": "feature-list-multi",
        "label": "Discrete covariates",
        "description": "Discrete covariates to control for during harmonization.",
    },
    "continuous_covariates": {
        "type": "feature-list-multi",
        "label": "Continuous covariates",
        "description": "Continuous covariates to control for during harmonization.",
    },
    "numerical_covariates": {
        "type": "feature-list-multi",
        "label": "Numerical covariates",
        "description": "Numerical covariates for CovBat harmonization.",
    },
    "smooth_terms": {
        "type": "feature-list-multi",
        "label": "Smooth terms",
        "description": "Names of columns to include as smooth, nonlinear terms.",
    },
    "discrete_cluster_features": {
        "type": "feature-list-multi",
        "label": "Discrete cluster features",
        "description": "Target site features which are categorical to one-hot encode for clustering.",
    },
    "continuous_cluster_features": {
        "type": "feature-list-multi",
        "label": "Continuous cluster features",
        "description": "Target site features which are continuous to scale for clustering.",
    },
    "metric": {
        "type": "selection",
        "label": "Metric",
        "description": "Metric to define the optimal number of clusters.",
        "options": ["distortion", "silhouette", "calinski_harabasz"]
    },
    "features_reduction": {
        "type": "str",
        "label": "Features reduction",
        "description": "Method for reduction of the embedded space with n_components.",
    },
    "feature_reduction_dimensions": {
        "type": "int",
        "label": "Feature reduction dimensions",
        "description": "Dimension of the embedded space for features reduction.",
    },
    "empirical_bayes": {
        "type": "bool",
        "label": "Empirical bayes",
        "description": "Whether to use empirical Bayes estimates of site effects.",
        "default": True,
    },
    "mean_only": {
        "type": "bool",
        "label": "Mean only",
        "description": "Whether to perform mean-only adjustment.",
        "default": False,
    },
    "parametric": {
        "type": "bool",
        "label": "Parametric",
        "description": "Whether to use parametric adjustments.",
        "default": True,
    },
    "return_extended": {
        "type": "bool",
        "label": "Return extended",
        "description": "Whether to return extended outputs (intermediate dataframes).",
        "default": False,
    },
    "use_gmm": {
        "type": "bool",
        "label": "Use GMM",
        "description": "Whether to use Gaussian Mixture Model (GMM) for grouping.",
        "default": True,
    },
    "site_indicator": {
        "type": "feature-list-single",
        "label": "Site indicator",
        "description": "Feature that differentiates different sites.",
    },
    "patient_identifier": {
        "type": "feature-list-single",
        "label": "Patient identifier",
        "description": "Column name identifying each patient.",
    },
    "intermediate_results_path": {
        "type": "str",
        "label": "Intermediate results path",
        "description": "Path to save intermediate results.",
    },
}
