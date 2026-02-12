// Composant FAQList : récupère et affiche la liste des FAQ depuis l'API
'use client'; // Obligatoire car on utilise des hooks

import { useState, useEffect } from 'react';
import { Card, CardBody, Spinner } from '@heroui/react';

export default function FAQList() {
  // État pour stocker les questions/réponses
  const [faqData, setFaqData] = useState([]);
  
  // État pour gérer le chargement
  const [isLoading, setIsLoading] = useState(true);
  
  // État pour gérer les erreurs
  const [error, setError] = useState(null);

  // useEffect : s'exécute au chargement du composant
  useEffect(() => {
    // Fonction pour récupérer les données de l'API
    const fetchFAQ = async () => {
      try {
        // Appel à l'API FastAPI (à adapter avec votre URL)
        const res = await fetch('/api/FAQ');
        
        if (!res.ok) {
          throw new Error('Erreur lors de la récupération des données');
        }
        
        const data = await res.json();
        
        // Stocke les données (selon votre format API : data.faq ou data directement)
        setFaqData(data.faq || data);
        
      } catch (err) {
        console.error('Erreur API:', err);
        setError(err.message);
      } finally {
        setIsLoading(false); // Arrête le loader
      }
    };

    fetchFAQ(); // Lance la récupération au chargement
  }, []); // [] = s'exécute une seule fois au montage du composant

  // Affichage pendant le chargement
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-20">
        <Spinner size="lg" label="Chargement de la FAQ..." />
      </div>
    );
  }

  // Affichage en cas d'erreur
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p className="text-red-600 font-semibold">Erreur : {error}</p>
        <p className="text-red-500 text-sm mt-2">
          Vérifiez que votre API est bien lancée sur http://localhost:8000
        </p>
      </div>
    );
  }

  // Affichage si aucune FAQ
  if (faqData.length === 0) {
    return (
      <div className="text-center py-20 text-gray-500">
        Aucune question disponible pour le moment
      </div>
    );
  }

  // Affichage de la liste des FAQ
  return (
    <div className="space-y-4">
      {/* space-y-4 : espace entre chaque carte */}
      
      {faqData.map((item, index) => (
        <Card 
          key={index} 
          className="bg-white shadow-md hover:shadow-lg transition-shadow"
        >
          {/* hover:shadow-lg : ombre plus prononcée au survol */}
          {/* transition-shadow : animation fluide */}
          
          <CardBody className="p-6">
            {/* Question */}
            <h3 className="text-lg font-semibold text-gray-800 mb-3">
              {item.question}
            </h3>
            
            {/* Séparateur */}
            <div className="border-b border-gray-200 mb-3"></div>
            
            {/* Réponse */}
            <p className="text-gray-700 leading-relaxed">
              {item.answer}
            </p>
          </CardBody>
        </Card>
      ))}
    </div>
  );
}