#!/bin/bash

API_URL="http://localhost:5000"

# /meals/import_csv
echo "📦 Importing meals from CSV..."
curl -s -X POST "$API_URL/meals/import_csv" \
  -H "Content-Type: application/json" \
  -d '{"file_path": "demo_meals.csv"}' | jq

# /meals
echo -e "\n📋 Listing all meals..."
curl -s "$API_URL/meals" | jq

# /meals/1
echo -e "\n🔍 Getting meal by ID (1)..."
curl -s "$API_URL/meals/1" | jq

# /meals ADD POST
echo -e "\n➕ Creating a new meal..."
curl -s -X POST "$API_URL/meals" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tuna Sandwich",
    "description": "Simple tuna sandwich with mayo",
    "ingredients": ["bread", "tuna", "mayonnaise"]
  }' | jq

echo -e "\n📋 Re-listing all meals after creation..."
curl -s "$API_URL/meals" | jq
