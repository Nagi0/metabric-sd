# metabrick-sd
To open orange, just type `orange-canvas.exe` on the terminal where the virtual environment is activated.
Now on open and select the `metabrick_sd/load_database/load_metabrick.ows` file located in this folder. It will request to install the bioinformatics package, which contains the tools to get the gene sets and identify the genes in the metabrick database.

![alt text](image.png)

This file will provide the metabrick database, but also all the preprocessing needed to discretize both the clinical and genetic data.

![alt text](image-1.png)

As it can be seen in the image, there are many options of database to aquire, they are:
- **Clinical plus genetic data** (discretized with: entropy discretization; three intervals made by: < 25%quantile, 25% ≤ x ≤ 75% and > 75% quantile; three intervals of equal frequency)
- **Genetic only data** (with the three discretization options above)
-  **Top k Genetic only**: Taking the top genes returned by the Rank Survival Feature 'Multivariate log-rank'. The criterion for the top k genes was the p-value < 0.005 (with the three discretization options above)