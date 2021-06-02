# Gitレポジトリの内部構造をGraphvizでグラフ化してみた

## 解決すべき問題

わたしは毎日Gitを使う。まず`git init`する。そのあと`git add xxx`して`git status`して`git commit -m "xxx"`するのを繰り返す。ときどき`git log`したり`git status`もする。これら高級なgitコマンドだけでGitのメリットを享受できる。わたしはずっとそうやってきた。しかしGitが内部にどういうデータ構造を持っているのか、どういう動作をしているのか、皆目わからないまま何年も過ごしてきた。

ある日、[【翻訳】Gitをボトムアップから理解する](http://keijinsonyaban.blogspot.com/2011/05/git.html#ct3) という記事を読んだ。原著者は[John Wiegley](http://newartisans.com/2008/04/git-from-the-bottom-up/) さん、日本語訳 by O-Showさん。この記事は示唆に満ちていた。`git status`のような高級なコマンドだけではなく、`git cat-file`などの低レベルなgitコマンドを駆使すればGitレポジトリの内部のデータ構造を目視できることを教えてくれた。しかしながら、この記事が示す図は概念的・抽象的であっていまいちよくわからなかった。commitオブジェクトとtreeオブジェクトとblobオブジェクトから成るツリーがどういう構造をしているのか、この記事だけでわたしは納得できなかった。

いま自分の手元にあるこのプロジェクトの `.git` ディレクトリのなかにあるcommitオブジェクトとtreeオブジェクトとblobオブジェクトのツリーの実物を読み出しそれを図に写し取りたい。そういうツールを作れないか？

## 解決方法

1. `git cat-file`、`git revparse`、`git ls-tree`、`git ls-files`などの低レベルなgitコマンドをコマンドラインから実行すればgitレポジトリの内容を読み取ることができる。コマンドがSTDOUTに出力したテキストをparseすれば、commitオブジェクトのhashやtreeオブジェクトの内容など、gitレポジトリの内容をすべて把握することができる。

2. グラフを描くツールとして[Graphviz](https://graphviz.org/)がある。

3. gitコマンドとgraphvizを武器として利用するツールをPython言語で組み立てよう。

ツールの名前を `visualize_git_repository` として、開発しました。

## 説明

ひとつ小さなプロジェクトを作り、`git init`していくつかファイルをコミットした。そして `visualize_git_repository` を実行してgitオブジェクトのツリーがどういう形に構築されたかを図にしてみた。コミットを計3回やって、そのつどツリーの形がどのように変化していくかを観察した。以下、その次第をレポートします。

### 1回目のcommitをするまで

プロジェクトのディレクトリを適当な場所に作りました。そのなかにファイルを3つ作りました。

```
% mkdir project
% cd project
% echo '*~' > .gitignore
% echo '# Readme please'> README.md
% echo 'prinln("How do you do?");' > src/greeting.pl
```

このディレクトリで `git init`しました。

```
% git init
```

ファイル3つをGitレポジトリのindexに登録しました。

```
% git add .
```

`git status`コマンドを実行すると、次に`git commit`したら何が起こるかを教えてくれました。

```
% git status
On branch master

No commits yet

Changes to be committed:
(use "git rm --cached <file>..." to unstage)
new file:   .gitignore
new file:   README.md
new file:   src/greeting.pl
```
まだ一度もgit commitをしたことがないこと、git commitすれば3つのファイルがレポジトリに追加されるはずだとわかります。

`git ls-files --stage`コマンドを実行すると、この時点でindexがどのような内容になっているかを読み出すことができます。
```
% git ls-files --stage
100644 b25c15b81fae06e1c55946ac6270bfdb293870e8 0	.gitignore
100644 aadb69a077c74818e3aff608c0c60c56c6c7c6c9 0	README.md
100644 b371df9d9194821c4a54f0e3a77f89bbcee62f7e 0	src/greeting.pl
```
git addしたときに3つのファイルに対応するblobオブジェクトが生成された。そのblobのhashが3つ、indexのなかに列挙されています。各blobに対応するファイルのパスも示されています。たとえば `src/greeting.pl` のようにルートディレクトリを基底とする相対パスが示されています。

`git commit`しました。
```
% git commit -m "initial commit"
[master (root-commit) eba6db4] initial commit
3 files changed, 3 insertions(+)
create mode 100644 .gitignore
create mode 100644 README.md
create mode 100644 src/greeting.pl
```

HEADが指し示すところのcommitオブジェクトのhashが何かを調べました。

```
% git rev-parse HEAD
eba6db414f7045bdを5bce871f0cb183673def2c0c
```

HEADが指し示すところのオブジェクトがcommitオブジェクトであることを念のため確認しました。

```
% git cat-file -t eba6db414f7045bd5bce871f0cb183673def2c0c
commit
```

HEADが指し示すところのcommitオブジェクトの内容をプリントしてみました。
```
% git cat-file -p eba6db4
tree c9b82148b2a37422ec497b1b6aff179410052d31
author kazurayam <kazuaki.urayama@gmail.com> 1622613358 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1622613358 +0900

initial commit
```

commitオブジェクトにはparentで始まる行が少なくとも1行あるのが普通で、それによってcommitオブジェクトのチェーンが形成されます。ところが上記のcommitオブジェクトにはparentがありません。というのも、このcommitオブジェクトはこのプロジェクトがgit initされてから最初のcommitなので、親が無いんですね。

commitオブジェクトを読み出した一行目にtreeオブジェクトのblobが書いてあります。このtreeオブジェクトをたどれば3つのファイルのblobオブジェクトにアクセスできるにちがいありません。treeオブジェクトを読み出してみましょう。

```
% git ls-tree c9b82148b2a37422ec497b1b6aff179410052d31
100644 blob b25c15b81fae06e1c55946ac6270bfdb293870e8	.gitignore
100644 blob aadb69a077c74818e3aff608c0c60c56c6c7c6c9	README.md
040000 tree 3365c4adc895a4c382b97ec206be94f7ee3883e4	src
```
ここにはルートディレクトリの直下にある2つのファイル `.gitignore` と `README.md`に対応するblobオブジェクトのhashが列挙されており、そしてサブディレクトリ `src` に対応するtreeオブジェクトのhashが示されています。

`.gitignore`ファイルのblobの中身を読み出してみましょう。
```
% git cat-file blob b25c15b
*~
```

はい、たしかにこうでした。`README.md`ファイルのblobの中身も読み出してみましょう。

```
% git cat-file blob aadb69a
# Read me please
```

はい、その通りでした。`src`ディレクトリに対応するtreeオブジェクトの中身を読み出してみましょう。

```
% git ls-tree 3365c4adc895a4c382b97ec206be94f7ee3883e4
100644 blob b371df9d9194821c4a54f0e3a77f89bbcee62f7e	greeting.pl
```

`src`ディレクトリの下に `greeting.pl` ファイルのblobオブジェクトがある、と書いてあった。ではそのblobオブジェクトの中身をprintしてみましょう。

```
% git cat-file blob b371df9
print("How do you do?");
```

はい、`greeting.pl`ファイルの中身はたしかにこうでした。

一回目のgit commitが完了した時点で `visualize_git_repository` ツールを実行しました。ツールが生成したグラフがこれです。

![graph-1](docs/images/git-repository-1.png)

この図をみてわたしはこのように理解しました。

1. commitオブジェクトはかならずプロジェクトのルートディレクトリ `/` に対応するtreeオブジェクトへのポインタを持っている。
2. commitオブジェクトは個々のファイル（`README.md`とか）へのポインタを持っていない。
3. commitオブジェクトからルートディレクトリ `/` に対応するtreeオブジェクトを探り、そのtreeを起点としてツリーをたどればプロジェクトのすべてのファイルのblobオブジェクトに到達することができる。


### 2回目のcommitをするまで



% modified README

% git add .


% git status
On branch master
Changes to be committed:
(use "git restore --staged <file>..." to unstage)
modified:   README.md

% git ls-files --stage
100644 b25c15b81fae06e1c55946ac6270bfdb293870e8 0	.gitignore
100644 5a7954106794a54e6fc251a0c85b417baf39a87f 0	README.md
100644 b371df9d9194821c4a54f0e3a77f89bbcee62f7e 0	src/greeting.pl

% git commit -m "modified README.md"
[master 3de57bc] modified README.md
1 file changed, 1 insertion(+), 1 deletion(-)

% git rev-parse HEAD
3de57bc90ad3e77db3b1df4dc897ea268f4bb5be

% git cat-file -t 3de57bc90ad3e77db3b1df4dc897ea268f4bb5be
commit

% git cat-file -p 3de57bc
tree bd4ab230c988560dade3777a5f729cc62792d701
parent eba6db414f7045bd5bce871f0cb183673def2c0c
author kazurayam <kazuaki.urayama@gmail.com> 1622613359 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1622613359 +0900

modified README.md

% git ls-tree bd4ab230c988560dade3777a5f729cc62792d701
100644 blob b25c15b81fae06e1c55946ac6270bfdb293870e8	.gitignore
100644 blob 5a7954106794a54e6fc251a0c85b417baf39a87f	README.md
040000 tree 3365c4adc895a4c382b97ec206be94f7ee3883e4	src

% git cat-file blob b25c15b
*~

% git cat-file blob 5a79541
# Read me more carefully

% git ls-tree 3365c4adc895a4c382b97ec206be94f7ee3883e4
100644 blob b371df9d9194821c4a54f0e3a77f89bbcee62f7e	greeting.pl

% git cat-file blob b371df9
print("How do you do?");

% git cat-file -t eba6db414f7045bd5bce871f0cb183673def2c0c
commit

% git cat-file -p eba6db4
tree c9b82148b2a37422ec497b1b6aff179410052d31
author kazurayam <kazuaki.urayama@gmail.com> 1622613358 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1622613358 +0900

initial commit

% git ls-tree c9b82148b2a37422ec497b1b6aff179410052d31
100644 blob b25c15b81fae06e1c55946ac6270bfdb293870e8	.gitignore
100644 blob aadb69a077c74818e3aff608c0c60c56c6c7c6c9	README.md
040000 tree 3365c4adc895a4c382b97ec206be94f7ee3883e4	src

% git cat-file blob b25c15b
*~

% git cat-file blob aadb69a
# Read me please

% git ls-tree 3365c4adc895a4c382b97ec206be94f7ee3883e4
100644 blob b371df9d9194821c4a54f0e3a77f89bbcee62f7e	greeting.pl

% git cat-file blob b371df9
print("How do you do?");



![graph-2](docs/images/git-repository-2.png)



 ------------------------------------------------------------------------
% add doc/TODO.txt

% git add .


% git status
On branch master
Changes to be committed:
(use "git restore --staged <file>..." to unstage)
new file:   doc/TODO.txt

% git ls-files --stage
100644 b25c15b81fae06e1c55946ac6270bfdb293870e8 0	.gitignore
100644 5a7954106794a54e6fc251a0c85b417baf39a87f 0	README.md
100644 de13371a889dad1d6ead2cc440086db40ac8690e 0	doc/TODO.txt
100644 b371df9d9194821c4a54f0e3a77f89bbcee62f7e 0	src/greeting.pl

% git commit -m "add doc/TODO.txt"
[master 851aa8d] add doc/TODO.txt
1 file changed, 1 insertion(+)
create mode 100644 doc/TODO.txt

% git rev-parse HEAD
851aa8d6b19c19df6589e69ade43d2537b24c124

% git cat-file -t 851aa8d6b19c19df6589e69ade43d2537b24c124
commit

% git cat-file -p 851aa8d
tree 39e990facd1efd19301e1f28377c63f28c4f238a
parent 3de57bc90ad3e77db3b1df4dc897ea268f4bb5be
author kazurayam <kazuaki.urayama@gmail.com> 1622613360 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1622613360 +0900

add doc/TODO.txt

% git ls-tree 39e990facd1efd19301e1f28377c63f28c4f238a
100644 blob b25c15b81fae06e1c55946ac6270bfdb293870e8	.gitignore
100644 blob 5a7954106794a54e6fc251a0c85b417baf39a87f	README.md
040000 tree b2298cc3a3956d2c430fd9c061d73c02fa62b078	doc
040000 tree 3365c4adc895a4c382b97ec206be94f7ee3883e4	src

% git cat-file blob b25c15b
*~

% git cat-file blob 5a79541
# Read me more carefully

% git ls-tree b2298cc3a3956d2c430fd9c061d73c02fa62b078
100644 blob de13371a889dad1d6ead2cc440086db40ac8690e	TODO.txt

% git cat-file blob de13371
Sleep well tonight.

% git ls-tree 3365c4adc895a4c382b97ec206be94f7ee3883e4
100644 blob b371df9d9194821c4a54f0e3a77f89bbcee62f7e	greeting.pl

% git cat-file blob b371df9
print("How do you do?");

% git cat-file -t 3de57bc90ad3e77db3b1df4dc897ea268f4bb5be
commit

% git cat-file -p 3de57bc
tree bd4ab230c988560dade3777a5f729cc62792d701
parent eba6db414f7045bd5bce871f0cb183673def2c0c
author kazurayam <kazuaki.urayama@gmail.com> 1622613359 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1622613359 +0900

modified README.md

% git ls-tree bd4ab230c988560dade3777a5f729cc62792d701
100644 blob b25c15b81fae06e1c55946ac6270bfdb293870e8	.gitignore
100644 blob 5a7954106794a54e6fc251a0c85b417baf39a87f	README.md
040000 tree 3365c4adc895a4c382b97ec206be94f7ee3883e4	src

% git cat-file blob b25c15b
*~

% git cat-file blob 5a79541
# Read me more carefully

% git ls-tree 3365c4adc895a4c382b97ec206be94f7ee3883e4
100644 blob b371df9d9194821c4a54f0e3a77f89bbcee62f7e	greeting.pl

% git cat-file blob b371df9
print("How do you do?");

% git cat-file -t eba6db414f7045bd5bce871f0cb183673def2c0c
commit

% git cat-file -p eba6db4
tree c9b82148b2a37422ec497b1b6aff179410052d31
author kazurayam <kazuaki.urayama@gmail.com> 1622613358 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1622613358 +0900

initial commit

% git ls-tree c9b82148b2a37422ec497b1b6aff179410052d31
100644 blob b25c15b81fae06e1c55946ac6270bfdb293870e8	.gitignore
100644 blob aadb69a077c74818e3aff608c0c60c56c6c7c6c9	README.md
040000 tree 3365c4adc895a4c382b97ec206be94f7ee3883e4	src

% git cat-file blob b25c15b
*~

% git cat-file blob aadb69a
# Read me please

% git ls-tree 3365c4adc895a4c382b97ec206be94f7ee3883e4
100644 blob b371df9d9194821c4a54f0e3a77f89bbcee62f7e	greeting.pl

% git cat-file blob b371df9
print("How do you do?");



![graph-3](docs/images/git-repository-3.png)

## わたしが驚いたこと

### commitオブジェクトはルートディレクトリのtreeオブジェクトを指している


### indexはblobの一次元の列、commit+tree+blobはhashをキーとするオブジェクトのツリー


>おや？ `git ls-files --stage` でindexの中身をプリントしたときにはプロジェクトを構成するファイルのパスが単純な一次元のシーケンスとして表現されていた。treeオブジェクトとblob

