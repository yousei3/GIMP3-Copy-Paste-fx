# Copy Paste Layer fx for GIMP 3

# English
## Overview
A Python 3 plugin for GIMP 3 that allows you to copy non-destructive layer effects (GEGL filters) from one layer and paste them onto another. It supports pasting to multiple layers simultaneously, as well as pasting across different images (tabs).

## Requirements
- GIMP 3.0 or later

## Installation
1. Open your GIMP user configuration directory and navigate to the `plug-ins` folder.
   (e.g., on Windows: `C:\Users\YourUsername\AppData\Roaming\GIMP\3.0\plug-ins`)
2. Create a new folder named `copy_paste_fx` inside the `plug-ins` folder.
3. Place the `copy_paste_fx.py` script inside this new folder.
   (The path should look like: `...\plug-ins\copy_paste_fx\copy_paste_fx.py`)
4. (Linux/macOS only) Grant execution permissions to the script file.
5. Restart GIMP.

## Usage

### Copying Effects
1. Select the layer containing the effects you want to copy.
2. Right-click on the layer in the Layers panel and select "fx Copy" (or go to the top menu: `Layer` > `fx Copy`).
3. A message will appear at the bottom of the screen indicating the number of effects copied.

### Pasting Effects
1. Select the target layer(s) where you want to apply the effects. (You can select multiple layers).
2. Right-click on the layer(s) in the Layers panel and select "fx Paste".
3. The copied effects will be applied while maintaining their original stack order.


## Limitations
- The plugin saves the copied effect parameters to a `gimp_fx_clipboard.json` file inside the plugin folder. This enables cross-tab pasting between different images. You can safely delete this file manually if it is no longer needed.
- Due to GEGL filter property specifications, parameters using special data types (such as color objects) are excluded from the copy process. Standard parameters like numbers, booleans, and strings will be maintained and copied correctly.

---

# 日本語

## 概要 (Overview)
GIMP 3の非破壊レイヤーエフェクト（GEGLフィルタ）をコピーし、別のレイヤーにペーストするためのPython 3プラグインです。
複数のレイヤーを選択しての一括ペーストや、別タブで開いている他の画像へのペーストにも対応しています。

## 動作環境 (Requirements)
- GIMP 3.0 以上

## インストール方法 (Installation)
1. GIMPのユーザー設定ディレクトリ内の `plug-ins` フォルダを開きます。
   Windowsの例: `C:\Users\ユーザー名\AppData\Roaming\GIMP\3.0\plug-ins`
2. `plug-ins` フォルダ内に、スクリプト名と同じ `copy_paste_fx` という名前のフォルダを新規作成します。
3. 作成したフォルダの中に `copy_paste_fx.py` を配置します。
   配置後のパス例: `...\plug-ins\copy_paste_fx\copy_paste_fx.py`
4. （Linux/macOSの場合）スクリプトファイルに実行権限を付与します。
5. GIMPを起動（または再起動）します。

## 使い方 (Usage)
### エフェクトのコピー
1. コピー元のエフェクトが適用されているレイヤーを選択します。
2. レイヤーパネル上で右クリックし、メニューから「fx Copy」を選択します。（または画面上部の「Layer」メニュー内の「fx Copy」を選択）
3. 画面下部にコピーされたエフェクトの数がメッセージとして表示されます。

### エフェクトのペースト
1. エフェクトを適用したいターゲットのレイヤーを選択します。（複数レイヤーの同時選択も可能です）
2. レイヤーパネル上で右クリックし、メニューから「fx Paste」を選択します。
3. コピー元のエフェクトが、元の重なり順を維持したまま適用されます。


## 仕様と制限事項 (Limitations)
- コピーされたエフェクトのパラメータ設定は、プラグインフォルダ内に生成される `gimp_fx_clipboard.json` ファイルに一時保存されます。この仕組みにより、GIMPのプロセスをまたいだタブ間でのコピペを実現しています。不要になった場合は手動で削除して構いません。
- GEGLフィルタのプロパティの仕様上、色情報（GeglColorオブジェクトなど）といった特殊なデータ型を使用する一部のパラメータはコピーから除外されます。数値、真偽値、文字列などの基本的なパラメータは維持されます。

