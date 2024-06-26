from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Perceptron
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from matplotlib.colors import ListedColormap

from logistic_regression_gd import LogisticRegressionGD

import numpy as np
import matplotlib.pyplot as plt


def plot_decision_regions(
    X, y, classifier, test_idx=None, resolution=0.02
):  # setup marker generator and color map
    markers = ("o", "s", "^", "v", "<")
    colors = ("red", "blue", "lightgreen", "gray", "cyan")
    cmap = ListedColormap(colors[: len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx1, xx2 = np.meshgrid(
        np.arange(x1_min, x1_max, resolution), np.arange(x2_min, x2_max, resolution)
    )
    lab = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)
    lab = lab.reshape(xx1.shape)
    plt.contourf(xx1, xx2, lab, alpha=0.3, cmap=cmap)
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())
    # plot class examples
    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(
            x=X[y == cl, 0],
            y=X[y == cl, 1],
            alpha=0.8,
            c=colors[idx],
            marker=markers[idx],
            label=f"Class {cl}",
            edgecolor="black",
        )
        # highlight test examples
    if test_idx:
        # plot all examples
        X_test, y_test = X[test_idx, :], y[test_idx]
        plt.scatter(
            X_test[:, 0],
            X_test[:, 1],
            c="none",
            edgecolor="black",
            alpha=1.0,
            linewidth=1,
            marker="o",
            s=100,
            label="Test set",
        )


iris = datasets.load_iris()
X = iris.data[:, [2, 3]]
y = iris.target

print("Class labels:", np.unique(y))

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y
)

# Just to show that stratify actually works as intended
print("Labels counts in y:", np.bincount(y))
print("Labels counts in y_train:", np.bincount(y_train))
print("Labels counts in y_test:", np.bincount(y_test))

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
X_test_std = sc.transform(X_test)

ppn = Perceptron(eta0=0.1, random_state=1)
ppn.fit(X_train_std, y_train)

y_pred = ppn.predict(X_test_std)
print("Misclassified examples: %d" % (y_test != y_pred).sum())
print("Accuracy score: %.3f" % ppn.score(X_test_std, y_test))

X_combined_std = np.vstack((X_train_std, X_test_std))
y_combined = np.hstack((y_train, y_test))
plot_decision_regions(
    X=X_combined_std, y=y_combined, classifier=ppn, test_idx=range(105, 150)
)
plt.xlabel("Petal length [standardized]")
plt.ylabel("Petal width [standardized]")
plt.tight_layout()
plt.show()

X_train_01_subset = X_train_std[(y_train == 0) | (y_train) == 1]
y_train_01_subset = y_train[(y_train == 0) | (y_train) == 1]
lrgd = LogisticRegressionGD(eta=0.3, n_iter=1000, random_state=1)

lrgd.fit(X_train_01_subset, y_train_01_subset)
plot_decision_regions(X=X_train_01_subset, y=y_train_01_subset, classifier=lrgd)
plt.xlabel("Petal length [standardized]")
plt.ylabel("Petal width [standardized]")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

from sklearn.linear_model import LogisticRegression

lr = LogisticRegression(C=100.0, solver="lbfgs", multi_class="ovr")
lr.fit(X_train_std, y_train)
plot_decision_regions(
    X_combined_std, y_combined, classifier=lr, test_idx=range(105, 150)
)
plt.xlabel("Petal length [standardized]")
plt.ylabel("Petal width [standardized]")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

prediction = lr.predict_proba(X_test_std[:3, :]).argmax(axis=1)
print("Classes predicted", prediction)

# Regularization and feature scaling

weights, params = [], []

for c in np.arange(-5, 5):
    lr = LogisticRegression(C=10.0**c, multi_class="ovr")
    lr.fit(X_train_std, y_train)
    weights.append(lr.coef_[1])
    params.append(10.0**c)
weights = np.array(weights)
plt.plot(params, weights[:, 0], label="Petal length")
plt.plot(params, weights[:, 1], linestyle="--", label="Petal width")
plt.ylabel("Weight coefficient")
plt.xlabel("X")
plt.legend(loc="upper left")
plt.xscale("log")
plt.show()

# Support Vector machine approach with a lower value for C
from sklearn.svm import SVC

svm = SVC(kernel="linear", C=1.0, random_state=1)
svm.fit(X_train_std, y_train)
plot_decision_regions(
    X_combined_std, y_combined, classifier=svm, test_idx=range(105, 150)
)
plt.xlabel("Petal length [standardized]")
plt.ylabel("Petal width [standardized]")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

np.random.seed(1)
X_xor = np.random.randn(200, 2)
y_xor = np.logical_xor(X_xor[:, 0] > 0, X_xor[:, 1] > 0)
y_xor = np.where(y_xor, 1, 0)
plt.scatter(
    X_xor[y_xor == 1, 0],
    X_xor[y_xor == 1, 1],
    c="royalblue",
    marker="s",
    label="Class 1",
)
plt.scatter(
    X_xor[y_xor == 0, 0], X_xor[y_xor == 0, 1], c="tomato", marker="o", label="Class 0"
)
plt.xlim([-3, 3])
plt.ylim([-3, 3])
plt.xlabel("Feature 1")
plt.xlabel("Feature 2")
plt.legend(loc="best")
plt.tight_layout()
plt.show()

