The Best Feature Engineering Tools
9 mins read
Author Tanay Agrawal
February 22nd, 2021
When it comes to predictive models, the dataset always needs a good description. In the real world, datasets are raw and need plenty of work. If the model is to understand a dataset for supervised or unsupervised learning, there are several operations you need to perform and this is where feature engineering comes in.

In this article, we’ll discuss:

What is feature engineering
Types of problem in feature engineering
Open source tools for feature engineering
Comparison of feature engineering tools
Feature engineering examples
Let’s start with a couple of examples. Here, we have a categorical feature column with certain fruit: ‘banana’, ‘pineapple’ and ‘unknown’. We can label encode it:

Fruits
banana
pineapple
banana
unknown
Fruits
1
2
1
0
However, linear predictive models like decisions tree would understand this feature better if we decompose it to three different features, one-hot encoding them:

Fruits
banana
pineapple
banana
unknown
f_banana	f_pineapple	f_unknown
1	0	0
0	1	0
1	0	0
0	0	1
In the last example we used a feature which made no sense to the machine learning algorithm and transformed it to numbers. Now in the second example we’ll perform a more complex operation. Let’s take the famous titanic dataset. In the titanic dataset, based on certain attributes, we define if titanic passengers survived or not. 

We have a column called ‘Name’. Names have titles like ‘mr.’, ‘mrs.’, ‘lord’, or ‘master’, which might have impacted the survival of a person. We can use the information and engineer a new feature, based on titles in passenger names. 

Let’s see how we can do this with a small block of code:

import pandas as pd
import re

df = pd.read_csv('./train.csv')

names = list()
_ = [names.extend(i.split()) for i in df['Name']]

names = [' '.join(re.findall(r"[a-zA-Z]+", name)).lower() for name in names]

seen_titles = set()
titles = [x for x in names if x not in seen_titles and not seen_titles.add(x)]

counts = dict()
for title in titles:
    counts[title] = names.count(title)

print({i: counts[i] for i in counts if counts[i]>50})

Output:

{'miss': 182, 'mr': 521, 'mrs': 129, 'william': 64}
We can see the occurrences of ‘miss’, ‘mr’ and ‘mrs’ is high, we can use this information, use the three titles and unknown (or if you want to do more work, find titles like master, lord, etc.) and make a categorical feature out of this. High number of occurrences of these titles means more data points have these values, which means there can be some relation between these titles and target columns. Also we can deduce that females had a higher survival rate or a person with the title ‘lord’ was more probable to survive. And hence this attribute which was just a bunch of names, is now an important feature.

Now that you’ve seen it in practice, let’s move on to a bit of theory behind feature engineering.

What is feature engineering?
Feature Engineering is the art of creating features from raw data, so that predictive models can deeply understand the dataset and perform well on unseen data. Feature engineering is not a generic method that you can apply on all datasets in the same way. Different datasets require different approaches. 

The representation of datasets for machine learning algorithms is different in each case. In case of images, important features can be shapes, lines, and edges. For audio, it can be certain words that make a difference. 

A good example of engineering features in images can be autoencoders, where they actually learn automatically what kind of features will the model understand best. Autoencoders input the images and the output is the same image, so the layers in between learn the latent representation of those images. These latent representations are better understood by neural networks and can be used to train better models.

Types of problems in feature engineering
Before going into tools for feature engineering, we’ll look at some of the operations that we can perform. Just remember that the best approach depends on the problem statement.

Feature extraction:
Feature extraction is the process of making new features which are composite of the existing ones. One of the great example of Feature Extraction is dimensionality reduction.

There can be millions of features in a dataset with audio, images, or even a tabular one. While a lot of them can be redundant, there is also the problem of model complexity. 

For some machine learning algorithms, the training time complexity increases exponentially as the number of features grows. In this case, we use feature extraction or dimensionality reduction.

There are algorithms like PCA, TSNE, and others that can be used to reduce feature dimensionality. They aggregate different features by using mathematical operations, while trying to keep the information intact. 

Let’s see an example of feature extraction while using PCA in Scikit-learn:

import pandas as pd
from sklearn.decomposition import PCA

df = pd.DataFrame([[2,4,6,8], [4,8,12,16]])
print(df)

0	1	2	3
0	2	4	6	8
1	4	8	12	16
 dr = PCA(n_components=2)
reduced_df = dr.fit_transform(df)
print(reduced_df)

array([[ 5.47722558e+00,  6.66133815e-16],
       [-5.47722558e+00,  6.66133815e-16]])
In the code above we used PCA to reduce the dimension of the above dataframe from 4 to 2. 

Feature selection:
Some features are more important, and others are so redundant that they don’t affect the model at all. We can score them based on a chosen metric, and arrange them in order of importance. Then, eliminate the unimportant ones. 

This can also be a recursive process where, after feature selection, we train the model, calculate the accuracy score, and then do feature selection again. We can iterate until we find the final number of features to keep in the dataset. The process is called recursive feature selection.

Some of the commonly used feature scoring functions are: 

F-score, 
mutual information score, 
Chi-square score. 
F-score can find the linear relation between feature and target columns, and create scores accordingly. Using scores for each feature, we can eliminate the ones with a lower F-score. Similarly, mutual information score can capture both linear and non-linear relationships between feature and target column, but needs more samples.

Chi square is a test used in statistics to test the independence of two events. A lower value of chi square suggests that the two variables(feature and target) are independent. Higher values for two variables means dependent hence important features.

The above are univariate feature selection algorithms. There are also algorithms based on trees or lasso regression, which can be used to calculate impurity-based feature importance.

Features can also be dropped based on the correlation between them. If two features are highly correlated, it makes sense to drop one of them as we’ll reduce the dimensionality of the dataset. 

Now, let’s look at a really simple F-score example:

import pandas as pd
df = pd.DataFrame([[1,12,2], [2, 34, 4], [3,87,6] ])
print(df)
0	1	2
0	1	12	2
1	2	34	4
2	3	87	6
from sklearn.feature_selection import f_regression
scores, _ = f_regression(df.iloc[:,0:2], df.iloc[:,-1])
print(scores)
[4.50359963e+15 1.75598335e+01]
We can see the huge difference between F-scores for columns ‘0’ and ‘1’ with respect to the target column ‘2’. And you can see how I created the dataframe, each value in column ‘0’ is half of each respective value in column ‘2’. However column ‘1’ contains some random values. F-score is high between column ‘0’ and target col ‘2’ but low between col ‘1’ and col ‘2’. We can say col ‘0’ better defines the target col ‘2’ therefore a higher score.

Feature construction:
Some features make sense to predictive models after some work, like we saw in the first and second example. This is called feature construction. It involves constructing more powerful features from the existing features in a dataset.

For example, we might have the domain knowledge for some feature that if the value is high enough, it falls into a different category than if it’s lower. 

Let’s say we have the count of trees in an area, with a maximum number of trees at 300. We can categorize: 

0-100 trees as 1, 
101-200 trees as 2,
201-300 trees as 3. 
Categorizing them like this would remove the noise.

We can aggregate features or decompose them (like we did with one-hot encoding). Either way, we are creating new, better features out of the existing ones.

Tools for feature engineering
If you’re working on a very specific problem set, for a dataset in a dedicated project, then I would suggest you to manually work on data. But for generic problems, not everyone has the time to sit and engineer features. So, in this section we’ll look at some of the tools that automate feature engineering.
