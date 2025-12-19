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
#mongo_uri2 = f"mongodb://admin:password@192.168.25.24:27017/?authSource=admin"


# Connexion à MongoDB
def connect_mongo():    
    try:
        print(f"Connexion à MongoDB sur {rpi_ip}:{mongo_port}...")
        client = MongoClient(mongo_uri)
        print("Connexion réussie à MongoDB!")
        return client['magasin']
    except Exception as e:
        print(f"Erreur de connexion à MongoDB : {e}")
        sys.exit(1)

#Fonction qui permet d'afficher toutes les collections de la database
def show_tables(db):
    return db.list_collection_names()

#Fonction qui permet d'afficher toutes les lignes de la collection clients
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

#Fonction qui permet d'ajouter un client à la base de données
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
En t'aidant des fonctions précédentes, complète la fonction insert_produit
"""
def insert_produit(db, nom, prix, categorie, stock):
    pass



#Fonction qui permet de retrouver un client depuis son id
def get_client(db, id):
    return db.clients.find_one({"_id": id})


"""
Complète la fonction suivante pour qu'elle permette de trouver un client à l'aide de son email
"""
def get_client_by_email(db, email):
    pass


"""
Complète la fonction get_product_price pour qu'elle retrouve le prix d'un produit grâce à son id
"""
def get_product_price(db,id):
    pass



"""
Créé une fonction qui calcule le prix total d'une vente sans utiliser l'attribut total_vente. Somme de quantite * prix_unitaire de chaque produit.
"""
def total_vente(db,id_vente):
    pass


"""
Affiche les noms de produits dont le prix est supérieur à un prix donné
"""
def afficher_produits_prix_superieur(db, prix):
    pass

#Fonction qui permet de modifier le nom d'un client
def modifier_nom_client(db,id_client,nouveau_nom):
    db.clients.update_one(
        {"_id": id_client},
        {"$set": {"nom": nouveau_nom}}
    )
    print(f"Le stock du produit {id_client} a été incrémenté de {nouveau_nom}.")


"""
À partir de la fonction précédente, complète la fonction suivante pour modifier le prix d'un produit à partir de son id
"""
def modifier_prix_produit(db,id_produit, nouveau_prix):
    pass



#Incrémenter le stock d'un produit
def incrementer_stock_produit(db, produit_nom, quantite):
    db.produits.update_one(
        {"nom": produit_nom},
        {"$inc": {"stock": quantite}}  # Incrémenter le stock
    )
    print(f"Le stock du produit {produit_nom} a été incrémenté de {quantite}.")

"""En se basant sur la fonction précéddente, complète la fonction suivante pour qu'elle 
retire des stocks concernés les produits présents dans une vente donnée."""
def update_stock_apres_vente(db,id_vente):
    pass

# Supprime un client par id
def supprimer_client(db, email):
    db.clients.delete_one({"email": email})
    print(f"Le client avec l'email {email} a été supprimé.")


""" 
Supprimer tous les produits qui n'ont plus de stock
"""
def supprimer_produits(db):
    pass


"""
Complète cette dernière fonction qui doit réaliser ces 3 étapes : 
    -Créer une vente
    -Mettre à jour le stock des produits vendus
    -Mettre à jour l'historique du client
"""
def vente_client(db,produits_ids,id_client):
    pass

#Permet de réinitialiser la db
def reset_magasin_from_admin(client):
    SOURCE_DB = "admin"
    TARGET_DB = "magasin"

    while True :
        confirm = input("Réinitialiser la base magasin ? (oui/non) : ").strip().lower()

        if confirm == "oui":
            break
        elif confirm == "non":
            print("Réinitialisation annulée")
            return
        else:
            print("Réponse invalide, merci de répondre par 'oui' ou par 'non'")

    try:
        client.drop_database(TARGET_DB)
    except Exception as e:
        print("Erreur lors de la suppression :", e)
        return
    print("Base 'magasin' supprimée.")

    source = client[SOURCE_DB]
    target = client[TARGET_DB]

    collections = ["clients", "produits", "ventes"]

    for col in collections:
        if col in source.list_collection_names():
            docs = list(source[col].find())
            if docs:
                target[col].insert_many(docs)
                print(f"Collection '{col}' copiée ({len(docs)} documents).")
            else:
                print(f"Collection '{col}' vide, rien à copier.")
        else:
            print(f"Collection '{col}' inexistante dans admin.")

    print("Base 'magasin' recréée depuis 'admin'.")