import { CopilotKitProvider } from "@copilotkit/react-core/v2";
import "@copilotkit/react-core/v2/styles.css";
import { createRoot } from "react-dom/client";
import { App } from "./App";
import { catalogue } from "./catalogue";

// Catalogue A2UI de la page (base + composants bancaires) : la page sait rendre
// ses composants, et leur schéma est envoyé à l'agent dans le contexte de chaque requête.
createRoot(document.getElementById("root")!).render(
  <CopilotKitProvider runtimeUrl="http://localhost:4000/api/copilotkit" a2ui={{ catalog: catalogue }}>
    <App />
  </CopilotKitProvider>,
);
