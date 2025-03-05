# Agent UI

A modern chat interface for AI agents built with Next.js, Tailwind CSS, and TypeScript. This template provides a ready-to-use UI for interacting with Agno agents.

![image (1)](https://github.com/user-attachments/assets/7dfb6c34-7164-4497-a961-0030d684ecab)

## Features

- 💬 **Modern Chat Interface**: Clean, responsive design with message streaming support
- 🔄 **Real-time Streaming**: Stream AI responses as they're generated
- 🧩 **Tool Calls Support**: Visualize agent tool calls and their results
- 🧠 **Reasoning Steps**: Display agent reasoning process (when available)
- 🔌 **API Integration**: Connect to any compatible AI agent backend
- 🎨 **Customizable UI**: Built with Tailwind CSS for easy styling
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🔍 **Agent Selection**: Switch between different AI agents
- 🌙 **Dark Mode Support**: Toggle between light and dark themes
- 🧰 **Built with Modern Stack**: Next.js, TypeScript, Zustand, and more

## Getting Started

### Prerequisites

- Node.js 18.x or later
- npm, yarn, or pnpm

### Installation

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

This UI template is designed to connect to any compatible AI agent backend that exposes a REST API. By default, it connects to `http://localhost:7777`, but you can change this in the UI or update the default in the code.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or raise an issue.

1. For bugs and feature requests, please raise a ticket first
2. Fork the repository
3. Create your feature branch (`git checkout -b feature/amazing-feature`)
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
