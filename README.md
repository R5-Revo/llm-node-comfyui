# Universal LLM Node for ComfyUI

これは、ComfyUIで以下のLLM APIと接続してプロンプト拡張を行うためのノードです：

- OpenAI (ChatGPT)
- Claude (Anthropic)
- Gemini (Google)
- Groq
- Mistral

## 導入方法

1. このリポジトリを `ComfyUI/custom_nodes/` に配置
2. `.env` に各サービスのAPIキーを記載：

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
GROQ_API_KEY=...
MISTRAL_API_KEY=...
```

3. 必要パッケージをインストール：

```bash
source venv/bin/activate
pip install -r requirements.txt
```

4. ComfyUIを再起動すれば、`Universal LLM Prompt` ノードが使えるようになります。
