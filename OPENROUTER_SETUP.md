# OpenRouter Integration Guide

## Best Free AI Models on OpenRouter

OpenRouter provides access to multiple AI models through a unified API. Here are the **best FREE models** perfect for your CNC recommendations:

### 🏆 Top Recommendations:

1. **Meta Llama 3.1 8B (free-tier)**
   - Model: `meta-llama/llama-3.1-8b-instruct:free`
   - Best for: General recommendations, good quality
   - Speed: Fast
   - Quality: ⭐⭐⭐⭐

2. **Google Gemma 2B (free-tier)**
   - Model: `google/gemma-2b-it:free`
   - Best for: Quick responses, cost-effective
   - Speed: Very Fast
   - Quality: ⭐⭐⭐

3. **Mistral 7B (free-tier)**
   - Model: `mistralai/mistral-7b-instruct:free`
   - Best for: Technical recommendations
   - Speed: Fast
   - Quality: ⭐⭐⭐⭐

4. **Qwen 2.5 7B (free-tier)**
   - Model: `qwen/qwen-2.5-7b-instruct:free`
   - Best for: Technical analysis
   - Speed: Fast
   - Quality: ⭐⭐⭐⭐

5. **Phi-3 Mini (free-tier)**
   - Model: `microsoft/phi-3-mini-128k-instruct:free`
   - Best for: Structured responses
   - Speed: Very Fast
   - Quality: ⭐⭐⭐

### 💰 Free Tier Limits:
- Most free models have rate limits (requests per minute)
- Some have daily limits
- Quality is still excellent for your use case

### 🎯 Recommended for Your Use Case:
**Best Choice: `meta-llama/llama-3.1-8b-instruct:free`**
- Excellent for structured JSON responses
- Good understanding of technical content
- Reliable and fast

## Setup Instructions

1. **Get OpenRouter API Key:**
   - Sign up at: https://openrouter.ai/
   - Get your API key from: https://openrouter.ai/keys
   - It's FREE to sign up!

2. **Update .env file:**
   ```
   OPENROUTER_API_KEY=your_openrouter_key_here
   OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
   USE_OPENROUTER=true
   ```

3. **The system will automatically use OpenRouter if configured!**

## Advantages Over OpenAI:
- ✅ FREE models available
- ✅ Multiple model options
- ✅ Same API interface (easy switch)
- ✅ No credit card required for free tier
- ✅ Good quality for technical recommendations

