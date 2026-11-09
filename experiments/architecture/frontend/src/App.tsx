import { CopilotChat, useFrontendTool } from "@copilotkit/react-core/v2";
import { useEffect } from "react";
import { consulterComptes, consulterTransactions } from "./outils";
import { enregistrerOutilsWebMCP } from "./webmcp";

export function App() {
  // Déclaration des outils au navigateur (WebMCP)
  useEffect(() => enregistrerOutilsWebMCP(), []);

  // Les mêmes outils sont transmis à l'agent à chaque requête AG-UI.
  // Quand l'agent en appelle un, il est exécuté ici, dans la page.
  useFrontendTool(consulterComptes);
  useFrontendTool(consulterTransactions);

  // CopilotChat consomme les événements AG-UI : texte en streaming, appels d'outils
  // et surfaces A2UI, rendues avec les composants du catalogue.
  return (
    <main style={{ height: "100vh", maxWidth: 760, margin: "0 auto" }}>
      <CopilotChat labels={{ chatInputPlaceholder: "Posez une question sur vos comptes" }} />
    </main>
  );
}
