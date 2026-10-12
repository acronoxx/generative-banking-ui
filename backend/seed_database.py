
import random
import hashlib
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import insert, select, func
from sqlalchemy.orm import Session

# Charge les modèles du projet
from backend.database import engine
from backend.models import (
    Advisor,
    Customer,
    User,
    BankingProduct,
    Category,
    Account,
    Subscription,
    Card,
    BankTransaction,
)


# ---------------- CONFIGURATION ----------------

SEED = 20261012
TODAY = date.today()
BATCH_SIZE = 5000

NB_CUSTOMERS = 100_000
NB_ADVISORS = 500
NB_ACCOUNTS = 150_000
NB_SUBSCRIPTIONS = 120_000
NB_CARDS = 120_000
NB_TRANSACTIONS = 1_000_000

rng = random.Random(SEED)


# ---------------- DONNÉES SYNTHÉTIQUES ----------------

FIRST_NAMES = """
Adam Adel Adèle Adrien Agathe Ahmed Aïcha Aïdan Alain Alan Alba
Alex Alexandre Alexandra Alexis Alice Alicia Ali Amine Anaïs André
Andréa Anna Anne Anthony Antoine Antonin Aria Arnaud Arthur Aya
Baptiste Bastien Benjamin Bilal Boris Camille Capucine Carla Carmen
Céleste Chloé Clara Clément Clémence Colin Constance Corentin
Damien Daniel David Dorian Éden Édouard Élena Élia Élias Élise
Éloïse Elsa Emma Enzo Éric Ethan Eva Evan Fabien Fatima
Félix Florian François Gabriel Gaël Gaspard Guillaume Hana
Hannah Hélène Hugo Ibrahim Ilan Inaya Inès Iris Isaac Ismaël
Jade Jean Jérémy Jérôme Jeanne Jihane Joseph Jules Julia
Juliette Karim Kenza Kevin Léo Léa Léna Lina Lisa Louis
Louise Lucas Lucie Ludovic Maël Maëlys Malik Manon Marc
Margaux Maria Marie Marion Mathéo Mathilde Mathieu Maxandre Mehdi Mélanie
Mila Mohamed Morgane Myriam Nadia Naël Nathan Nicolas Nina
Noah Nora Nour Océane Olivier Omar Oscar Pablo Paul Pauline
Raphaël Rayan Rémi Romain Rose Salma Sam Sami Sarah Sacha
Sana Sofiane Sofia Sonia Soraya Théo Thomas Timothée Yanis
Yasmine Youssef Zoé Zayn
""".split()

LAST_NAMES = """
Abadie Adam Albert Allard André Antoine Arnaud Aubert Auger
Bailly Barbier Barreau Barthelemy Benali Bernard Bertin Bertrand
Besson Blanc Blanchard Bonnet Boucher Boulanger Bourgeois Boyer
Brun Brunet Caron Carpentier Carreaux Cartier Charles Chevalier
Clement Colin Collin Cordier Costa Cousin Da Costa Daniel David
Delattre Delmas Denis Deschamps Diallo Didier Dubois Dufour
Dumas Dumont Dupont Durand Duval Fabre Faure Fernandes Fernandez
Fleury Fontaine Fournier François Garcia Garnier Gautier Gauthier
Germain Giraud Girard Gomes Gonzalez Gosselin Gregoire Guerin
Guillaume Guillon Henry Hernandez Hubert Huet Jacques Jean
Joly Julien Lambert Laurent Leblanc Leclerc Lefebvre Lefevre
Legrand Lemaire Leroy Leroux Lévêque Lopez Louis Lucas Marchand
Marie Marin Martel Martin Martinez Masson Mathieu Meunier Meyer
Michel Millet Moreau Morel Morin Muller Noel Olivier Payet
Perrin Petit Philippe Picard Pierre Pires Poirier Renard Richard
Robert Robin Roger Rolland Rousseau Roux Roy Sanchez Schmitt
Simon Thomas Torres Vincent Wagner Weber
""".split()

