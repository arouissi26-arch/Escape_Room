#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Motor de IA para generar tarjetas de estudio
Procesamiento de lenguaje natural en español
"""

import re
from collections import Counter
from typing import List, Dict, Tuple

class StudyAI:
    """
    Motor de Inteligencia Artificial para generar tarjetas de estudio
    """

    def __init__(self):
        # Palabras comunes a ignorar (stopwords en español)
        self.stopwords = {
            'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
            'de', 'del', 'al', 'a', 'ante', 'bajo', 'con', 'contra',
            'desde', 'en', 'entre', 'hacia', 'hasta', 'para', 'por',
            'según', 'sin', 'sobre', 'tras', 'y', 'o', 'u', 'e',
            'que', 'como', 'cuando', 'donde', 'cual', 'cuales',
            'este', 'esta', 'estos', 'estas', 'ese', 'esa', 'esos', 'esas',
            'aquel', 'aquella', 'aquellos', 'aquellas', 'su', 'sus',
            'mi', 'mis', 'tu', 'tus', 'nuestro', 'nuestra', 'vuestro',
            'se', 'si', 'no', 'ni', 'también', 'más', 'muy', 'son',
            'está', 'están', 'fue', 'fueron', 'han', 'ser', 'estar', 'hay'
        }

        # Verbos indicadores de definición
        self.definition_verbs = [
            'es', 'son', 'fue', 'fueron', 'será', 'serán',
            'significa', 'significan', 'define', 'definen',
            'consiste', 'consisten', 'representa', 'representan',
            'constituye', 'constituyen', 'forma', 'forman',
            'contiene', 'contienen', 'incluye', 'incluyen',
            'comprende', 'comprenden', 'denomina', 'denominan'
        ]

        # Verbos de acción
        self.action_verbs = [
            'produce', 'producen', 'realiza', 'realizan',
            'ejecuta', 'ejecutan', 'lleva', 'llevan',
            'efectúa', 'efectúan', 'cumple', 'cumplen',
            'desempeña', 'desempeñan', 'hace', 'hacen'
        ]

    def generate_flashcards(self, text: str) -> List[Dict]:
        """
        Generar tarjetas de estudio a partir del texto
        """
        sentences = self._split_sentences(text)
        flashcards = []

        for sentence in sentences:
            if len(sentence.strip()) < 20:
                continue

            # Generar diferentes tipos de preguntas
            cards = self._create_questions(sentence)
            flashcards.extend(cards)

        return flashcards

    def _split_sentences(self, text: str) -> List[str]:
        """
        Dividir texto en oraciones
        """
        # Limpiar el texto
        text = re.sub(r'\n+', '. ', text)
        text = re.sub(r'\s+', ' ', text)

        # Dividir por puntos, pero mantener puntos decimales
        sentences = re.split(r'(?<!\d)\.(?!\d)(?=\s|$)', text)
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences

    def _create_questions(self, sentence: str) -> List[Dict]:
        """
        Crear preguntas a partir de una oración
        """
        cards = []

        # Tipo 1: Preguntas de definición (¿Qué es...?)
        def_card = self._create_definition_question(sentence)
        if def_card:
            cards.append(def_card)

        # Tipo 2: Preguntas de completar espacios
        fill_card = self._create_fill_blank_question(sentence)
        if fill_card:
            cards.append(fill_card)

        # Tipo 3: Preguntas sobre características
        char_card = self._create_characteristic_question(sentence)
        if char_card:
            cards.append(char_card)

        # Tipo 4: Preguntas causales
        causal_card = self._create_causal_question(sentence)
        if causal_card:
            cards.append(causal_card)

        return cards

    def _create_definition_question(self, sentence: str) -> Dict:
        """
        Crear pregunta de definición
        Patrón: "X es Y" -> "¿Qué es X?"
        """
        patterns = [
            r'^(.+?)\s+(es|son|fue|fueron)\s+(.+?)\.?$',
            r'^(.+?)\s+se\s+(define|conoce|denomina)\s+como\s+(.+?)\.?$',
            r'^(.+?)\s+(significa|representa|constituye)\s+(.+?)\.?$'
        ]

        for pattern in patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                subject = match.group(1).strip()
                verb = match.group(2).strip()
                definition = match.group(3).strip()

                # Validar longitud
                if len(subject.split()) <= 7 and len(definition) > 10:
                    return {
                        'type': 'definición',
                        'question': f"¿Qué {verb} {subject.lower()}?",
                        'answer': definition.capitalize(),
                        'difficulty': 'fácil'
                    }

        return None

    def _create_fill_blank_question(self, sentence: str) -> Dict:
        """
        Crear pregunta de completar espacios
        """
        keywords = self._extract_keywords(sentence)

        if not keywords:
            return None

        # Seleccionar palabra clave más relevante
        keyword = keywords[0]

        # Reemplazar por espacio en blanco
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        question = pattern.sub('______', sentence, count=1)

        if question != sentence:
            return {
                'type': 'completar',
                'question': f"Completa la frase: {question}",
                'answer': keyword,
                'difficulty': 'medio'
            }

        return None

    def _create_characteristic_question(self, sentence: str) -> Dict:
        """
        Crear pregunta sobre características
        Patrón: "X tiene/contiene/posee Y"
        """
        pattern = r'^(.+?)\s+(tiene|tienen|contiene|contienen|posee|poseen|presenta|presentan)\s+(.+?)\.?$'
        match = re.search(pattern, sentence, re.IGNORECASE)

        if match:
            subject = match.group(1).strip()
            verb = match.group(2).strip()
            characteristic = match.group(3).strip()

            if len(subject.split()) <= 6:
                return {
                    'type': 'característica',
                    'question': f"¿Qué {verb} {subject.lower()}?",
                    'answer': characteristic.capitalize(),
                    'difficulty': 'medio'
                }

        return None

    def _create_causal_question(self, sentence: str) -> Dict:
        """
        Crear pregunta causal
        Patrón: "X porque Y" -> "¿Por qué X?"
        """
        pattern = r'^(.+?)\s+porque\s+(.+?)\.?$'
        match = re.search(pattern, sentence, re.IGNORECASE)

        if match:
            effect = match.group(1).strip()
            cause = match.group(2).strip()

            return {
                'type': 'causal',
                'question': f"¿Por qué {effect.lower()}?",
                'answer': f"Porque {cause}",
                'difficulty': 'difícil'
            }

        return None

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extraer palabras clave del texto
        """
        # Convertir a minúsculas y eliminar puntuación
        words = re.findall(r'\b[a-záéíóúñü]+\b', text.lower())

        # Filtrar stopwords y palabras cortas
        keywords = [
            word for word in words
            if word not in self.stopwords
            and word not in self.definition_verbs
            and len(word) > 4
        ]

        # Contar frecuencias
        word_freq = Counter(keywords)

        # Retornar las más frecuentes
        return [word for word, _ in word_freq.most_common(5)]

    def analyze_text(self, text: str) -> Dict:
        """
        Analizar texto y extraer información relevante
        """
        sentences = self._split_sentences(text)
        all_keywords = []

        for sentence in sentences:
            keywords = self._extract_keywords(sentence)
            all_keywords.extend(keywords)

        # Conceptos principales
        concept_freq = Counter(all_keywords)
        main_concepts = [word for word, _ in concept_freq.most_common(10)]

        return {
            'sentence_count': len(sentences),
            'word_count': len(text.split()),
            'main_concepts': main_concepts,
            'complexity': self._calculate_complexity(text)
        }

    def _calculate_complexity(self, text: str) -> str:
        """
        Calcular complejidad del texto
        """
        words = text.split()
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0

        if avg_word_length < 5:
            return 'baja'
        elif avg_word_length < 7:
            return 'media'
        else:
            return 'alta'

# Prueba del motor
if __name__ == '__main__':
    ai = StudyAI()

    test_text = """
    La fotosíntesis es el proceso por el cual las plantas convierten la luz solar en energía química.
    Las mitocondrias son las centrales energéticas de la célula porque producen ATP.
    El ADN contiene la información genética de todos los seres vivos.
    """

    print("🧠 Probando motor de IA...")
    flashcards = ai.generate_flashcards(test_text)

    print(f"\n✅ Generadas {len(flashcards)} tarjetas:\n")
    for i, card in enumerate(flashcards, 1):
        print(f"{i}. [{card['type']}] {card['question']}")
        print(f"   → {card['answer']}\n")
