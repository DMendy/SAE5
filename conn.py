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


def get_clients(db):
    clients = db.clients.find()
    for client in clients:
        print(client)
"""
En reprenant la fonction get_clients, complète les deux fonctions suivantes.
"""
def get_produits(db):
    pass

def get_ventes(db):
    pass

"""
A l'aide de la fonction insert_client, insère une ligne client dans la base de donnée
"""
def insert_client(db, nom, prenom, email):
    ajd = str(datetime.now())
    db.clients.insert_one({
        "nom": nom,
        "prenom": prenom,
        "email": email,
        "dateInscription": datetime.strptime(ajd, "%Y-%m-%d")
    })
    print(f"Client {nom} {prenom} ajouté avec succès.")

"""
En t'aidant de la fonction précédente, complete la fonction insert_produit
"""
def insert_produit(db, nom, prix, categorie, stock):
    pass



"""
Complète la fonction get_client pour trouver un client à partir de son id
"""
def get_client(db, id):
    return db.clients.find_one({"_id": id})

"""
Recherche un client à l'aide de son email
"""
def get_client_by_email(db, email):
    pass


"""
Complète la fonction get_product_price pour qu'elle retrouve le prix d'un produit grâce à son id
"""
def get_product_price(db,id):
    pass


produits= [
      {
        "produit_id": ObjectId('6942b26b9a4ec022e53f1190'),
        "quantite": 2,
        "prix_unitaire": 15
      },
      {
        "produit_id": ObjectId('69416ec66ac222fe513f118f'),
        "quantite": 1,
        "prix_unitaire": 20
      },
      {
        "produit_id": ObjectId('69416e496ac222fe513f118d'),
        "quantite": 3,
        "prix_unitaire": 10.99
      }
    ]

"""
Créé une fonction qui calcule le prix total d'une vente. Somme de quantite X prix_unitaire de chaque produit.
"""
def total_vente(produits):
    pass


"""
Affiche les noms de produits dont le prix est supérieur à un prix donné
"""
def afficher_produits_prix_superieur(db, prix):
    pass



"""
Modifier le prix d'un produit
"""
def modifier_prix_produit(db,id_produit, nouveau_prix):
    db.produits.update_one(
        {"_id": id_produit},
        {"$set": {"prix": nouveau_prix}}
    )
    print(f"Le prix du produit {id_produit} a été modifié à {nouveau_prix}.")


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
    get_clients(db)
    #print(get_product_price(db,ObjectId('69416c996ac222fe513f118c')))
    # Exemple d'insertion d'un client
    #insert_client(db, "Dupont", "Jean", "jean.dupont@mail.com", "2025-12-18")

    # Exemple de recherche de produit par prix
    #afficher_produits_prix_superieur(db, 50)

    # Exemple de calcul du chiffre d'affaires
    #calculer_chiffre_affaires(db)
