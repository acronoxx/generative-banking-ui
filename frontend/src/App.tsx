import { CopilotChat } from "@copilotkit/react-core/v2";

export function App() {
  return (
    <main>
      <CopilotChat labels={{ chatInputPlaceholder: "Posez une question sur vos comptes" }} />
    </main>
  );
}