"""
These classes are not linearly separable thus we map them into another dimension.
In this case we can map each example into a 3 dimensional space via the following
mapping function:
   f(x1, x2) = (z1, z2, z3) = (x1, x2, x1**2 + x2**2)

Basic kernel svm steps:
Non linearly separable classes -> map them onto a 3d space -> fit a linear svm model
(aka find the decision boundary) -> map the decision boundary back into the original dimension
"""

from sklearn.svm import SVC

svm = SVC(kernel="rbf", random_state=1, gamma=0.1, C=10.0)
svm.fit(X_xor, y_xor)
plot_decision_regions(X_xor, y_xor, classifier=svm)
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

svm = SVC(kernel="rbf", random_state=1, gamma=0.1, C=1.0)
svm.fit(X_train_std, y_train)
plot_decision_regions(
    X_combined_std, y_combined, classifier=svm, test_idx=range(105, 150)
)
plt.xlabel("Petal length [standardized]")
plt.ylabel("Petal width [standardized]")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

svm = SVC(kernel="rbf", random_state=1, gamma=100.0, C=1.0)
svm.fit(X_train_std, y_train)
plot_decision_regions(
    X_combined_std, y_combined, classifier=svm, test_idx=range(105, 150)
)
plt.xlabel("Petal length [standardized]")
plt.ylabel("Petal width [standardized]")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()


def visualize_entropy_criterion():
    """
    By executing this portion we can visualize how a dependending on the
    "uniformity" of class distribution, the entropy varies.
    """

    def entropy(p: float) -> float:
        return -p * np.log2(p) - (1 - p) * np.log2((1 - p))

    __x = np.arange(0.0, 1.0, 0.01)
    ent = [entropy(p) if p != 0 else None for p in __x]
    plt.ylabel("Entropy")
    plt.xlabel("Class-membership probability p(i=1)")
    plt.plot(__x, ent)
    plt.show()


visualize_entropy_criterion()


def visualize_criterion_comparisons():
    import matplotlib.pyplot as plt
    import numpy as np

    def gini(p):
        return p * (1 - p) + (1 - p) * (1 - (1 - p))

    def entropy(p: float) -> float:
        return -p * np.log2(p) - (1 - p) * np.log2((1 - p))

    def error(p):
        return 1 - np.max([p, 1 - p])

    x = np.arange(0.0, 1.0, 0.01)
    ent = [entropy(p) if p != 0 else None for p in x]
    sc_ent = [e * 0.5 if e else None for e in ent]
    err = [error(i) for i in x]
    fig = plt.figure()
    ax = plt.subplot(111)

    for i, lab, ls, c in zip(
        [ent, sc_ent, gini(x), err],
        ["Entropy", "Entropy (scaled)", "Gini impurity", "Misclassification error"],
        ["-", "-", "--", "-."],
        ["black", "lightgray", "red", "green", "cyan"],
    ):
        line = ax.plot(x, i, label=lab, linestyle=ls, lw=2, color=c)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        ncol=5,
        fancybox=True,
        shadow=False,
    )
    ax.axhline(y=0.5, linewidth=1, color="k", linestyle="--")
    ax.axhline(y=1.0, linewidth=1, color="k", linestyle="--")
    plt.ylim([0, 1.1])
    plt.xlabel("p(i=1)")
    plt.ylabel("impurity index")
    plt.show()


visualize_criterion_comparisons()

from sklearn.tree import DecisionTreeClassifier

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=1, stratify=y
)

tree_model = DecisionTreeClassifier(criterion="gini", max_depth=4, random_state=1)
tree_model.fit(X_train, y_train)
X_combined = np.vstack((X_train, X_test))
y_combined = np.hstack((y_train, y_test))
plot_decision_regions(
    X_combined, y_combined, classifier=tree_model, test_idx=range(105, 150)
)

plt.xlabel("Petal length [cm]")
plt.ylabel("Petal width [cm]")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

from sklearn import tree

feature_names = ["Sepal length", "Sepal width", "Petal length", "Petal width"]
tree.plot_tree(tree_model, feature_names=feature_names, filled=True)
plt.show()

from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=25, random_state=1, n_jobs=2)
forest.fit(X_train, y_train)
plot_decision_regions(
    X_combined, y_combined, classifier=forest, test_idx=range(105, 150)
)
plt.xlabel("Petal length [cm]")
plt.ylabel("Petal width [cm]")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5, p=2, metric="minkowski")
knn.fit(X_train_std, y_train)
plot_decision_regions(
    X_combined_std, y_combined, classifier=knn, test_idx=range(105, 150)
)

plt.xlabel("Petal length [standardized]")
plt.ylabel("Petal width [standardized]")
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()
