# SAE BUT 3 FA  
## TP Client–Serveur MongoDB

### INF3-FA – 2025-2026

**Auteurs :**  
AZIRGUI Younes  
DINANGA Alexis  
MENDY Doryan  
KOUNDI Maryam  

---

## 1. Objectif du TP

Ce TP a pour objectif de vérifier l’accessibilité d’un serveur MongoDB distant hébergé sur un Raspberry Pi depuis une machine cliente située sur le réseau du département informatique.

À travers ce TP, l’étudiant devra :
- Se connecter à un serveur MongoDB distant
- Manipuler des données via un script Python
- Vérifier les opérations CRUD (Create, Read, Update, Delete)
- Valider le bon fonctionnement d’une architecture client–serveur

---

## 2. Contexte client–serveur

- **Serveur MongoDB** : Raspberry Pi  
- **Adresse IP du serveur** : `192.168.25.24`  
- **Port MongoDB** : `27017`  
- **Base de données** : `magasin`  
- **Utilisateur MongoDB** : `admin`  
- **Mot de passe** : `password`  
- **Base d’authentification** : `admin`  

Le serveur est déjà configuré et fonctionnel.  
Le TP se concentre uniquement sur la partie **client**.

---

## 3. Principe du TP

Le TP repose sur un **script Python client** qui se connecte à MongoDB à distance à l’aide de la bibliothèque `pymongo`.  
Ce script permet :
- d’afficher les collections
- d’insérer des données
- de lire des données
- de modifier et supprimer des documents
- de simuler des ventes dans un magasin de vêtements

---

## 4. Script Python client MongoDB

Le script suivant est à exécuter **sur la machine cliente**.

```python
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
rpi_ip = "192.168.25.24"
mongo_port = 27017
mongo_user = "admin"
mongo_password = "password"
auth_db = "admin"

# URI de connexion MongoDB
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{rpi_ip}:{mongo_port}/?authSource={auth_db}"


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
    produits = db.produits.find()
    for produit in produits:
        print(produit)

def get_ventes(db):
    ventes = db.ventes.find()
    for vente in ventes:
        print(vente)

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
    db.produits.insert_one({
        "nom":nom,
        "prix":prix,
        "categorie":categorie,
        "stock":stock
    })
    print(f"Le produit {nom} a été ajouté avec succès.")




#Fonction qui permet de retrouver un client depuis son id
def get_client(db, id):
    return db.clients.find_one({"_id": id})


"""
Complète la fonction suivante pour qu'elle permette de trouver un client à l'aide de son email
"""
def get_client_by_email(db, email):
    return db.clients.find_one({"mail": email})


"""
Complète la fonction get_product_price pour qu'elle retrouve le prix d'un produit grâce à son id
"""
def get_product_price(db,id):
    return db.produits.find_one({"_id":id},{"_id":0,"prix":1})



"""
Créé une fonction qui calcule le prix total d'une vente sans utiliser l'attribut total_vente. Somme de quantite * prix_unitaire de chaque produit.
"""
def total_vente(db,id_vente):
    somme=0
    produits =  db.ventes.find_one({"_id":id_vente},{"_id":0,"produits":1})
    for produit in produits:
        somme+=produit.get("prix_unitaire")*produit.get("quantite")
    return somme


"""
Affiche les noms de produits dont le prix est supérieur à un prix donné
"""
def afficher_produits_prix_superieur(db, prix):
    produits = db.produits.find({ "prix": { "$gt": prix } })
    for produit in produits:
        print(produit)

#Fonction qui permet de modifier le nom d'un client
def modifier_nom_client(db,id_client,nouveau_nom):
    ancien_nom = db.clients.find_one({"_id":id_client},{"_id":0,"nom":1})
    db.clients.update_one(
        {"_id": id_client},
        {"$set": {"nom": nouveau_nom}}
    )
    print(f"Le nom du produit {id_client} a été changé de {ancien_nom} en {nouveau_nom}.")


"""
À partir de la fonction précédente, complète la fonction suivante pour modifier le prix d'un produit à partir de son id
"""
def modifier_prix_produit(db,id_produit, nouveau_prix):
    ancien_prix = get_product_price(db,id_produit)
    db.produits.update_one(
        {"_id":id_produit},
        {"$set":{"prix":nouveau_prix}}
    )
    print(f"Le prix du produit {id_produit} est passé de {ancien_prix}DH à {nouveau_prix}DH.")




#Incrémenter le stock d'un produit depuis son nom
def incrementer_stock_produit(db, produit_nom, quantite):
    db.produits.update_one(
        {"nom": produit_nom},
        {"$inc": {"stock": quantite}}  # Incrémenter le stock
    )
    print(f"Le stock du produit {produit_nom} a été incrémenté de {quantite}.")

"""En se basant sur la fonction précéddente, complète la fonction suivante pour qu'elle 
retire des stocks concernés les produits présents dans une vente donnée."""
def update_stock_apres_vente(db,id_vente):
    produits =  db.ventes.find_one({"_id":id_vente},{"_id":0,"produits":1})
    for produitVente in produits:
        db.produits.update_one(
            {"_id":produitVente.get("produit_id")},
            {"$inc": {"stock": -produitVente.get("quantite")}}
        )
        print(f'Le stock du produit {produitVente.get("produit_id")} a diminué de {produitVente.get("quantite")}')
        


# Supprime un client par mail
def supprimer_client_mail(db, email):
    db.clients.delete_one({"email": email})
    print(f"Le client avec l'email {email} a été supprimé.")


""" 
Supprimer tous les produits qui n'ont plus de stock
"""
def supprimer_produits(db):
    produits = db.produits.find({"stock":{"$lte":0}})
    for produit in produits:
        nom = produit.get("nom")
        db.produits.delete_one({"_id":produit.get("_id")})
        print(f"Le produit {nom} a été supprimé car nous n'avions plus de stock")

"""
Complète cette dernière fonction qui doit réaliser ces 3 étapes : 
    -Créer une vente
    -Mettre à jour le stock des produits vendus
    -Mettre à jour l'historique du client
"""
def vente_client(db,liste_produit,id_client):
    produits = []
    total_vente = 0
    for id,quantite in liste_produit:
        produit = db.produits.find_one({"_id":id})
        produits.append(
            {
                "produit_id":id,
                "quantite":quantite,
                "prix_unitaire":produit.get("prix")
            }
        )
        total_vente+=quantite*produit.get("prix")
    vente = db.ventes.insert_one({
        "id_client":id_client,
        "produits":produits,
        "date":datetime.now(),
        "total_vente" : total_vente
    })
    print(f"La vente a été ajouté avec succès.")

    update_stock_apres_vente(db,vente.inserted_id)
    
    db.clients.update_one(
        {"_id":id_client},
        {"$push":{"historique":vente.inserted_id}}
    )
