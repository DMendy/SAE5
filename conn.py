from bson import ObjectId
from pymongo import MongoClient
import sys
from datetime import datetime


"""
Bienvenue dans notre TP. 
Il consiste en l'utilisation de la base de données que nous hébergeons sur notre RPI5.
L'IP de notre RPI est 192.168.25.24, et la base de données est sur le port 27017. Le user auquel se connecter est admin et son mdp est password.
La base d'authentification de tout cela se nomme elle aussi admin
"""


"""
A l'aide du texte precedent, complete les variables suivantes pour pouvoir te connecter à notre base de données
"""
# Paramètres de connexion
rpi_ip = None
mongo_port = None
mongo_user = None
mongo_password = None
auth_db = None

# URI de connexion MongoDB
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{rpi_ip}:{mongo_port}/?authSource={auth_db}"
mongo_uri2 = f"mongodb://admin:password@192.168.25.24:27017/?authSource=admin"


# Connexion à MongoDB
def connect_mongo():
    try:
        print(f"Connexion à MongoDB sur {rpi_ip}:{mongo_port}...")
        client = MongoClient(mongo_uri2)
        print("Connexion réussie à MongoDB!")
        return client
    except Exception as e:
        print(f"Erreur de connexion à MongoDB : {e}")
        sys.exit(1)

def show_tables(db):
    return db.list_collection_names()



"""
A l'aide de la fonction insert_client, insère une ligne client dans la base de donnée
"""
def insert_client(db, nom, prenom, email, dateInscription):
    db.clients.insert_one({
        "nom": nom,
        "prenom": prenom,
        "email": email,
        "dateInscription": datetime.strptime(dateInscription, "%Y-%m-%d")
    })
    print(f"Client {nom} {prenom} ajouté avec succès.")



"""
En t'aidant de la fonction précédente, complete la fonction insert_produit
"""
def insert_produit(db, nom, prix, categorie, stock):
    pass



def get_clients(db):
    clients = db.clients.find()
    for client in clients:
        print(client)


"""
Complète la fonction get_client pour trouver un client à partir de son id
"""
def get_client(db, id):
    pass

def get_product_price(db,id):
    return db.produits.find_one({"_id": id},{"prix": 1,"_id":0})

"""
Créé une fonction qui calcule le prix total d'une vente. Somme de quantite X prix_unitaire de chaque produit.
"""
def total_vente(produits):
    """Modèle de produits
    produits = [
        {
            produit_id,
            quantite,
            prix_unitaire
        },...
    ]
    """
    pass



"""
Insère une vente avec plusieurs produits
"""
def insert_vente(db, clientId, produits, dateVente):
    db.ventes.insert_one({
        "clientId": clientId,
        "produits": produits,
        "dateVente": datetime.strptime(dateVente, "%Y-%m-%d"),
        "total_vente":total_vente(produits)
    })
    print(f"Vente ajoutée pour le client {clientId}.")






"""
Recherche un client à l'aide de son email
"""
def rechercher_client_par_email(db, email):
    client = db.clients.find_one({"email": email})
    if client:
        print(client)
    else:
        print(f"Aucun client trouvé avec l'email {email}.")



"""
Affiche les produits dont le prix est supérieur à 50 €
"""
def afficher_produits_prix_superieur(db, prix):
    pass



"""
Trie les produits par prix croissant
"""
def trier_produits_par_prix(db):
    produits = db.produits.find().sort("prix", 1)  # 1 pour croissant, -1 pour décroissant
    for produit in produits:
        print(produit)



"""
Modifier le prix d'un produit
"""
def modifier_prix_produit(db, produit_nom, nouveau_prix):
    db.produits.update_one(
        {"nom": produit_nom},
        {"$set": {"prix": nouveau_prix}}
    )
    print(f"Le prix du produit {produit_nom} a été modifié à {nouveau_prix}.")



"""
Ajouter un champ fidélité à un client
"""
def ajouter_fidelite_client(db, email, fidelite):
    db.clients.update_one(
        {"email": email},
        {"$set": {"fidelite": fidelite}}  # Ajoute le champ fidélité au client
    )
    print(f"Le client avec l'email {email} a reçu le statut fidélité {fidelite}.")



"""
Incrémenter le stock d'un produit
"""
def incrementer_stock_produit(db, produit_nom, quantite):
    db.produits.update_one(
        {"nom": produit_nom},
        {"$inc": {"stock": quantite}}  # Incrémenter le stock
    )
    print(f"Le stock du produit {produit_nom} a été incrémenté de {quantite}.")



"""

"""
# Supprimer un client par email
def supprimer_client(db, email):
    db.clients.delete_one({"email": email})
    print(f"Le client avec l'email {email} a été supprimé.")



"""

"""
# Supprimer toutes les ventes d'un client
def supprimer_ventes_client(db, clientId):
    db.ventes.delete_many({"clientId": clientId})
    print(f"Toutes les ventes du client {clientId} ont été supprimées.")



"""

"""
# Rechercher un produit par catégorie
def rechercher_produit_par_categorie(db, categorie):
    produits = db.produits.find({"categorie": categorie})
    for produit in produits:
        print(produit)



"""

"""
# Rechercher les ventes réalisées sur une période donnée
def rechercher_ventes_par_periode(db, date_debut, date_fin):
    ventes = db.ventes.find({
        "dateVente": {"$gte": datetime.strptime(date_debut, "%Y-%m-%d"), "$lte": datetime.strptime(date_fin, "%Y-%m-%d")}
    })
    for vente in ventes:
        print(vente)



"""

"""
# Utiliser les opérateurs $gt et $lt pour rechercher des produits par prix
def rechercher_produits_par_prix(db, min_prix, max_prix):
    produits = db.produits.find({"prix": {"$gt": min_prix, "$lt": max_prix}})
    for produit in produits:
        print(produit)



"""

"""
# Calculer le chiffre d'affaires total du magasin
def calculer_chiffre_affaires(db):
    result = db.ventes.aggregate([
        {"$unwind": "$produits"},
        {"$group": {
            "_id": None,
            "chiffreAffaires": {"$sum": {"$multiply": ["$produits.prix", "$produits.quantite"]}}
        }}
    ])
    for r in result:
        print(f"Chiffre d'affaires total : {r['chiffreAffaires']}")



"""

"""
# Trouver le produit le plus vendu
def produit_le_plus_vendu(db):
    result = db.ventes.aggregate([
        {"$unwind": "$produits"},
        {"$group": {
            "_id": "$produits.produitId",
            "totalVendu": {"$sum": "$produits.quantite"}
        }},
        {"$sort": {"totalVendu": -1}},
        {"$limit": 1}
    ])
    for r in result:
        print(f"Produit le plus vendu : {r}")

# Exécution du script
if __name__ == "__main__":
    # Connexion à MongoDB
    client = connect_mongo()
    db = client["magasin"]
    print(get_product_price(db,ObjectId('69416c996ac222fe513f118c')))
    # Exemple d'insertion d'un client
    #insert_client(db, "Dupont", "Jean", "jean.dupont@mail.com", "2025-12-18")

    # Exemple de recherche de produit par prix
    #afficher_produits_prix_superieur(db, 50)

    # Exemple de calcul du chiffre d'affaires
    #calculer_chiffre_affaires(db)
