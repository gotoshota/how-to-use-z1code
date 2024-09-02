# how-to-use-z1plus
Z1+ の使い方を簡単にまとめたリポジトリ。
関係者向け。

ソースコードは[ここから](https://data.mendeley.com/datasets/m425t6xtwr/1)、公式のドキュメントは[ここ](https://www.sciencedirect.com/science/article/pii/S0010465522002867?via%3Dihub)。
基本的に公式のREADMEやドキュメントが読めるならそちらを参照することをお勧めする。

## 注意事項
多分MACOSでは使えないので、Linux環境で使うことをお勧めする。

## インストール
上記のURLか、以下のコマンドでダウンロードできる。
```bash
wget -O Z1+.tar.gz https://data.mendeley.com/public-files/datasets/m425t6xtwr/files/3b51d5b9-e873-4ef5-9689-c04cbcc055f1/file_downloaded
```
ダウンロードできたら、適当なディレクトリに解凍する。
場所はどこでもいいが、`local/src/` などがいいかもしれない。
```bash
mkdir Z1+
tar -xvf Z1+.tar.gz -C Z1+
```

コンパイルには、以下のソフトウェアが必要。
**依存関係**
- perl
- fortran

Z1+を解凍したディレクトリで、
```bash
perl Z1+install.pl
```
コンパイルが成功すれば、`Z1+` という実行ファイルが生成される。
これを使って計算を行うが、PATHを通したディレクトリに置いておくと便利なので、例えば、
```bash
cp Z1+ ~/local/bin/
```
などとしておくと、どこからでも `Z1+` で実行できるようになる。

## 使い方
`Z1+` と引数なしで実行すれば、使い方が表示される。
ここでは、LAMMPS の出力結果を使って、Z1+ を使った絡み合い数の計算を行う方法を説明する。
この場合、Z1+はインプットファイルとして、LAMMPSのDATAファイル(`write_data`で出力したもの)を読み込むことができる。
```bash
Z1+ lmp.data
```
とすると、`lmp.data` というファイルを読み込んで計算を行い、
いろいろなファイルが出力される。
多分 `mol` を出力していれば、LAMMPSのトラジェクトリファイル (`dump`、`lammpstrj`) も読み込めると思われる。

## 出力ファイル
読み方を説明する。
出力ファイルは以下の通り、
```bash
$ ls -1
Lpp_values.dat
N_values.dat
Ree_values.dat
Z1+SP.dat
Z1+initconfig.dat
Z1+parameters
Z1+summary.dat
Z1+summary.html
Z_values.dat
config.Z1
```
`N_values.dat` や `Ree_values.dat` などは見ての通り、
`Z1+summary.dat` が最終的な結果をまとめたファイルである。
`Z1+summary.html` は `Z1+summary.dat` をHTML形式にしたもので、ブラウザで見ることができる。
MacOSなら、
```bash
open Z1+summary.html
```

`Z1+summary.dat` の中身は以下の通り、
```
1         : タイムステップ（利用可能な場合）
2         : 真の鎖の数（各鎖に2つ以上のビーズが含まれているもの）
3         : 元の鎖あたりのビーズの平均数
4         : 平均二乗末端間距離
5         : 最短経路の鎖あたりの平均輪郭長 = <Lpp>
6         : 鎖あたりの絡み合いの平均数
7         : コイルチューブの直径（推定値）
8         : コイルチューブのステップ長 (bpp)
9         : 鎖あたりの平均二乗輪郭長の平方根 = sqrt(<Lpp^2>)
10        : 古典的キンクのNe推定値 = Ne_CK
11        : 修正されたキンクのNe推定値 = Ne_MK
12        : 古典的コイルのNe推定値 = Ne_CC
13        : 修正されたコイルのNe推定値 = Ne_MC
14        : 元の鎖の平均結合長
15        : 元の配置におけるビーズの密度
```
上記は、公式ドキュメントを翻訳にかけたもの。
`Ne_xx` とあるのが絡み合い数で、推定方法が複数あって、それぞれの推定方法で計算された絡み合い数が出力されている。
`Ne_MK` を使うのがいいだろう。多分よく見るデータはこの方法で計算されたものだと思う。
（$k_\theta = 1.5$ の $N_\mathrm{e} \sim 28$ とかは`Ne_MK` のはず）

## tools
`tools` ディレクトリには、LAMMPSのトラジェクトリファイルをデータファイルに変換するスクリプトがある。
```bash
python tools/lammps2data.py --input dump.lammpstrj --data lmp.data <--sparse N>
```
- input : LAMMPSのトラジェクトリファイル
- data : 参照するDATAファイル。最終構造の一つくらいは出力してるでしょう？それをトポロジーの参照に使います。
- sparse : このオプションをつけると、Nステップごとにデータを取得する。デフォルトは1。

## その他
ちなみに、LAMMPS の リスタートファイルをデータファイルに変換するには、
```bash
lmp -restart2data <restart file> <data file>
```
とすればいい。


















