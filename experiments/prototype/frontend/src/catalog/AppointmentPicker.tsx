// Advisor and simulated appointment slots (data: get_advisor and get_appointment_slots).
// Choosing a slot books nothing: the database has no calendar.

import { DynamicStringSchema } from "@copilotkit/a2ui-renderer";
import { useState } from "react";
import { type CatalogEntry, card, props, z } from "./schema";

type Props = { advisorName: string; slots: string[] };

function Picker({ props }: { props: Props }) {
  const [chosen, setChosen] = useState<string | null>(null);
  return (
    <div style={card}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>Rendez-vous avec {props.advisorName}</div>
      {chosen ? (
        <div>Rendez-vous simulé le {chosen}.</div>
      ) : (
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          {props.slots.map((slot) => (
            <button key={slot} onClick={() => setChosen(slot)}>
              {slot}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export const AppointmentPicker: CatalogEntry = {
  definition: {
    description: "Advisor name and buttons to choose one of the appointment slots.",
    props: props({
      advisorName: DynamicStringSchema.describe("Name of the advisor"),
      slots: z.array(z.string()).describe("Formatted slots, for example « jeudi 30/10 à 10h00 »"),
    }),
  },
  render: Picker,
};
