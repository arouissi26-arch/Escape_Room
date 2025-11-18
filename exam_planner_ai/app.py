#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Planificador de Exámenes con IA
Servidor Flask para generar tarjetas de estudio automáticamente
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime
from ai_engine import StudyAI

app = Flask(__name__)
CORS(app)

# Inicializar el motor de IA
ai_engine = StudyAI()

# Directorio para guardar datos
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_flashcards():
    """
    Generar tarjetas de estudio a partir del contenido
    """
    try:
        data = request.get_json()
        content = data.get('content', '')

        if not content:
            return jsonify({'error': 'No se proporcionó contenido'}), 400

        # Generar tarjetas con IA
        flashcards = ai_engine.generate_flashcards(content)

        return jsonify({
            'success': True,
            'flashcards': flashcards,
            'count': len(flashcards)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    Analizar texto y extraer conceptos principales
    """
    try:
        data = request.get_json()
        content = data.get('content', '')

        if not content:
            return jsonify({'error': 'No se proporcionó contenido'}), 400

        # Analizar con IA
        concepts = ai_engine.analyze_text(content)

        return jsonify({
            'success': True,
            'concepts': concepts
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save', methods=['POST'])
def save_data():
    """
    Guardar datos del usuario
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default')

        filename = os.path.join(DATA_DIR, f'{user_id}.json')

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return jsonify({'success': True})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/load/<user_id>', methods=['GET'])
def load_data(user_id):
    """
    Cargar datos del usuario
    """
    try:
        filename = os.path.join(DATA_DIR, f'{user_id}.json')

        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify({'flashcards': [], 'exams': []})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Verificar estado del servidor"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'ai_engine': 'running'
    })

if __name__ == '__main__':
    print("🚀 Servidor iniciado en http://localhost:5000")
    print("📚 Motor de IA cargado y listo")
    print("✨ Presiona Ctrl+C para detener")
    app.run(debug=True, host='0.0.0.0', port=5000)
