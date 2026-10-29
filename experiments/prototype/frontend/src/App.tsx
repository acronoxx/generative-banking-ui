// Login page until the customer is connected, then the conversation.
// The session token goes in the headers of every request to the CopilotKit runtime,
// which forwards it to the agent (Authorization header).

import { CopilotKitProvider } from "@copilotkit/react-core/v2";
import { useState } from "react";
import { logout } from "./api";
import { catalog } from "./catalog";
import { ChatPage } from "./pages/ChatPage";
import { LoginPage } from "./pages/LoginPage";

export function App() {
  const [token, setToken] = useState<string | null>(null);

  if (!token) return <LoginPage onLogin={setToken} />;

  return (
    <CopilotKitProvider
      runtimeUrl={import.meta.env.VITE_RUNTIME_URL}
      headers={{ Authorization: `Bearer ${token}` }}
      a2ui={{ catalog }}
    >
      <ChatPage onLogout={() => logout().finally(() => setToken(null))} />
    </CopilotKitProvider>
  );
}
