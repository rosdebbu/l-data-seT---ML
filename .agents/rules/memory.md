# Persistent Memory — Roshni's Workspace

## Hardware & Setup
- **Laptop**: Lenovo with NVIDIA GeForce RTX 5050 Laptop GPU (8 GB VRAM)
- **Driver**: NVIDIA Driver 610.88, CUDA 13.3
- **OS**: Windows 11

## Local AI Setup (Completed 2026-08-15)
- **Ollama**: Installed natively on Windows (`v0.32.13`)
  - Models: `qwen2.5-coder:7b` (coding), `deepseek-r1:8b` (reasoning)
  - Endpoint: `http://localhost:11434/v1`
- **DeepSeek Harness (dsh)**: Installed (`@deepseek-ai/dsh@0.1.0-rc.6`)
  - Web UI: `http://localhost:3080`
  - Provider: `openai` pointing to local Ollama
  - Config: `~/.dsh/settings.yaml`

## User Preferences
- Prefers local/offline AI tools (privacy-conscious)
- Interested in ML, Data Science, and AI model fine-tuning
- Uses GitHub for version control
- Workspace: `l-data-seT---ML` repository
- Prefers simple step-by-step instructions
- Interested in: Unsloth (fine-tuning), Win11Debloat (system optimization)

## Tools Explored
- Ollama (local LLM runner) ✅ Installed
- DeepSeek Harness (AI agent framework) ✅ Installed
- Unsloth (fine-tuning & training) — Interested, not yet installed
- Win11Debloat (Windows optimization) — Interested, not yet run
- DeepSeek V4 (cloud) — Available free at chat.deepseek.com

## Key Learnings
- Agent = Model + Harness
- Ollama exposes OpenAI-compatible API at localhost:11434/v1
- RTX 5050 can run 7B/8B quantized models comfortably (~6.8GB VRAM)
- RTX 5050 can fine-tune 7B models with QLoRA via Unsloth
