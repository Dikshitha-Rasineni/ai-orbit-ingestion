import requests


COMPANIES = [
    {
        "name": "OpenAI",
        "url": "https://openai.com",
        "description": "AI research and deployment company developing artificial intelligence systems and products.",
    },
    {
        "name": "Anthropic",
        "url": "https://www.anthropic.com",
        "description": "AI safety and research company developing reliable and interpretable AI systems.",
    },
    {
        "name": "Google DeepMind",
        "url": "https://deepmind.google",
        "description": "Artificial intelligence research organization developing advanced AI systems.",
    },
    {
        "name": "NVIDIA",
        "url": "https://www.nvidia.com",
        "description": "Technology company developing GPUs, AI computing platforms, and accelerated computing systems.",
    },
    {
        "name": "Meta AI",
        "url": "https://ai.meta.com",
        "description": "Artificial intelligence research and development organization at Meta.",
    },
    {
        "name": "Microsoft AI",
        "url": "https://www.microsoft.com/en-us/ai",
        "description": "AI organization developing artificial intelligence products, services, and research.",
    },
    {
        "name": "Hugging Face",
        "url": "https://huggingface.co",
        "description": "AI platform providing machine learning models, datasets, and development tools.",
    },
    {
        "name": "Mistral AI",
        "url": "https://mistral.ai",
        "description": "AI company developing open and commercial large language models.",
    },
    {
        "name": "Cohere",
        "url": "https://cohere.com",
        "description": "AI company developing enterprise-focused language models and AI solutions.",
    },
    {
        "name": "xAI",
        "url": "https://x.ai",
        "description": "Artificial intelligence company developing large language models and AI systems.",
    },
    {
        "name": "Stability AI",
        "url": "https://stability.ai",
        "description": "AI company developing generative AI models and creative AI systems.",
    },
    {
        "name": "AI21 Labs",
        "url": "https://www.ai21.com",
        "description": "AI company developing language models and generative AI applications.",
    },
    {
        "name": "Perplexity AI",
        "url": "https://www.perplexity.ai",
        "description": "AI company developing an answer engine and AI-powered search products.",
    },
    {
        "name": "Scale AI",
        "url": "https://scale.com",
        "description": "AI company providing data infrastructure and AI development platforms.",
    },
    {
        "name": "Databricks",
        "url": "https://www.databricks.com",
        "description": "Data and AI company providing platforms for analytics, machine learning, and generative AI.",
    },
    {
        "name": "IBM",
        "url": "https://www.ibm.com",
        "description": "Technology company providing enterprise computing, AI, and cloud solutions.",
    },
    {
        "name": "Amazon Web Services",
        "url": "https://aws.amazon.com",
        "description": "Cloud computing provider offering infrastructure and artificial intelligence services.",
    },
    {
        "name": "Google Cloud",
        "url": "https://cloud.google.com",
        "description": "Cloud platform providing infrastructure, machine learning, and artificial intelligence services.",
    },
    {
        "name": "Runway",
        "url": "https://runwayml.com",
        "description": "AI company developing generative tools for video and creative production.",
    },
    {
        "name": "ElevenLabs",
        "url": "https://elevenlabs.io",
        "description": "AI company developing speech synthesis and voice AI technology.",
    },
    {
        "name": "Pika",
        "url": "https://pika.art",
        "description": "Generative AI company developing AI-powered video creation tools.",
    },
    {
        "name": "Character AI",
        "url": "https://character.ai",
        "description": "AI company developing conversational character and chatbot experiences.",
    },
    {
        "name": "Replit",
        "url": "https://replit.com",
        "description": "Software development platform incorporating AI-assisted programming tools.",
    },
    {
        "name": "Cursor",
        "url": "https://www.cursor.com",
        "description": "AI-powered code editor and software development platform.",
    },
    {
        "name": "Groq",
        "url": "https://groq.com",
        "description": "AI infrastructure company developing accelerated inference technology and AI computing systems.",
    },
    {
        "name": "Lambda",
        "url": "https://lambdal.com",
        "description": "AI infrastructure company providing GPU cloud computing and machine learning infrastructure.",
    },
    {
        "name": "Together AI",
        "url": "https://www.together.ai",
        "description": "AI platform providing model inference, training, and generative AI infrastructure.",
    },
    {
        "name": "Replicate",
        "url": "https://replicate.com",
        "description": "Platform for running and deploying machine learning models through APIs.",
    },
    {
        "name": "Weights & Biases",
        "url": "https://wandb.ai",
        "description": "Machine learning platform for experiment tracking, model development, and AI workflows.",
    },
    {
        "name": "Vercel",
        "url": "https://vercel.com",
        "description": "Cloud platform providing deployment infrastructure and AI application development tools.",
    },
]

def fetch_companies(
    limit: int = 10,
) -> list[dict]:
    companies = []

    for company in COMPANIES[:limit]:
        try:
            response = requests.get(
                company["url"],
                timeout=10,
                headers={
                    "User-Agent": "AI-Orbit-Ingestion/1.0"
                },
            )

            company_data = dict(company)
            company_data["status_code"] = response.status_code

        except requests.RequestException:
            company_data = dict(company)
            company_data["status_code"] = None

        companies.append(company_data)

    return companies