// Transfer prepared by the agent (data: prepare_transfer, schema TransferSimulationOut).
// The customer confirms it here with their password: the page calls the backend
// directly (POST /api/transfers/{id}/confirm), the agent never confirms a transfer.

import { DynamicStringSchema } from "@copilotkit/a2ui-renderer";
import { useState } from "react";
import { cancelTransfer, confirmTransfer } from "../api";
import { type CatalogEntry, card, props, z } from "./schema";

type Props = { simulationId: number; beneficiaryName: string; amount: string; reason: string };

function Confirmation({ props }: { props: Props }) {
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState<string | null>(null);

  const run = (action: () => Promise<{ status: string }>) =>
    action().then(
      (result) => setStatus(result.status === "confirmed" ? "Virement effectué." : "Virement annulé."),
      (error: Error) => setStatus(`Erreur : ${error.message}`),
    );

  return (
    <div style={card}>
      <div style={{ fontWeight: 600 }}>Virement à confirmer</div>
      <div>
        {props.amount} à {props.beneficiaryName} — {props.reason}
      </div>
      {status ? (
        <div style={{ marginTop: 8 }}>{status}</div>
      ) : (
        <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
          <input
            type="password"
            placeholder="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={() => run(() => confirmTransfer(props.simulationId, password))}>Confirmer</button>
          <button onClick={() => run(() => cancelTransfer(props.simulationId))}>Annuler</button>
        </div>
      )}
    </div>
  );
}

export const TransferConfirmation: CatalogEntry = {
  definition: {
    description: "Summary of a prepared transfer, with the password field and the confirm and cancel buttons.",
    props: props({
      simulationId: z.number().describe("id returned by prepare_transfer"),
      beneficiaryName: DynamicStringSchema.describe("Name of the beneficiary"),
      amount: DynamicStringSchema.describe("Formatted amount, for example « 50,00 € »"),
      reason: DynamicStringSchema.describe("Reason of the transfer"),
    }),
  },
  render: Confirmation,
};
