import { NextRequest, NextResponse } from "next/server";

/**
 * API Route: Fetch Models from different providers
 * Supports: OpenAI, Groq, Anthropic, Local (Ollama), Custom OpenAI-compatible
 */

interface ModelsResponse {
    success: boolean;
    models: { id: string; name: string; provider: string }[];
    error?: string;
}

// Known models for providers that don't have a models endpoint
const ANTHROPIC_MODELS = [
    { id: "claude-3-5-sonnet-20241022", name: "Claude 3.5 Sonnet", provider: "anthropic" },
    { id: "claude-3-opus-20240229", name: "Claude 3 Opus", provider: "anthropic" },
    { id: "claude-3-sonnet-20240229", name: "Claude 3 Sonnet", provider: "anthropic" },
    { id: "claude-3-haiku-20240307", name: "Claude 3 Haiku", provider: "anthropic" },
];

const GEMINI_MODELS = [
    { id: "gemini-2.0-flash-exp", name: "Gemini 2.0 Flash", provider: "google" },
    { id: "gemini-1.5-pro", name: "Gemini 1.5 Pro", provider: "google" },
    { id: "gemini-1.5-flash", name: "Gemini 1.5 Flash", provider: "google" },
];

async function fetchOpenAIModels(apiKey: string, baseUrl: string = "https://api.openai.com/v1") {
    const response = await fetch(`${baseUrl}/models`, {
        headers: {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error(`OpenAI API error: ${response.status}`);
    }

    const data = await response.json();
    return data.data
        .filter((model: any) =>
            model.id.includes("gpt") ||
            model.id.includes("o1") ||
            model.id.includes("text-embedding") ||
            model.id.includes("dall-e")
        )
        .map((model: any) => ({
            id: model.id,
            name: model.id,
            provider: "openai",
        }));
}

async function fetchGroqModels(apiKey: string) {
    const response = await fetch("https://api.groq.com/openai/v1/models", {
        headers: {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error(`Groq API error: ${response.status}`);
    }

    const data = await response.json();
    return data.data.map((model: any) => ({
        id: model.id,
        name: model.id,
        provider: "groq",
    }));
}

async function fetchOllamaModels(baseUrl: string = "http://localhost:11434") {
    const response = await fetch(`${baseUrl}/api/tags`);

    if (!response.ok) {
        throw new Error(`Ollama API error: ${response.status}`);
    }

    const data = await response.json();
    return (data.models || []).map((model: any) => ({
        id: model.name,
        name: model.name,
        provider: "local",
    }));
}

async function fetchLMStudioModels(baseUrl: string = "http://localhost:1234") {
    const response = await fetch(`${baseUrl}/v1/models`);

    if (!response.ok) {
        throw new Error(`LM Studio API error: ${response.status}`);
    }

    const data = await response.json();
    return (data.data || []).map((model: any) => ({
        id: model.id,
        name: model.id,
        provider: "local",
    }));
}

async function fetchCustomModels(apiKey: string, baseUrl: string) {
    // Try OpenAI-compatible endpoint
    const response = await fetch(`${baseUrl}/models`, {
        headers: {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json",
        },
    });

    if (!response.ok) {
        throw new Error(`Custom API error: ${response.status}`);
    }

    const data = await response.json();
    return (data.data || []).map((model: any) => ({
        id: model.id,
        name: model.id || model.name,
        provider: "custom",
    }));
}

export async function POST(request: NextRequest) {
    try {
        const body = await request.json();
        const { api_type, api_key, base_url } = body;

        let models: { id: string; name: string; provider: string }[] = [];

        switch (api_type) {
            case "openai":
                models = await fetchOpenAIModels(api_key, base_url || "https://api.openai.com/v1");
                break;

            case "groq":
                models = await fetchGroqModels(api_key);
                break;

            case "anthropic":
                // Anthropic doesn't have a public models endpoint, return known models
                // But we can validate the API key first
                try {
                    const testResponse = await fetch("https://api.anthropic.com/v1/messages", {
                        method: "POST",
                        headers: {
                            "x-api-key": api_key,
                            "anthropic-version": "2023-06-01",
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify({
                            model: "claude-3-haiku-20240307",
                            max_tokens: 1,
                            messages: [{ role: "user", content: "test" }],
                        }),
                    });
                    // If we get 400 or 200, the key is valid (400 might be rate limit, etc)
                    if (testResponse.status === 401) {
                        throw new Error("Invalid Anthropic API key");
                    }
                } catch (e: any) {
                    if (e.message.includes("Invalid")) throw e;
                }
                models = ANTHROPIC_MODELS;
                break;

            case "google":
            case "gemini":
                // Google AI doesn't have a simple models list endpoint
                models = GEMINI_MODELS;
                break;

            case "local":
                // Try Ollama first, then LM Studio
                try {
                    models = await fetchOllamaModels(base_url || "http://localhost:11434");
                } catch {
                    try {
                        models = await fetchLMStudioModels(base_url || "http://localhost:1234");
                    } catch {
                        throw new Error("Could not connect to local model server (Ollama/LM Studio)");
                    }
                }
                break;

            case "custom":
                if (!base_url) {
                    throw new Error("Base URL is required for custom providers");
                }
                models = await fetchCustomModels(api_key, base_url);
                break;

            default:
                throw new Error(`Unknown provider type: ${api_type}`);
        }

        return NextResponse.json({
            success: true,
            models: models,
            count: models.length,
        } as ModelsResponse);

    } catch (error: any) {
        console.error("Error fetching models:", error);
        return NextResponse.json(
            {
                success: false,
                models: [],
                error: error.message || "Failed to fetch models",
            } as ModelsResponse,
            { status: 500 }
        );
    }
}
