// Conversation minimale : chaque réponse de l'agent est du OpenUI Lang, affiché
// par le Renderer avec les composants du catalogue, au fur et à mesure du flux.
import { Renderer } from "@openuidev/react-lang";
import { useState } from "react";
import { bibliotheque } from "./bibliotheque";

type Message = { role: "user" | "assistant"; content: string };

export function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [saisie, setSaisie] = useState("");
  const [enCours, setEnCours] = useState(false);

  async function envoyer(texte: string) {
    const historique: Message[] = [...messages, { role: "user", content: texte }];
    setMessages([...historique, { role: "assistant", content: "" }]);
    setEnCours(true);

    const reponse = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: historique }),
    });
    const lecteur = reponse.body!.pipeThrough(new TextDecoderStream()).getReader();
    let accumule = "";
    for (;;) {
      const { done, value } = await lecteur.read();
      if (done) break;
      accumule += value;
      setMessages([...historique, { role: "assistant", content: accumule }]);
    }
    setEnCours(false);
  }

  return (
    <main style={{ maxWidth: 640, margin: "0 auto", fontFamily: "system-ui" }}>
      <h1>Assistant bancaire (OpenUI)</h1>
      {messages.map((m, i) =>
        m.role === "user" ? (
          <p key={i} style={{ textAlign: "right" }}>
            <em>{m.content}</em>
          </p>
        ) : (
          <Renderer
            key={i}
            library={bibliotheque}
            response={m.content}
            isStreaming={enCours && i === messages.length - 1}
            // Un clic sur un bouton (confirmer un virement) renvoie un message à l'agent
            onAction={(evenement) => {
              if (evenement.type === "continue_conversation") envoyer(evenement.humanFriendlyMessage);
            }}
          />
        ),
      )}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          if (saisie && !enCours) envoyer(saisie);
          setSaisie("");
        }}
      >
        <input
          value={saisie}
          onChange={(e) => setSaisie(e.target.value)}
          placeholder="Posez une question sur vos comptes"
          style={{ width: "80%" }}
        />
        <button type="submit" disabled={enCours}>
          Envoyer
        </button>
      </form>
    </main>
  );
}
