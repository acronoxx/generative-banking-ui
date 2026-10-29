// Conversation with the agent. CopilotChat consumes the AG-UI events: streamed text,
// tool calls and A2UI surfaces, rendered with the components of the catalog.

import { CopilotChat } from "@copilotkit/react-core/v2";

export function ChatPage({ onLogout }: { onLogout: () => void }) {
  return (
    <main style={{ height: "100vh", maxWidth: 760, margin: "0 auto", display: "flex", flexDirection: "column" }}>
      <div style={{ textAlign: "right", padding: 8 }}>
        <button onClick={onLogout}>Se déconnecter</button>
      </div>
      <div style={{ flex: 1, minHeight: 0 }}>
        <CopilotChat labels={{ chatInputPlaceholder: "Posez une question sur vos comptes" }} />
      </div>
    </main>
  );
}
