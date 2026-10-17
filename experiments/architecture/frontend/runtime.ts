// Runtime CopilotKit (port 4000) : le relais entre la page et l'agent.
// Il parle AG-UI avec l'agent Python et transforme les interfaces A2UI
// qu'il produit en surfaces à afficher.

import { HttpAgent } from "@ag-ui/client";
import { CopilotRuntime } from "@copilotkit/runtime/v2";
import { createCopilotExpressHandler } from "@copilotkit/runtime/v2/express";
import express from "express";

const runtime = new CopilotRuntime({
  agents: { default: new HttpAgent({ url: "http://127.0.0.1:8000/" }) },
  a2ui: {},
});

const app = express();
app.use(createCopilotExpressHandler({ runtime, basePath: "/api/copilotkit" }));
app.listen(4000, () => console.log("Runtime CopilotKit : http://localhost:4000/api/copilotkit"));
