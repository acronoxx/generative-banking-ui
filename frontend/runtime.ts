/* Runtime CopilotKit (Port 4000) :
Serves as a relay between the page and the agent.
Uses AG-UI with python agent(s) and transforms A2UI interfaces
that the agent(s) produce(s) into surfaces to print.
*/

import { HttpAgent } from "@ag-ui/client";
import { CopilotRuntime } from "@copilotkit/runtime/v2";
import { createCopilotExpressHandler } from "@copilotkit/runtime/v2/express";
import express from "express";

// Variables from the .env file (see .env.example)
process.loadEnvFile();
const AGENT_URL = process.env.AGENT_URL ?? "http://127.0.0.1:8001/";
const PORT = Number(process.env.RUNTIME_PORT ?? 4000);

const runtime = new CopilotRuntime({
    agents: { default: new HttpAgent({ url: AGENT_URL }) },
    a2ui: {},
});

const app = express();
app.use(createCopilotExpressHandler({ runtime, basePath: "/api/copilotkit" }));
app.listen(PORT, () =>
    console.log(`Runtime CopilotKit : http://localhost:${PORT}/api/copilotkit (agent : ${AGENT_URL})`),
);
