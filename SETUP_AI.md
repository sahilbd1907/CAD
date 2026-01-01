# AI Recommendations Setup Guide

## Quick Setup

The AI recommendations feature is now integrated! It works in two modes:

### Mode 1: With OpenAI API (Recommended for Best Results)
Uses GPT-3.5 or GPT-4 for intelligent, context-aware recommendations.

**Setup Steps:**
1. Get an OpenAI API key from: https://platform.openai.com/api-keys
2. Set it as an environment variable:
   ```bash
   # Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # Windows (CMD)
   set OPENAI_API_KEY=your-api-key-here
   
   # Linux/Mac
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. (Optional) Set the model (default is gpt-3.5-turbo):
   ```bash
   export OPENAI_MODEL="gpt-3.5-turbo"  # Cheaper, fast
   # or
   export OPENAI_MODEL="gpt-4"  # More accurate, slower, expensive
   ```

4. Install the OpenAI package:
   ```bash
   pip install openai
   ```

5. Restart your Flask app

**Cost:** ~$0.001-0.003 per quote (very affordable with GPT-3.5-turbo)

### Mode 2: Rule-Based (No API Key Needed)
If no API key is set, the system automatically uses intelligent rule-based recommendations that still provide:
- Material alternatives with cost comparisons
- Design optimization suggestions
- Cost analysis and quick wins

**No setup required!** Works out of the box.

---

## What You Get

### Material Recommendations
- Alternative materials with cost comparisons
- Pros and cons for each material
- Time savings/losses
- Best use cases

### Design Optimization Suggestions
- Thickness optimization
- Geometry simplification recommendations
- Feature modifications
- Priority levels (high/medium/low)

### Cost Analysis
- Main cost drivers identification
- Quick wins for cost reduction
- Potential savings percentage

---

## Testing

1. Upload a DXF file
2. Generate a quote
3. Scroll to the "AI Optimization Recommendations" section
4. Review material alternatives and design suggestions

---

## Troubleshooting

**No AI recommendations showing?**
- Check if `ai_recommendations` is in the results_cache
- Check console for any errors (AI errors are non-critical and won't break the app)
- Verify API key is set correctly (if using OpenAI)

**API errors?**
- Verify your OpenAI API key is valid
- Check your API usage/quota at https://platform.openai.com/usage
- The system will automatically fall back to rule-based recommendations

**Want to disable AI?**
- Simply don't set the OPENAI_API_KEY environment variable
- The system will use rule-based recommendations

---

## Privacy

- **With OpenAI**: Your CAD data is sent to OpenAI's API. Review their privacy policy.
- **Rule-based mode**: All processing is local, no data leaves your server.

---

## Next Steps

Consider implementing:
1. Caching AI responses for similar parts
2. User feedback on recommendations (thumbs up/down)
3. Historical learning from past quotes
4. Custom recommendation prompts per industry

