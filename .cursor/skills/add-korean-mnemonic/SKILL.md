---
name: add-korean-mnemonic
description: >-
  Adds Korean study lines with Chinese mnemonic hints (谐音) into
  data/store.json, then commits and pushes that file. Use when the user
  pastes Korean plus a 谐音 or memory hint, asks to add words or numbers
  to data.json, store.json, or 学习记录, or says 帮助记忆.
---

# 写入韩文谐音记录

用户口中的 `data.json` 就是本仓库的 `data/store.json`。不要新建别的数据文件。

## 条目

每条放进 `translations` 数组最前面，保持用户给出的先后顺序。字段：

- `zh`：中文意思。纯数字 1–10 且没有另外的中文意思时，写成一二三四五六七八九十。
- `ko`：韩文。去掉括号里的拉丁字母。
- `rom`：括号里的罗马字，没有就用空字符串。
- `ipa`：空字符串。页面会自己算音标。
- `memo`：`zh`、一个空格、用户给的谐音。谐音照抄，不改写、不补造。
- `at`：当前毫秒时间戳，同一批里靠前的更大。
- `id`：本文件里不重复的短字符串。

同一 `zh` + `ko` 已存在时，只更新 `memo` 和 `rom` 并把它移到最前，不另加一条。

保留 `learned`、`reviewLetters`、`reviewSyllables`、`stats` 和其余条目。`translations` 最多 40 条，多出的从末尾丢掉。把 `updatedAt` 设为当前毫秒时间戳。

用 2 空格缩进、`ensure_ascii` 为假、文件末尾一个换行写回。

## 提交并推送

记录写完后提交 `data/store.json` 并推送。没有实际变化就不提交。

提交说明用仓库现有风格，一句中文说明记下了什么。不要改 git 配置，不要强推。

先试 `git push`。若本机 `127.0.0.1:7890` 代理不通，改用已有的 SSH，不改配置：

```bash
git push git@github.com:FrankJIE09/hangul-phonics.git HEAD:main
git fetch git@github.com:FrankJIE09/hangul-phonics.git +refs/heads/main:refs/remotes/origin/main
```

## 例子

输入：`1하나 (hana)哈拿`

写入：

```json
{
  "zh": "一",
  "ko": "하나",
  "rom": "hana",
  "ipa": "",
  "memo": "一 哈拿"
}
```
