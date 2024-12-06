# VocaLlama

Ce projet implémente un agent **Speech-to-Speech** multi-modulaire, conçu pour effectuer une conversation vocale simple tout en permettant une grande flexibilité pour adapter ses modules selon vos besoins.

## Fonctionnalités principales

1. **Détection de l'activité vocale :**
   - Utilise un détecteur de volume audio pour vérifier si une activité est présente avant de lancer le traitement.

2. **Transcription audio :**
   - Transforme l'audio en texte grâce à l'API **Whisper**.

3. **Génération de texte :**
   - Le texte est envoyé à **Llama 3** via l'API **Ollama**, qui génère une réponse.

4. **Synthèse vocale :**
   - Convertit le texte généré en audio grâce à **gTTS (Google Text-to-Speech)**.

5. **Hotword detection :**
   - Intègre **Porcupine** pour activer le système via des mots-clés prédéfinis.

6. **Modularité :**
   - Architecture modulaire qui permet d'ajouter, modifier ou supprimer des composants pour répondre à différents besoins.

---

## Installation et configuration

### Prérequis

- **Python 3.9 ou supérieur**
- Compte Porcupine (nécessaire pour le système de hotword)
- Installation d’Ollama sur votre machine

### Étapes d'installation

1. Clonez ce dépôt :  
   ```bash
   git clone https://github.com/Sushiman31/VocaLlama.git
   cd VocaLlama
   ```

2. Installez les dépendances Python :  
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez **Ollama** :
   - Téléchargez Ollama depuis leur site officiel.
   - Configurez l’API pour permettre l’accès depuis votre machine.

4. Configurez **Porcupine** :
   - Créez un compte sur le site de **Porcupine**.
   - Téléchargez vos mots-clés personnalisés et configurez leur chemin dans le projet.

---

## Utilisation

1. Démarrez l'agent :
   ```bash
   python main.py
   ```

2. Parlez à l'agent en utilisant le mot-clé configuré. L'agent détectera l'activité, générera une réponse, et vous répondra sous forme vocale.

---

## Limites actuelles

- **Latence :** Le système présente encore une latence significative due à l’utilisation d’APIs multiples. Une optimisation des processus est nécessaire.
- **Dépendances externes :** Nécessite plusieurs APIs et comptes pour fonctionner (Whisper, Ollama, Porcupine, gTTS).

---

## Points forts

- **Flexibilité :** Grâce à sa modularité, vous pouvez facilement personnaliser l'agent en ajoutant de nouveaux modèles ou en remplaçant les modules existants.
- **Facilité d'utilisation :** L'intégration des modules est simple et rapide.

---

## Améliorations futures

- Optimisation de la latence.
- Intégration de modules supplémentaires (par exemple, reconnaissance des émotions ou amélioration de la qualité audio).

---
