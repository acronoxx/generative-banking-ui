package fr.imt.mesures;

import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;

public class OutilsBancaires {

    // Outils appelés pendant l'essai en cours
    final Set<String> appeles = new HashSet<>();

    @Tool(name = "get_balance", description = "Renvoie le solde d'un compte ('courant' ou 'livret').")
    public String getBalance(@ToolParam(description = "Nom du compte") String account) {
        appeles.add("get_balance");
        return Map.of("courant", "1 250 €", "livret", "8 400 €").getOrDefault(account, "Compte inconnu");
    }

    @Tool(name = "get_transactions",
          description = "Renvoie les transactions des trois derniers mois supérieures à un montant en euros.")
    public String getTransactions(@ToolParam(description = "Montant minimal en euros") double min_amount) {
        appeles.add("get_transactions");
        Map<String, Integer> transactions = new LinkedHashMap<>();
        transactions.put("Loyer", 780);
        transactions.put("Garage", 620);
        transactions.put("Courses", 95);
        transactions.put("Billets de train", 510);
        String resultat = transactions.entrySet().stream()
                .filter(t -> t.getValue() >= min_amount)
                .map(t -> t.getKey() + " : " + t.getValue() + " €")
                .collect(Collectors.joining("\n"));
        return resultat.isEmpty() ? "Aucune transaction" : resultat;
    }
}
