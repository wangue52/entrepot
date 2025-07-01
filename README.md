# README.md
# Product Price Comparison API

API REST pour comparer les prix de produits entre différents points de vente.

## Fonctionnalités

- **Gestion des produits** : CRUD complet avec recherche avancée
- **Gestion des points de vente** : CRUD avec filtres par ville et type
- **Gestion des prix** : Association produit-point de vente-date
- **Statistiques** : Analyses et métriques sur les données
- **Documentation automatique** : Swagger UI et ReDoc
- **Validation des données** : Validation Pydantic
- **Logging** : Système de logs complet
- **Tests** : Tests unitaires avec pytest

## Installation

1. Cloner le repository
```bash
git clone <repository-url>
cd product-price-api
```

2. Installer les dépendances
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer le fichier .env selon vos besoins
```

4. Lancer l'application
```bash
uvicorn main:app --reload
```

## Utilisation

### Documentation API
- Swagger UI : http://localhost:8000/docs
- ReDoc : http://localhost:8000/redoc

### Endpoints principaux

#### Produits
- `POST /products/` - Créer un produit
- `GET /products/` - Lister les produits
- `GET /products/{id}` - Détail d'un produit
- `PUT /products/{id}` - Modifier un produit
- `DELETE /products/{id}` - Supprimer un produit

#### Points de vente
- `POST /sale-points/` - Créer un point de vente
- `GET /sale-points/` - Lister les points de vente
- `GET /sale-points/{id}` - Détail d'un point de vente

#### Prix
- `POST /prices/` - Créer un prix
- `GET /prices/` - Lister les prix
- `GET /prices/{product_id}/{sale_point_id}/{date_id}` - Détail d'un prix

### Exemples d'utilisation

#### Créer un produit
```bash
curl -X POST "http://localhost:8000/products/" \
     -H "Content-Type: application/json" \
     -d '{
       "id": "iphone-15",
       "title": "iPhone 15",
       "link": "https://example.com/iphone-15"
     }'
```

#### Rechercher des produits
```bash
curl -X POST "http://localhost:8000/products/search" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "iPhone",
       "city": "Paris"
     }'
```

## Tests

```bash
pytest test_main.py -v
```

## Déploiement avec Docker

```bash
docker-compose up -d
```

## Structure du projet

```
.
├── main.py              # Application FastAPI principale
├── models.py            # Modèles SQLAlchemy
├── schemas.py           # Modèles Pydantic
├── crud.py              # Opérations CRUD
├── database.py          # Configuration base de données
├── config.py            # Configuration
├── exceptions.py        # Exceptions personnalisées
├── middleware.py        # Middlewares
├── utils.py             # Utilitaires
├── validators.py        # Validateurs
├── logging_config.py    # Configuration logging
├── test_main.py         # Tests
├── requirements.txt     # Dépendances
├── docker-compose.yml   # Configuration Docker
├── Dockerfile          # Image Docker
└── README.md           # Documentation
```

## Configuration

L'application utilise des variables d'environnement pour la configuration :

- `DATABASE_URL` : URL de connexion à la base de données
- `SECRET_KEY` : Clé secrète pour la sécurité
- `API_V1_STR` : Préfixe des routes API

## Contribution

1. Fork le projet
2. Créer une branche feature
3. Commit les changements
4. Push vers la branche
5. Créer une Pull Request

## License

MIT License
