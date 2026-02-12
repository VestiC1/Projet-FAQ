// Composant Chat : gestion des questions/réponses
'use client'; // Obligatoire car on utilise des hooks (useState)

import { useState } from 'react';
import { Input, Button } from '@heroui/react';

export default function Chat() {
  // État pour stocker la question de l'utilisateur
  const [question, setQuestion] = useState('');
  
  // État pour stocker la réponse de l'API
  const [response, setResponse] = useState('');
  
  // État pour gérer le chargement (afficher un loader pendant l'appel API)
  const [isLoading, setIsLoading] = useState(false);

  // Fonction appelée quand l'utilisateur clique sur "Envoyer"
  const handleSubmit = async (e) => {
    e.preventDefault(); // Empêche le rechargement de la page
    
    // Validation : ne rien faire si le champ est vide
    if (!question.trim()) return;
    
    setIsLoading(true); // Active le loader
    
    try {
      // Appel à l'API FastAPI (à adapter avec votre URL)
      const res = await fetch('/api/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }),
      });
      
      const data = await res.json();
      
      // Stocke la réponse
      setResponse(data.answer || 'Aucune réponse trouvée.');
      
    } catch (error) {
      console.error('Erreur lors de l\'appel API:', error);
      setResponse('Erreur lors de la récupération de la réponse.');
    } finally {
      setIsLoading(false); // Désactive le loader
    }
  };

  return (
    <div className="space-y-6">
      {/* space-y-6 : espace vertical entre les éléments */}
      
      {/* Carte blanche pour le formulaire */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <form onSubmit={handleSubmit} className="space-y-4">
          
          {/* Champ de saisie */}
          <Input
            type="text"
            label="Posez votre question"
            placeholder="Ex: Comment réinitialiser mon mot de passe ?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            size="lg"
            variant="bordered"
            className="w-full"
            disabled={isLoading}
            classNames={{
              input: "bg-gray-50",
              inputWrapper: "border-gray-300 hover:border-gray-400"
            }}
          />
          
          {/* Bouton d'envoi */}
          <Button
            type="submit"
            color="primary"
            size="lg"
            className="w-full font-semibold"
            isLoading={isLoading}
            disabled={isLoading || !question.trim()}
          >
            {isLoading ? 'Envoi en cours...' : 'Envoyer'}
          </Button>
        </form>
      </div>
      
      {/* Affichage de la réponse */}
      {response && (
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Réponse :
          </h3>
          <p className="text-gray-700 leading-relaxed">
            {response}
          </p>
        </div>
      )}
    </div>
  );
}