# activate/deactivate models here for testing
MODELS = [
    {
        "id": "openai/gpt-4o-mini",
        "name": "GPT-4o (OpenAI - ChatGPT)",
        "active": False
    },

    {
        "id": "google/gemini-flash-1.5-8b",
        "name": "Gemini Pro (Google)",
        "active": False
    },
    {
        "id": "meta-llama/llama-3.2-3b-instruct",
        "name": "LLaMA 3 (Meta)",
        "active": False
    },
    {
        "id": "x-ai/grok-2-vision-1212",
        "name": "Grok 1 (xAI / Elon Musk)",
        "active": False
    },
    {
        "id": "deepseek/deepseek-chat:free",
        "name": "DeepSeek (China)",
        "active": False
    },
    {
        "id": "mistralai/mixtral-8x7b-instruct",
        "name": "Mixtral 8x7B (Mistral)",
        "active": False
    },
    {
        "id": "perplexity/llama-3.1-sonar-small-128k-online",
        "name": "Llama 3.1 (Perplexity)",
        "active": False
        # soll eher conservaitive sein laut Tavishi Choudhary (ZOTERO rot)
    },{
        "name": "ChatGPT",
        "id" : "openai/gpt-4.1-nano",
        "desciption" : """Created Apr 14, 2025
                        1,047,576 context
                        $0.10/M input tokens
                        $0.40/M output tokens
                        For tasks that demand low latency, GPT‑4.1 nano is the fastest and cheapest model in the GPT-4.1 series. It delivers exceptional performance at a small size with its 1 million token context window, and scores 80.1% on MMLU, 50.3% on GPQA, and 9.8% on Aider polyglot coding – even higher than GPT‑4o mini. It’s ideal for tasks like classification or autocompletion.""",
        "active": True
    },
    {
        "name": "Mixtral",
        "id" : "mistralai/mistral-small-3.1-24b-instruct",
        "active": True
    },
    {
        "name" : "GoogleGemini",
        "id" : "google/gemini-2.5-flash-preview-05-20",
        "desciption" : """Created Apr 14, 2025, Low Latency, high throughput, 1 million token """,
        "active": True
    },
    {
        "name" : "Deepseek",
        "id" : "deepseek/deepseek-r1-0528-qwen3-8b",
        "active": True

    },
    {
        "name" : "Grok/X",
        "id" : "x-ai/grok-3-beta",
        "active": True
    },
    {
       "name" : "Llama",
       "id" : "meta-llama/llama-4-maverick",
       "active": True
    }


]
