# Quick Start: OpenRouter (FREE AI Models)

## 🎯 Best Free Models for Your CNC System

### Top Recommendation:
**`meta-llama/llama-3.1-8b-instruct:free`**
- ✅ Excellent for structured JSON responses
- ✅ Great for technical content
- ✅ Fast and reliable
- ✅ Completely FREE!

### Other Great Options:
1. `google/gemma-2b-it:free` - Very fast, good for quick responses
2. `mistralai/mistral-7b-instruct:free` - Great for technical analysis
3. `qwen/qwen-2.5-7b-instruct:free` - Excellent quality
4. `microsoft/phi-3-mini-128k-instruct:free` - Good for structured data

## 🚀 Setup (2 minutes)

1. **Sign up for OpenRouter** (FREE):
   - Go to: https://openrouter.ai/
   - Click "Sign Up" (no credit card needed!)
   - Verify your email

2. **Get your API key**:
   - Go to: https://openrouter.ai/keys
   - Click "Create Key"
   - Copy your key

3. **Update your .env file**:
   ```bash
   USE_OPENROUTER=true
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
   ```

4. **Restart your Flask app**:
   ```bash
   python app.py
   ```

5. **Done!** Your system now uses FREE AI models! 🎉

## 💡 Why OpenRouter?

- ✅ **FREE models** - No credit card required
- ✅ **Multiple models** - Choose the best one for your needs
- ✅ **Same API** - Works exactly like OpenAI
- ✅ **Easy switch** - Just change USE_OPENROUTER flag
- ✅ **Good quality** - Models are excellent for your use case

## 🔄 Switching Between Providers

To use OpenAI instead:
```bash
USE_OPENROUTER=false
OPENAI_API_KEY=your-openai-key
```

To use OpenRouter (FREE):
```bash
USE_OPENROUTER=true
OPENROUTER_API_KEY=your-openrouter-key
```

The system automatically detects which provider to use!

