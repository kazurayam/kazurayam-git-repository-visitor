# Gitの内部データ構造をGraphvizで描画してみた 第4回 ワーキングツリーとインデックスとblob

## 解決すべき問題

Gitレポジトリができたばかりの世界のことをコミットをGraphvizによるグラフで描写してみようとおもう。

ワーキングツリーにファイルを作ってから`git init`して`git add`して`git commit`するまで、創世記



## 解決方法

## 説明

ワーキングツリーに3つのファイルを作った

`$wt/.gitignore`
`$wt/README.md`
`$wt/src/greeting.pl`

まだ `git add .` していない。この段階でvisualizeしてみた。`git ls-files --stage`でindexの中身を調べたら空っぽだった。

`git add .`した。`git ls-files --stage`でindexの中身を調べたら、3つのファイルのblobがリストアップされていた。`$wt/.git/objects`のツリーをみたら3個のファイルができていた。

`git commit -m "initial commit"`した。commitオブジェクトとtreeオブジェクトとblobオブジェクトができた。`$wt/.git/objects`のツリーをみたら5のファイルができていた。commitオブジェクトが1つ、treeオブジェクトが1つ、blobオブジェクトが3つ、計5つだ。

`$wt/cheerup.txt`ファイルを作った。`git add .`した。


`git rev-list --objects --all`

## まとめ

