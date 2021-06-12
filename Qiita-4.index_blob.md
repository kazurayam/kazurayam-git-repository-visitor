# Gitの内部データ構造をGraphvizで描画してみた 第4回 ワークツリーとインデックスとblob

## 解決すべき問題

...

## 解決方法

## 説明

### ステップ1 `git init`した後で`git add`する前

![figure-4.1](docs/images/figure-4.1.png)

### ステップ2 `git add`したらインデックスとblobが更新された

![figure-4.2](docs/images/figure-4.2.png)

### ステップ3 `git commit`したらblobがツリーにつながった

![figure-4.3](docs/images/figure-4.3.png)

### ステップ4 TODO.txtファイルを追加して`git add`する前

![figure-4.4](docs/images/figure-4.4.png)

### ステップ5 `git add`したらインデックスとblobが更新された

![figure-4.5](docs/images/figure-4.5.png)

### ステップ6 `git commit`したらblobがツリーにつながった

![figure-4.6](docs/images/figure-4.6.png)

### ステップ7 READMEファイルを修正して`git add`した

![figure-4.7](docs/images/figure-4.7.png)

### ステップ8 READMEファイルをもう一度修正して`git add`した

![figure-4.8](docs/images/figure-4.8.png)

### ステップ9 READMEファイルを`git commit`した

![figure-4.9](docs/images/figure-4.9.png)

[git gc](https://git-scm.com/docs/git-gc)

## まとめ

