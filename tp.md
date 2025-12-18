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
TP Client–Serveur MongoDB
Connexion à un serveur MongoDB distant hébergé sur Raspberry Pi
IP : 192.168.25.24
Port : 27017
Utilisateur : admin
Mot de passe : password
Base d'authentification : admin
"""

# Paramètres de connexion
rpi_ip = "192.168.25.24"
mongo_port = 27017
mongo_user = "admin"
mongo_password = "password"
auth_db = "admin"

mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{rpi_ip}:{mongo_port}/?authSource={auth_db}"

def connect_mongo():
    try:
        print("Connexion au serveur MongoDB distant...")
        client = MongoClient(mongo_uri)
        print("Connexion réussie")
        return client["magasin"]
    except Exception as e:
        print("Erreur de connexion :", e)
        sys.exit(1)

def show_tables(db):
    print("Collections disponibles :", db.list_collection_names())

def get_clients(db):
    for client in db.clients.find():
        print(client)

def get_produits(db):
    for produit in db.produits.find():
        print(produit)

def get_ventes(db):
    for vente in db.ventes.find():
        print(vente)

def insert_client(db, nom, prenom, email):
    db.clients.insert_one({
        "nom": nom,
        "prenom": prenom,
        "email": email,
        "dateInscription": datetime.now()
    })
    print("Client ajouté")

def insert_produit(db, nom, prix, categorie, stock):
    db.produits.insert_one({
        "nom": nom,
        "prix": prix,
        "categorie": categorie,
        "stock": stock
    })
    print("Produit ajouté")

def get_client_by_email(db, email):
    return db.clients.find_one({"email": email})

def get_product_price(db, id_produit):
    produit = db.produits.find_one({"_id": id_produit})
    return produit["prix"] if produit else None

def total_vente(db, id_vente):
    vente = db.ventes.find_one({"_id": id_vente})
    total = 0
    for p in vente["produits"]:
        total += p["quantite"] * p["prix"]
    return total

def afficher_produits_prix_superieur(db, prix):
    for produit in db.produits.find({"prix": {"$gt": prix}}):
        print(produit["nom"])

def modifier_prix_produit(db, id_produit, nouveau_prix):
    db.produits.update_one(
        {"_id": id_produit},
        {"$set": {"prix": nouveau_prix}}
    )
    print("Prix modifié")

def update_stock_apres_vente(db, id_vente):
    vente = db.ventes.find_one({"_id": id_vente})
    for p in vente["produits"]:
        db.produits.update_one(
            {"_id": p["produitId"]},
            {"$inc": {"stock": -p["quantite"]}}
        )

def supprimer_produits(db):
    db.produits.delete_many({"stock": {"$lte": 0}})
    print("Produits sans stock supprimés")

if __name__ == "__main__":
    db = connect_mongo()
    show_tables(db)
    get_clients(db)
