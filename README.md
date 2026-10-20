# AIDE+ Translations

AIDE+ 界面文字的翻译仓库。欢迎为现有语言改进译文，或添加新的语言。
Translations of the AIDE+ user interface. Improvements to existing languages and new languages are welcome.

## 目录 / Layout

```
app/values/          英文原文（由 AIDE+ 主仓库自动生成，请不要修改）
                     English source strings (generated from the AIDE+ sources; do not edit)
app/values-zh-rCN/   简体中文 / Simplified Chinese
app/values-de/       Deutsch
app/values-pt/       Português
app/values-xx/       新语言 / new languages
tools/validate.py    与 CI 相同的检查 / the same checks CI runs
```

文件格式是 Android 字符串资源（`strings.xml`）。每个语言目录中的文件名与 `app/values/` 中的对应，
只需要写你翻译了的条目，没有翻译的条目会显示英文原文。

Files are Android string resources. File names in a language folder match the ones in `app/values/`;
include only the entries you translated — missing entries fall back to English.

## 如何贡献 / How to contribute

1. Fork 本仓库，在对应语言目录中修改或新增条目（新语言：新建 `app/values-xx/`，如 `values-ja`、`values-fr`、
   `values-zh-rTW`、`values-b+sr+Latn`）。
2. 本地检查：`python tools/validate.py app`（需要 Python 3，无其它依赖）。
3. 提交 Pull Request。CI 通过、经维护者审核后会合并，并在下一个版本中进入 AIDE+。

1. Fork, then edit or add entries in the language folder (new language: create `app/values-xx/`, e.g. `values-ja`,
   `values-fr`, `values-zh-rTW`, `values-b+sr+Latn`).
2. Check locally: `python tools/validate.py app` (Python 3, no dependencies).
3. Open a pull request. Once CI passes and a maintainer reviews it, it ships in the next AIDE+ release.

## 翻译规则 / Rules

- **保持 `name` 不变**，只翻译标签之间的文字。不要新增 `values/` 中没有的 key。
  Keep every `name`; translate only the text. Do not add keys that are not in `values/`.
- **格式占位符保持一致**：`%1$s`、`%2$d`、`%s` 等必须原样保留（顺序可以按语言调整，编号不能变）。
  Keep format placeholders such as `%1$s`, `%2$d`, `%s` (reordering is fine, numbers must not change).
- **单引号写成 `\'`**，换行写成 `\n`，`&` 写成 `&amp;`，`<` 写成 `&lt;`。
  Escape apostrophes as `\'`, new lines as `\n`, `&` as `&amp;`, `<` as `&lt;`.
- **技术名词不翻译**：类名、Gradle/XML 写法、命令、文件路径、按键名（ESC、CTRL…）和产品名保持原样。
  Do not translate class names, Gradle/XML syntax, commands, paths, key names (ESC, CTRL…) or product names.
- `plurals` 至少要有 `quantity="other"`；`string-array` 的条目数和顺序与原文相同。
  `plurals` need at least `quantity="other"`; `string-array` keeps the same number and order of items.
- 更新内容（What's new）只有中文原文，应用内会用翻译引擎即时翻译，不需要在这里翻译。
  Release notes are written in Chinese only and translated in the app on demand; they are not part of this repository.

## 许可 / License

本仓库中的翻译以 [CC0 1.0](LICENSE) 发布（放弃版权，进入公共领域）。提交 Pull Request 即表示你同意你的贡献
以 CC0 1.0 发布，并可被包含在 AIDE+（包括其非开源版本）中。

Translations in this repository are released under [CC0 1.0](LICENSE) (public domain dedication). By opening a pull
request you agree that your contribution is released under CC0 1.0 and may be shipped in AIDE+, including closed-source builds.
