// Serveur de l'agent : reçoit la conversation et renvoie le flux de messages
// au format attendu par useChat (parties texte, appel d'outil, résultat).
import "dotenv/config";
import { createServer } from "node:http";
import { pipeAgentUIStreamToResponse } from "ai";
import { agent } from "./agent.ts";

const PORT = 4100;

createServer(async (req, res) => {
  if (req.method !== "POST" || req.url !== "/api/chat") {
    res.writeHead(404).end();
    return;
  }
  let corps = "";
  for await (const morceau of req) corps += morceau;

  try {
    const { messages } = JSON.parse(corps);
    await pipeAgentUIStreamToResponse({ response: res, agent, uiMessages: messages });
  } catch (erreur) {
    console.error(erreur);
    if (!res.headersSent) res.writeHead(500).end(String(erreur));
  }
}).listen(PORT, () => console.log(`Agent prêt sur http://localhost:${PORT}/api/chat`));
