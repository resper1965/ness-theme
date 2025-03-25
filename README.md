# Agent UI

A modern chat interface for AI agents built with Next.js, Tailwind CSS, and TypeScript. This template provides a ready-to-use UI for interacting with Agno agents.

<img src="https://github.com/user-attachments/assets/7765fae5-a813-46cb-993b-904af9bc1672" alt="agent-ui" style="border-radius: 10px; width: 100%; max-width: 800px;" />

## Features

- 💬 **Modern Chat Interface**: Clean, responsive design with message streaming support
- 🔍 **Agent Selection**: Switch between different AI agents
- 🔄 **Real-time Streaming**: Stream AI responses as they're generated
- 🧩 **Tool Calls Support**: Visualize agent tool calls and their results
- 🧠 **Reasoning Steps**: Display agent reasoning process (when available)
- 📚 **References Support**: Show sources used by the agent
- 🖼️ **Multi-modality Support**: Handles various content types including images, video, and audio
- 🎨 **Customizable UI**: Built with Tailwind CSS for easy styling
- 🧰 **Built with Modern Stack**: Next.js, TypeScript, shadcn/ui, Framer Motion, and more

## Getting Started

### Prerequisites

Before setting up this UI, you may want to have an Agno playground backend running. If you haven't set up the Agno Playground yet, follow the [official guide](https://docs.agno.com/get-started/playground#running-playground-locally) to run the Playground locally.

### Installation

### Automatic Installation (Recommended)

```bash
npx create agent-ui@latest
```

### Manual Installation

1. Clone the repository:

```bash
git clone https://github.com/agno-agi/agent-ui.git
cd agent-ui
```

2. Install dependencies:

```bash
pnpm install
```

3. Start the development server:

```bash
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Connecting to an Agent Backend

By default Agent UI connects to `http://localhost:7777`. You can easily change this by hovering over the endpoint URL and clicking the edit option.

The default endpoint works with the standard Agno Playground setup described in the [official documentation](https://docs.agno.com/get-started/playground#running-playground-locally).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the [MIT License](./LICENSE).
