import { CopilotKitProvider } from "@copilotkit/react-core/v2";
import "@copilotkit/react-core/v2/styles.css";
import { createRoot } from "react-dom/client";
import { App } from "./App";

createRoot(document.getElementById("root")!).render(
  <CopilotKitProvider runtimeUrl="http://localhost:4000/api/copilotkit">
    <App />
  </CopilotKitProvider>,
);
