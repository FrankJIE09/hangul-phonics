# 韩语谚文拼读 · 跟读卡

基于桌面可用版 `korean-phonics.html` 扩展的纯前端单页工具：保留其可用的 Web Speech 朗读路径，并补全全部元音、辅音、收音与拼读。

**在线访问**：https://frankjie09.github.io/hangul-phonics/

## 文件

| 文件 | 说明 |
| --- | --- |
| `index.html` | 完整版（GitHub Pages 入口）：元音 21 · 辅音 19 · 收音 27 + 「无」 |
| `korean-phonics.html` | 桌面原版备份（元音 10 · 辅音 14 · 无收音） |

## 功能

- **辅音 19**：松音 / 送气 / 紧音 / 鼻音·流音
- **元音 21**：单元音、y 系列、w 系列
- **收音 27 +「无」**：点选后与初声+中声拼成完整音节；双收音标注代表音
- **拼读工作台**：初声 + 中声 + 收音 → 音节，显示罗马音与 IPA，可重复播放
- **键盘**：두벌식 单键 / Shift 紧音（复合元音请直接点卡片）
- **发音**：与桌面可用版相同——`cancel` → 韩文 → `lang=ko-KR` → `speak`（有韩语音色才指定 voice）

## 使用

打开 https://frankjie09.github.io/hangul-phonics/ ，或：

```bash
python -m http.server 8000
# http://127.0.0.1:8000/
```

也可直接双击 `index.html` / `korean-phonics.html`。

若提示未检测到韩语语音包：Windows 设置 → 时间和语言 → 语言和区域 → 添加「한국어」→ 勾选「语音」。

## 许可

MIT
