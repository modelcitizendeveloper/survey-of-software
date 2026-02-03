#!/bin/bash
# Demo script for pantry search and recipe viewing

echo "=========================================="
echo "Recipe Embeddings - Pantry Search Demo"
echo "=========================================="
echo ""
echo "1. Search for recipes with your pantry ingredients:"
echo "   ./recipe-emb.sh pantry --file test_pantry.txt --top 5"
echo ""
echo "2. View a specific recipe by ID:"
echo "   ./recipe-emb.sh show 7642"
echo ""
echo "3. Interactive mode (select recipes to view):"
echo "   ./recipe-emb.sh pantry --file test_pantry.txt --interactive"
echo ""
echo "=========================================="
echo "Running example pantry search..."
echo "=========================================="
echo ""

./recipe-emb.sh pantry --file test_pantry.txt --top 3 --max-recipes 50000

echo ""
echo "=========================================="
echo "To view full recipe, use: ./recipe-emb.sh show <ID>"
echo "Or run with --interactive flag to select interactively"
echo "=========================================="