CITIES = [
    ("Paris", "75000"),
    ("Marseille", "13000"),
    ("Lyon", "69000"),
    ("Toulouse", "31000"),
    ("Nice", "06000"),
    ("Nantes", "44000"),
    ("Montpellier", "34000"),
    ("Strasbourg", "67000"),
    ("Bordeaux", "33000"),
    ("Lille", "59000"),
    ("Rennes", "35000"),
    ("Reims", "51100"),
    ("Le Havre", "76600"),
    ("Saint-Étienne", "42000"),
    ("Toulon", "83000"),
    ("Grenoble", "38000"),
    ("Dijon", "21000"),
    ("Angers", "49000"),
    ("Nîmes", "30000"),
    ("Villeurbanne", "69100"),
    ("Clermont-Ferrand", "63000"),
    ("Aix-en-Provence", "13100"),
    ("Brest", "29200"),
    ("Tours", "37000"),
    ("Amiens", "80000"),
    ("Limoges", "87000"),
    ("Annecy", "74000"),
    ("Perpignan", "66000"),
    ("Boulogne-Billancourt", "92100"),
    ("Besançon", "25000"),
    ("Orléans", "45000"),
    ("Metz", "57000"),
    ("Rouen", "76000"),
    ("Mulhouse", "68100"),
    ("Caen", "14000"),
    ("Nancy", "54000"),
    ("Argenteuil", "95100"),
    ("Montreuil", "93100"),
    ("Saint-Denis", "93200"),
    ("Avignon", "84000"),
    ("Poitiers", "86000"),
    ("La Rochelle", "17000"),
    ("Pau", "64000"),
    ("Calais", "62100"),
    ("Cannes", "06400"),
    ("Antibes", "06600"),
    ("Colmar", "68000"),
    ("Versailles", "78000"),
    ("Courbevoie", "92400"),
    ("Vitry-sur-Seine", "94400"),
    ("Créteil", "94000"),
    ("Chambéry", "73000"),
    ("Lorient", "56100"),
    ("Vannes", "56000"),
    ("Quimper", "29000"),
    ("Saint-Malo", "35400"),
    ("Cholet", "49300"),
    ("Bayonne", "64100"),
    ("Biarritz", "64200"),
    ("Narbonne", "11100"),
    ("Carcassonne", "11000"),
    ("Tarbes", "65000"),
    ("Albi", "81000"),
    ("Béziers", "34500"),
    ("Valence", "26000"),
    ("Bourges", "18000"),
    ("Chartres", "28000"),
    ("Évreux", "27000"),
    ("Compiègne", "60200"),
    ("Troyes", "10000"),
    ("Chalon-sur-Saône", "71100"),
    ("Auxerre", "89000"),
    ("Nevers", "58000"),
    ("Mâcon", "71000"),
    ("La Roche-sur-Yon", "85000"),
    ("Niort", "79000"),
    ("Angoulême", "16000"),
    ("Brive-la-Gaillarde", "19100"),
    ("Saint-Brieuc", "22000"),
    ("Laval", "53000"),
    ("Épinal", "88000"),
    ("Belfort", "90000"),
    ("Forbach", "57600"),
    ("Thionville", "57100"),
    ("Sète", "34200"),
    ("Fréjus", "83600"),
    ("Arles", "13200"),
    ("Grasse", "06130"),
    ("Menton", "06500"),
    ("Ajaccio", "20000"),
    ("Bastia", "20200"),
    ("Fort-de-France", "97200"),
    ("Pointe-à-Pitre", "97110"),
    ("Saint-Denis de La Réunion", "97400"),
    ("Cayenne", "97300"),
    ("Mamoudzou", "97600"),
]

