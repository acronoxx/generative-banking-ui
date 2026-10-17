// WebMCP : la page déclare ses outils au navigateur, avec un nom, une description
// et un schéma de paramètres, au lieu de laisser un agent lire et cliquer dans l'interface.

import { z } from "zod";
import { OUTILS } from "./outils";

type ContexteModele = {
  registerTool: (outil: object, options?: { signal?: AbortSignal }) => Promise<void>;
};

export function enregistrerOutilsWebMCP() {
  const contexte = (document as { modelContext?: ContexteModele }).modelContext;
  if (!contexte) return; // navigateur sans WebMCP : les outils restent transmis à l'agent

  const arret = new AbortController();
  for (const outil of OUTILS) {
    contexte
      .registerTool(
        {
          name: outil.name,
          description: outil.description,
          inputSchema: z.toJSONSchema(outil.parameters),
          annotations: { readOnlyHint: true },
          execute: async (parametres: never) => JSON.stringify(await outil.handler(parametres)),
        },
        { signal: arret.signal },
      )
      .catch(() => {});
  }

  // Les outils sont retirés quand la page est démontée
  return () => arret.abort();
}
