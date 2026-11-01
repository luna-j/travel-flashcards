# 独立演示案例

这四组样张与个人复习卡组目录分开；入口为 `index.html`，每组3张。卡片页返回此处，不修改个人站点的卡组目录或收纳状态。

生成规范和模板位于 https://github.com/luna-j/scene-audio-flashcards 。本目录的第三方录音不属于该仓库的 MIT 许可；权利归原作品权利人，来源和核对状态见各组 `sources.md`。

内容源为 `data/<case>/cards.json`，音频为 `audio/`。共享模板更新后，在站点仓库执行：

```sh
python3 scripts/rebuild-demos.py --skill /path/to/scene-audio-flashcards
python3 scripts/validate-demos.py
python3 scripts/validate-decks.py
```

`rebuild-demos.py`复用已选好的音频，不需要整集原片、私人脚本或语音模型。它会更新卡片页、文档及下载包；目录页由 `manifest.json` 与 `index.html` 维护。不要把完整源片、转写缓存、私人反馈、真实学习进度或密钥加入本目录。