STREETS = [
    "rue de la Paix", "avenue Victor Hugo", "rue des Fleurs",
    "boulevard de la République", "rue du Général Leclerc",
    "avenue Jean Jaurès", "rue Pasteur", "rue des Écoles",
    "place du Marché", "rue des Lilas", "avenue de la Gare",
    "rue des Acacias", "rue des Tilleuls", "rue des Érables",
    "boulevard des Alliés", "rue du Moulin", "rue de Bretagne",
    "avenue de la Liberté", "rue des Jardins", "rue du Port",
    "rue de Verdun", "avenue de l'Europe", "rue des Vignes",
    "rue du Stade", "rue des Artisans", "rue de l'Église",
    "rue du Château", "boulevard Victor Schoelcher",
    "avenue du Président Wilson", "rue des Carmes",
    "rue des Augustins", "rue du Faubourg", "rue des Peupliers",
    "rue du Parc", "avenue des Pins", "rue de la Fontaine",
    "rue du 8-Mai-1945", "rue du 11-Novembre",
    "rue des Champs", "rue des Rosiers", "rue des Mimosas",
]

CATEGORY_NAMES = [
    "Alimentation", "Restaurants", "Transport", "Logement",
    "Santé", "Abonnements", "Télécommunications", "Maison",
    "Loisirs", "Achats", "Services", "Sport", "Salaire",
    "Virement", "Retrait", "Frais bancaires", "Épargne",
    "Impôts", "Voyage", "Assurance","Autres"
]

PRODUCTS = [
    ("Compte Essentiel", "Compte courant", "current_account", "2.50"),
    ("Compte Jeune", "Compte pour jeunes adultes", "current_account", "0.00"),
    ("Compte Premium", "Compte avec services étendus", "current_account", "12.00"),
    ("Livret Horizon", "Produit d'épargne fictif", "savings", "0.00"),
    ("Carte Classique", "Carte de démonstration", "card", "3.00"),
    ("Carte Premium", "Carte avec plafonds supérieurs", "card", "9.00"),
    ("Pack Famille", "Offre groupée fictive", "package", "8.00"),
    ("Assurance Voyage", "Assurance de démonstration", "insurance", "4.00"),
    ("Compte Professionnel", "Compte professionnel fictif", "business_account", "9.00"),
    ("Épargne Projet", "Épargne associée à un objectif", "savings", "0.00"),
]

MERCHANTS = [
    ("Carrefour", "Alimentation"),
    ("Monoprix", "Alimentation"),
    ("Restaurant du Centre", "Restaurants"),
    ("SNCF Connect", "Transport"),
    ("RATP", "Transport"),
    ("EDF", "Logement"),
    ("Netflix", "Abonnements"),
    ("Free Mobile", "Télécommunications"),
    ("IKEA", "Maison"),
    ("Fnac", "Loisirs"),
    ("Amazon", "Achats"),
    ("Pharmacie Centrale", "Santé"),
]

# ---------------- OUTILS ----------------

def batches(rows, size=BATCH_SIZE):
    for start in range(0, len(rows), size):
        yield rows[start:start + size]


def count_rows(session, model):
    return session.scalar(
        select(func.count()).select_from(model)
    ) or 0


def make_pin_hash(username):
    # Hash synthétique : aucune donnée secrète réelle n'est utilisée.
    salt = hashlib.sha256(username.encode()).hexdigest()[:32]
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        b"synthetic-demo-pin",
        salt.encode(),
        100_000,
    ).hex()
    return f"pbkdf2_sha256$100000${salt}${digest}"


def make_iban(number):
    # IBAN synthétique au format français ; ce n'est pas un compte réel.
    bban = (
        f"{20000 + number % 70000:05d}"
        f"{10000 + number % 80000:05d}"
        f"{number:011d}"
        f"{number % 97:02d}"
    )
    check_input = bban + "FR00"
    numeric = check_input.replace("F", "15").replace("R", "27")
    check_digits = 98 - int(numeric) % 97
    return f"FR{check_digits:02d}{bban}"


