# ==========================================
# 🍽️ Meal Recommender API - Makefile
# ==========================================
# Commandes standardisées pour le projet
# Usage: make <commande>

.PHONY: help install dev-install test test-cov lint format clean run run-api run-streamlit docker-build docker-up docker-down

# Couleurs pour le terminal
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
NC := \033[0m # No Color

# Commande par défaut
.DEFAULT_GOAL := help

## 📖 Affiche cette aide
help:
	@echo "$(GREEN)Meal Recommender API - Commandes disponibles:$(NC)"
	@echo ""
	@echo "$(BLUE)Installation:$(NC)"
	@echo "  make install      - Installe les dépendances de production"
	@echo "  make dev-install  - Installe les dépendances de développement"
	@echo ""
	@echo "$(BLUE)Développement:$(NC)"
	@echo "  make run          - Lance l'API et Streamlit (docker-compose)"
	@echo "  make run-api      - Lance l'API en local (uvicorn)"
	@echo "  make run-streamlit - Lance Streamlit en local"
	@echo ""
	@echo "$(BLUE)Tests & Qualité:$(NC)"
	@echo "  make test         - Lance les tests"
	@echo "  make test-cov     - Lance les tests avec couverture"
	@echo "  make lint         - Vérifie le code (ruff + mypy)"
	@echo "  make format       - Formate le code (ruff format)"
	@echo ""
	@echo "$(BLUE)Docker:$(NC)"
	@echo "  make docker-build - Build les images Docker"
	@echo "  make docker-up    - Démarre les containers"
	@echo "  make docker-down  - Arrête les containers"
	@echo ""
	@echo "$(BLUE)Maintenance:$(NC)"
	@echo "  make clean        - Nettoie les fichiers générés"
	@echo "  make setup-hooks  - Configure les pre-commit hooks"

## 🚀 Installation production
install:
	@echo "$(GREEN)📦 Installation des dépendances...$(NC)"
	pip install -e .

## 🔧 Installation développement
dev-install: install
	@echo "$(GREEN)🔧 Installation des dépendances de développement...$(NC)"
	pip install -e ".[dev]"
	@echo "$(GREEN)✅ Installation terminée!$(NC)"

## 🧪 Lance les tests
test:
	@echo "$(GREEN)🧪 Lancement des tests...$(NC)"
	pytest -v

## 📊 Lance les tests avec couverture
test-cov:
	@echo "$(GREEN)📊 Tests avec couverture...$(NC)"
	pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)✅ Rapport HTML généré dans htmlcov/$(NC)"

## 🔍 Linting (vérification qualité)
lint:
	@echo "$(GREEN)🔍 Vérification du code avec ruff...$(NC)"
	ruff check src tests
	@echo "$(GREEN)🔍 Vérification des types avec mypy...$(NC)"
	mypy src

## 🎨 Formatage du code
format:
	@echo "$(GREEN)🎨 Formatage avec ruff...$(NC)"
	ruff format src tests
	@echo "$(GREEN)🎨 Tri des imports...$(NC)"
	ruff check --select I --fix src tests

## 🐛 Lance l'API en local (mode dev)
run-api:
	@echo "$(GREEN)🚀 Démarrage API sur http://localhost:8000$(NC)"
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

## 🎨 Lance Streamlit en local
run-streamlit:
	@echo "$(GREEN)🎨 Démarrage Streamlit sur http://localhost:8501$(NC)"
	streamlit run streamlit_app/main.py

## 🐳 Lance avec Docker Compose
run:
	@echo "$(GREEN)🐳 Démarrage avec Docker Compose...$(NC)"
	docker-compose up --build

## 🐳 Build les images Docker
docker-build:
	@echo "$(GREEN)🐳 Build des images Docker...$(NC)"
	docker-compose build

## 🐳 Démarre les containers (détaché)
docker-up:
	@echo "$(GREEN)🐳 Démarrage des containers...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ API: http://localhost:8000$(NC)"
	@echo "$(GREEN)✅ Streamlit: http://localhost:8501$(NC)"

## 🐳 Arrête les containers
docker-down:
	@echo "$(GREEN)🛑 Arrêt des containers...$(NC)"
	docker-compose down

## 🧹 Nettoie les fichiers générés
clean:
	@echo "$(YELLOW)🧹 Nettoyage...$(NC)"
	rm -rf __pycache__ .pytest_cache htmlcov .mypy_cache
	rm -rf src/**/__pycache__ tests/**/__pycache__
	rm -rf build dist *.egg-info
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "$(GREEN)✅ Nettoyage terminé!$(NC)"

## 🔄 Configure les pre-commit hooks
setup-hooks:
	@echo "$(GREEN)🔄 Configuration des hooks...$(NC)"
	pre-commit install
	@echo "$(GREEN)✅ Hooks configurés!$(NC)"

## 🧪 Lance les tests de performance
bench:
	@echo "$(GREEN)🏃 Tests de performance...$(NC)"
	pytest tests/ -m benchmark --benchmark-only
