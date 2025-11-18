#!/bin/bash
# Quick launcher for Latin Keyboard Trainer

echo "======================================================================="
echo "LATIN KEYBOARD TRAINER - Interactive Mode"
echo "======================================================================="
echo ""
echo "Activating virtual environment..."

cd /home/ivanadamin/spawn-solutions/research/1.140-classical-language-libraries/02-implementations
source ../.venv/bin/activate

echo "Starting trainer..."
echo ""

python latin_trainer_fast.py