def insert_in_batches(session, model, rows):
    for batch in batches(rows):
        session.execute(insert(model), batch)
        session.flush()


# ---------------- GÉNÉRATION ----------------

def main():
    with Session(engine) as session:

        models = [
            Advisor, Customer, User, BankingProduct, Category,
            Account, Subscription, Card, BankTransaction,
        ]

        # Sécurité : ne pas dupliquer ni effacer des données existantes.
        existing = {
            model.__tablename__: count_rows(session, model)
            for model in models
        }

        non_empty = {
            table: count
            for table, count in existing.items()
            if count > 0
        }

        if non_empty:
            raise RuntimeError(
                f"La base contient déjà des données : {non_empty}. "
                "Arrêt pour éviter les doublons."
            )

        print("1/9 - Génération des conseillers...")

        advisor_rows = [
            {
                "name": f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}",
                "email": f"advisor{i:05d}@example.test",
                "phone": f"+339{i:08d}",
                "specialisation": rng.choice(
                    ["Épargne", "Crédit", "Patrimoine", "Comptes courants"]
                ),
                "status": "active",
            }
            for i in range(1, NB_ADVISORS + 1)
        ]
        insert_in_batches(session, Advisor, advisor_rows)
        advisor_ids = list(
            session.scalars(select(Advisor.id).order_by(Advisor.id))
        )

        print("2/9 - Génération des produits et catégories...")

        product_rows = [
            {
                "name": name,
                "description": description,
                "product_type": product_type,
                "monthly_fee": Decimal(fee),
                "status": "active",
            }
            for name, description, product_type, fee in PRODUCTS
        ]
        insert_in_batches(session, BankingProduct, product_rows)

        category_rows = [
            {"name": name, "description": f"Catégorie : {name}"}
            for name in CATEGORY_NAMES
        ]
        insert_in_batches(session, Category, category_rows)

        product_ids = list(
            session.scalars(select(BankingProduct.id))
        )
        category_by_name = dict(
            session.execute(select(Category.name, Category.id)).all()
        )

        print("3/9 - Génération des clients...")

        customer_rows = []

        for i in range(1, NB_CUSTOMERS + 1):
            city, postal_code = rng.choice(CITIES)

            customer_rows.append({
                "first_name": rng.choice(FIRST_NAMES),
                "last_name": rng.choice(LAST_NAMES),
                "email": f"customer{i:07d}@example.test",
                "phone": f"+336{rng.randrange(10**8):08d}",
                "date_of_birth": date(
                    rng.randint(1940, 2005),
                    rng.randint(1, 12),
                    rng.randint(1, 28),
                ),
                "address": (
                    f"{rng.randint(1, 200)} "
                    f"{rng.choice(STREETS)}"
                ),
                "city": city,
                "postal_code": postal_code,
                "country": "France",
                "status": rng.choices(
                    ["active", "dormant", "closed"],
                    weights=[92, 7, 1],
                )[0],
                "advisor_id": (
                    rng.choice(advisor_ids)
                    if rng.random() < 0.92 else None
                ),
            })

        insert_in_batches(session, Customer, customer_rows)

        customer_data = list(
            session.execute(
                select(Customer.id, Customer.advisor_id)
            )
        )
        customer_ids = [row.id for row in customer_data]

        print("4/9 - Génération des utilisateurs...")

        user_rows = []

        for customer_id in customer_ids:
            username = f"customer_{customer_id:07d}"
            user_rows.append({
                "username": username,
                "app_pin_hash": make_pin_hash(username),
                "app_pin_failed_attempts": 0,
                "app_pin_locked_until": None,
                "role": "customer",
                "status": "active",
                "created_at": TODAY,
                "customer_id": customer_id,
                "advisor_id": None,
            })

        for advisor_id in advisor_ids:
            username = f"advisor_{advisor_id:05d}"
            user_rows.append({
                "username": username,
                "app_pin_hash": make_pin_hash(username),
                "app_pin_failed_attempts": 0,
                "app_pin_locked_until": None,
                "role": "advisor",
                "status": "active",
                "created_at": TODAY,
                "customer_id": None,
                "advisor_id": advisor_id,
            })

        user_rows.append({
            "username": "admin_demo",
            "app_pin_hash": make_pin_hash("admin_demo"),
            "app_pin_failed_attempts": 0,
            "app_pin_locked_until": None,
            "role": "admin",
            "status": "active",
            "created_at": TODAY,
            "customer_id": None,
            "advisor_id": None,
        })

        insert_in_batches(session, User, user_rows)

        print("5/9 - Génération des comptes bancaires...")

        account_rows = []

        for i in range(1, NB_ACCOUNTS + 1):
            account_rows.append({
                "customer_id": rng.choice(customer_ids),
                "iban": make_iban(i),
                "account_type": rng.choices(
                    ["current", "savings", "joint"],
                    weights=[78, 18, 4],
                )[0],
                "currency": "EUR",
                "balance": Decimal(rng.randint(100, 8000)),
                "status": "active",
                "opened_at": datetime.now(timezone.utc)
                - timedelta(days=rng.randint(220, 3000)),
            })

        insert_in_batches(session, Account, account_rows)

        account_data = list(
            session.execute(
                select(Account.id, Account.customer_id, Account.opened_at)
            )
        )
        account_ids = [row.id for row in account_data]
        accounts_by_customer = {}

        for row in account_data:
            accounts_by_customer.setdefault(row.customer_id, []).append(row.id)

        print("6/9 - Génération des abonnements...")

        subscription_rows = []

        for _ in range(NB_SUBSCRIPTIONS):
            start_date = TODAY - timedelta(days=rng.randint(30, 2000))
            subscription_rows.append({
                "customer_id": rng.choice(customer_ids),
                "product_id": rng.choice(product_ids),
                "status": rng.choices(
                    ["active", "cancelled", "suspended"],
                    weights=[84, 13, 3],
                )[0],
                "start_date": start_date,
                "end_date": None,
            })

        insert_in_batches(session, Subscription, subscription_rows)

        subscription_data = list(
            session.execute(
                select(Subscription.id, Subscription.customer_id)
            )
        )
        subscriptions_by_customer = {}

        for row in subscription_data:
            subscriptions_by_customer.setdefault(row.customer_id, []).append(row.id)

        print("7/9 - Génération des cartes...")

        cards_by_account = {}
        card_rows = []

        for i in range(1, NB_CARDS + 1):
            account_id, customer_id, opened_at = rng.choice(account_data)
            valid_from = max(
                opened_at.date(),
                TODAY - timedelta(days=rng.randint(30, 1000)),
            )
            expires_at = valid_from + timedelta(days=3 * 365)
            last4 = f"{rng.randrange(10000):04d}"

            customer_subscriptions = subscriptions_by_customer.get(
                customer_id, []
            )
            subscription_id = (
                rng.choice(customer_subscriptions)
                if customer_subscriptions and rng.random() < 0.8
                else None
            )

            card_rows.append({
                "account_id": account_id,
                "subscription_id": subscription_id,
                "card_token": f"tok_test_{i:09d}",
                "card_number_test": f"9999{i:012d}",
                "last_four_digits": last4,
                "expiry_month": expires_at.month,
                "expiry_year": expires_at.year,
                "card_type": rng.choice(["debit", "credit", "virtual"]),
                "physical_type": rng.choice(["physical", "virtual"]),
                "daily_payment_limit": Decimal("1000.00"),
                "monthly_payment_limit": Decimal("5000.00"),
                "daily_withdrawal_limit": Decimal("300.00"),
                "currency": "EUR",
                "status": "active",
                "valid_from": valid_from,
                "expires_at": expires_at,
                "created_at": datetime.combine(
                    valid_from, datetime.min.time(), tzinfo=timezone.utc
                ),
            })

            cards_by_account.setdefault(account_id, [])

        insert_in_batches(session, Card, card_rows)

        card_data = list(
            session.execute(select(Card.id, Card.account_id))
        )
        cards_by_account = {}

        for row in card_data:
            cards_by_account.setdefault(row.account_id, []).append(row.id)

        print("8/9 - Génération des transactions...")

        transaction_types = [
            "card_payment", "direct_debit", "withdrawal",
            "transfer_out", "bank_fee", "salary",
            "transfer_in", "refund", "cash_deposit",
        ]
        weights = [42, 17, 8, 12, 3, 8, 5, 3, 2]

        for start in range(0, NB_TRANSACTIONS, BATCH_SIZE):
            stop = min(start + BATCH_SIZE, NB_TRANSACTIONS)
            transaction_rows = []

            for i in range(start, stop):
                account_id, customer_id, opened_at = rng.choice(account_data)
                tx_type = rng.choices(
                    transaction_types, weights=weights, k=1
                )[0]

                if tx_type == "salary":
                    amount = Decimal(rng.randint(1500, 4200))
                    merchant = "Employeur Exemple"
                    category_name = "Salaire"
                elif tx_type in ("transfer_in", "transfer_out"):
                    amount = Decimal(rng.randint(20, 1800))
                    merchant = None
                    category_name = "Virement"
                elif tx_type == "withdrawal":
                    amount = Decimal(rng.randint(20, 200))
                    merchant = "Distributeur automatique"
                    category_name = "Retrait"
                elif tx_type == "bank_fee":
                    amount = Decimal(rng.randint(1, 25))
                    merchant = "Frais bancaires"
                    category_name = "Frais bancaires"
                elif tx_type in ("refund", "cash_deposit"):
                    amount = Decimal(rng.randint(5, 300))
                    merchant = "Opération de démonstration"
                    category_name = (
                        "Épargne" if tx_type == "cash_deposit"
                        else "Achats"
                    )
                else:
                    amount = Decimal(rng.randint(3, 400))
                    merchant, category_name = rng.choice(MERCHANTS)

                tx_day = TODAY - timedelta(days=rng.randint(0, 180))
                tx_dt = datetime.combine(
                    tx_day,
                    datetime.min.time(),
                    tzinfo=timezone.utc,
                ) + timedelta(
                    hours=rng.randint(7, 22),
                    minutes=rng.randint(0, 59),
                )

                possible_cards = cards_by_account.get(account_id, [])
                card_id = (
                    rng.choice(possible_cards)
                    if possible_cards
                    and tx_type in ("card_payment", "withdrawal")
                    and rng.random() < 0.85
                    else None
                )

                transaction_rows.append({
                    "type": tx_type,
                    "amount": amount,
                    "currency": "EUR",
                    "description": f"Transaction synthétique {tx_type}",
                    "merchant": merchant,
                    "reference": f"DEMO-{i + 1:010d}",
                    "transaction_date": tx_dt,
                    "booked_at": tx_dt + timedelta(minutes=5),
                    "status": "completed",
                    "account_id": account_id,
                    "category_id": category_by_name.get(
                        category_name, category_by_name["Autres"]
                    ),
                    "card_id": card_id,
                })

            session.execute(insert(BankTransaction), transaction_rows)

            if stop % 100_000 == 0 or stop == NB_TRANSACTIONS:
                print(f"  {stop:,} transactions générées".replace(",", " "))

        print("9/9 - Validation et sauvegarde...")
        session.commit()

        for model in models:
            print(
                f"{model.__tablename__}: {count_rows(session, model):,}"
                .replace(",", " ")
            )

        print("\nDataset synthétique généré avec succès.")


if __name__ == "__main__":
    main()
