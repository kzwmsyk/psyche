# psyche と R5RS の差分

psyche は **R5RS をベースにした Scheme 実装** である。多くのコア機能は実装済みだが、**R5RS 完全準拠とは言えない**。本ドキュメントは仕様とのギャップを整理する。

最終更新の目安: テスト 125 passed 時点の実装状況。

---

## 総評

| 観点 | 状態 |
|------|------|
| コア言語（特殊形式・マクロ・リスト） | おおむね実装済み |
| 文字列・文字・ベクタ・ポート I/O | 主要部は実装済み |
| 数値塔・超越関数 | **未達（差が大きい）** |
| 継続の意味論 | **簡易実装（部分的）** |
| R5RS 外の拡張 | 複数あり（後述） |

**言えること:** 「R5RS を目標にした実装」「多くの R5RS プログラムが動く可能性が高い」

**言いにくいこと:** 「R5RS 準拠」「R5RS 完全実装」

---

## 1. 未実装の R5RS 標準手続き

### 数値

| 手続き | 備考 |
|--------|------|
| `positive?` | |
| `negative?` | |
| `odd?` | prelude / テスト内でのみ定義されることがある |
| `even?` | 同上 |
| `numerator` | 有理数モデル自体がない |
| `denominator` | 同上 |
| `rationalize` | 同上 |
| `exp` | |
| `log` | |
| `sin` | |
| `cos` | |
| `tan` | |
| `asin` | |
| `acos` | |
| `atan` | |

### ポート

| 手続き | 備考 |
|--------|------|
| `char-ready?` | 入力ポートに文字が待機しているか |
| `transcript-on` | |
| `transcript-off` | |

### ポート（変数としての `set!`）

R5RS では次の束縛に対する `set!` が定義される。

- `current-input-port`
- `current-output-port`

現状は `(current-input-port)` などの**手続き呼び出し**のみ。`set!` による動的切り替えは未対応。

---

## 2. 数値モデル・算術の意味論

R5RS は複素数・有理数を含む**数値塔**と、exact / inexact の厳密な規則を定める。

| 項目 | psyche の現状 |
|------|----------------|
| 内部表現 | Python の `int` / `float` のみ |
| 複素数 | 未対応（`complex?` は `number?` と同等の判定） |
| 有理数 | 未対応（`rational?` は整数・整数相当 float を真にする簡易判定） |
| exact / inexact の伝播 | Python 演算に依存（`+` 等で R5RS と異なる場合あり） |
| `number->string` の radix / exactness 引数 | 未対応（R5RS オプション引数） |
| `string->number` の radix / exactness 引数 | 未対応 |

---

## 3. 部分的・簡易実装（動くが R5RS 厳密意味とは限らない）

### `call/cc`（`call-with-current-continuation`）

- 例外ベースの非ローカル脱出で実装
- 基本的なキャプチャ・再開（例: `(+ 1 (call/cc (lambda (k) (k 5))))`）は動作
- **継続の完全なコピーではない**
- `dynamic-wind` との相互作用（`k` 呼び出し時の after 節の実行順など）は R5RS の要求を満たさない可能性がある

### `dynamic-wind`

- `try` / `finally` による before / after の実行は実装済み
- 継続経由の非ローカル脱出との組み合わせは未検証・不完全

### マクロ（`syntax-rules`）

- 衛生的展開を実装しているが、エッジケースで R5RS / 論文レベルの仕様と乖離する可能性がある
- テストでカバーされていないパターンは要確認

### 字句解析・リーダー

実装済み:

- 進数（`#b` `#o` `#d` `#x`）
- 正確度（`#e` `#i`）
- ブロックコメント（`#| ... |#`）
- 文字列の `\x` エスケープ

未確認・不完全の可能性:

- 字句規則のエッジケース全般
- ドット付きベクタなどの非標準的表記
- `+inf.0` / `-inf.0` / `+nan.0`（R5RS 外だが実装間で使われる）

### REPL（`psyche.py`）

- `Scanner(sys.stdin)` を直接使用
- `Port` 層（`current-input-port`, `peek-char` との共有バッファ）を経由しない
- REPL の `read` とポート API の `read` で経路が一致しない

### エラー処理

- R5RS の `error` / `assertion-violation` 区別はない
- 汎用 `Exception` で失敗する

---

## 4. R5RS にない拡張（準拠主張の妨げになる）

psyche 独自、または **R6RS 以降** の機能。

| 機能 | 備考 |
|------|------|
| `values` / `call-with-values` | R6RS 以降 |
| `let-values` / `let*-values` / `letrec-values` | R6RS 以降 |
| `let-syntax` / `letrec-syntax` | R6RS 以降 |
| バイトベクタ `#u8(...)` と関連手続き | R6RS / R7RS |
| `define-syntax` の lambda 変換子 | R6RS 的 |
| `print`（組み込み） | 拡張 |
| `filter`（prelude） | 拡張 |
| `atom?`（prelude） | 拡張 |
| `call/cc` エイリアス | `call-with-current-continuation` の別名（慣習的） |

---

## 5. 実装済みの主要 R5RS 機能（参考）

実装・テスト済みの範囲。詳細は `tests/implemented/` を参照。

### 特殊形式

`if`, `define`, `set!`, `quote`, `quasiquote`, `lambda`, `let`, `let*`, `letrec`, `cond`, `and`, `or`, `begin`, `case`, `do`, `delay`, `eval`, `include`, `define-syntax`

### リスト・制御

`cons`, `car`, `cdr`, `set-car!`, `set-cdr!`, `apply`, `map`, `for-each`, `force`, `eq?`, `eqv?`, `equal?`

### 数値（基本）

`+`, `-`, `*`, `/`, `=`, `<`, `>`, `<=`, `>=`, `abs`, `max`, `min`, `quotient`, `remainder`, `modulo`, `gcd`, `lcm`, `floor`, `ceiling`, `truncate`, `round`, `expt`, `sqrt`, `exact?`, `inexact?`, `integer?`, `complex?`, `real?`, `rational?`, `number->string`, `string->number`, `exact->inexact`, `inexact->exact`

### 文字・文字列・ベクタ

文字・文字列・ベクタの主要手続き（大文字小文字無視比較、`string-fill!`, `vector-fill!` 含む）

### ポート

`eof-object?`, `port?`, `input-port?`, `output-port?`, `current-*-port`, ファイルオープン/クローズ, `read`, `read-char`, `peek-char`, `write`, `write-char`, `display`, `newline`, `load`, `with-*-from-file`, `call-with-*-file`

### 環境

`interaction-environment`, `scheme-report-environment`, `null-environment`

### マクロ

衛生的 `syntax-rules`（`define-syntax`）

---

## 6. 優先度の目安（R5RS への近づけ方）

影響が大きい順の候補。

1. **超越関数**（`exp`, `log`, `sin` 等）— 教材・実用で頻出
2. **数値述語**（`positive?`, `negative?`, `odd?`, `even?`）
3. **`char-ready?`**, **`transcript-on` / `transcript-off`**
4. **`set!` 可能な `current-*-port`**
5. **数値塔・exact/inexact 規則**の整理（設計判断が必要）
6. **`call/cc` + `dynamic-wind`** の意味論を本格化

---

## 7. テスト方針

- 未実装・部分実装の項目にテストを追加する場合は `tests/unimplemented/` に置く（自動 `xfail`）
- 実装完了後は `tests/implemented/` へ移動する

詳細は `.cursor/rules/testing.mdc` を参照。
