# Paper Outline Planning
Thesis Type: **Empirical**

## Introduction and history on roles of data imputation
The aim of the first section of the  paper should play a role to justify the relevance of the material, which in this case is data imputation on missing values.
The introduction would explain the history of data analytics in general into the direction of handling missing values. The aim is to follow the trails of footprints that the data analytics field has had in the past, and explain not only the importance of data imputation itself (why it is crucial to have), but also the methods of execution. (why it is crucial to do it right.)



## Exposure to Various Imputation Methods
In this part of the paper introduces the various methods of imputation there are available to pick from, and its algorithmic/mathematical structure. Some of the members that will have its name in this section are quite trivial (ex. deleting datapoint, mean, forward fill, etc.), and does require less explanation. However, there are some methods that would be more complex to explain and go through, especially ones that involve complex algorithms like deep learning.


## Empirical Section
In this section, multiple datasets (at least 2, for regression and classification) to demonstrate the effects and consequences of the various imputation methods. The "experiment" will be conducted in the following manner:

1. Take a dataset from a famous Data analytics/ML competition sites such as Kaggle.
    (Assume there are no missing values in the original dataset)
2. Recognize the algorithm and its set of hyperparameters that the most accurate competitor has utilized.
3. Create multiple artificially damaged datasets based on some policy (The random method is something that could make sense) [1 -> n] datasets
4. Impute the missing values on various imputation methods mentioned in previous sections, and run the ML algorithms on the imputed dataset. Record the accuracies.
5. Conduct 3,4,5 multiple times (30+ for the sake of ease of experimentation due to the central limit theorem) to conduct a statistical hypothesis testing, to eventually find a statistically significant (inferior) imputation method against the accuracy with dataset w/o missing values.

Conduct 1-5 for multiple datasets for both regression and classification.


## Comments on Results
