package fr.imt.mesures;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

// Essai préparé mais NON compilé : aucun JDK n'était installé sur le poste.
// Lancement : GOOGLE_API_KEY=... mvn spring-boot:run
@SpringBootApplication
public class Mesures {

    static final String FRAMEWORK = "Spring AI";
    static final int REPETITIONS = 10;
    static final int PAUSE_MS = 10_000; // pause entre deux essais, pour respecter le quota gratuit

    record Scenario(String question, Set<String> outilsAttendus) {}

    // Chaque scénario : une question et les outils qui doivent être appelés
    static final List<Scenario> SCENARIOS = List.of(
            new Scenario("Quel est le solde de mon compte courant ?", Set.of("get_balance")),
            new Scenario("Quelles dépenses dépassent 500 € ?", Set.of("get_transactions")),
            new Scenario("Quel est mon solde courant, et quelles dépenses dépassent 500 € ?",
                    Set.of("get_balance", "get_transactions")),
            new Scenario("Bonjour, que peux-tu faire pour moi ?", Set.of()));

    public static void main(String[] args) {
        SpringApplication.run(Mesures.class, args);
    }

    @Bean
    CommandLineRunner mesurer(ChatModel chatModel) {
        return args -> {
            ChatClient client = ChatClient.create(chatModel);
            OutilsBancaires outils = new OutilsBancaires();

            System.out.println("framework;question;duree_mediane_s;duree_min_s;duree_max_s;"
                    + "tokens_entree;tokens_sortie;reussite;erreurs");

            for (Scenario scenario : SCENARIOS) {
                List<Double> durees = new ArrayList<>();
                List<Integer> entrees = new ArrayList<>(), sorties = new ArrayList<>();
                int reussites = 0;

                for (int i = 0; i < REPETITIONS; i++) {
                    outils.appeles.clear();
                    long debut = System.nanoTime();
                    ChatResponse reponse;
                    try {
                        reponse = client.prompt()
                                .system("Tu es un assistant bancaire. Utilise les outils, n'invente jamais de données.")
                                .user(scenario.question())
                                .tools(outils)
                                .call()
                                .chatResponse();
                    } catch (Exception erreur) {
                        System.out.println("  essai en échec : " + erreur.getClass().getSimpleName());
                        Thread.sleep(PAUSE_MS);
                        continue;
                    }
                    durees.add((System.nanoTime() - debut) / 1e9);

                    // La documentation ne précise pas si ces compteurs cumulent tous les
                    // appels au modèle ou seulement le dernier : à vérifier avant comparaison.
                    var usage = reponse.getMetadata().getUsage();
                    entrees.add(usage.getPromptTokens() == null ? 0 : usage.getPromptTokens());
                    sorties.add(usage.getCompletionTokens() == null ? 0 : usage.getCompletionTokens());
                    if (outils.appeles.equals(scenario.outilsAttendus())) reussites++;
                    Thread.sleep(PAUSE_MS);
                }

                if (!durees.isEmpty()) {
                    System.out.printf("%s;%s;%.2f;%.2f;%.2f;%.0f;%.0f;%d/%d;%d%n",
                            FRAMEWORK, scenario.question(), mediane(durees),
                            Collections.min(durees), Collections.max(durees),
                            mediane(entrees), mediane(sorties),
                            reussites, durees.size(), REPETITIONS - durees.size());
                }
            }
        };
    }

    static double mediane(List<? extends Number> valeurs) {
        List<Double> tri = valeurs.stream().map(Number::doubleValue).sorted().toList();
        int m = tri.size() / 2;
        return tri.size() % 2 == 1 ? tri.get(m) : (tri.get(m - 1) + tri.get(m)) / 2;
    }
}
