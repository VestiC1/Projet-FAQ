// Composant Chat : gestion des questions/réponses en streaming
'use client';

import { useState, useRef, useEffect } from 'react';
import { Input, Button } from '@heroui/react';
import ReactMarkdown from 'react-markdown';

export default function Chat() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Ref pour auto-scroll vers le bas pendant le streaming
  const responseRef = useRef(null);

  // Auto-scroll pendant le streaming
  useEffect(() => {
    if (responseRef.current) {
      responseRef.current.scrollTop = responseRef.current.scrollHeight;
    }
  }, [response]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsLoading(true);
    setResponse(''); // Reset la réponse précédente

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/answer/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        throw new Error(`Erreur HTTP: ${res.status}`);
      }

      // Lecture du stream token par token
      const reader = res.body.getReader();
      const decoder = new TextDecoder('utf-8');

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        setResponse((prev) => prev + chunk);
        await new Promise((r) => setTimeout(r, 75));
      }
    } catch (error) {
      console.error("Erreur lors de l'appel API:", error);
      setResponse('Erreur lors de la récupération de la réponse.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Carte blanche pour le formulaire */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
        <form onSubmit={handleSubmit} className="space-y-4">
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
              input: 'bg-gray-50',
              inputWrapper: 'border-gray-300 hover:border-gray-400',
            }}
          />

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

      {/* Affichage de la réponse en markdown */}
      {response && (
        <div
          ref={responseRef}
          className="bg-white rounded-lg shadow-md p-6 border border-gray-200 max-h-[60vh] overflow-y-auto"
        >
          <h3 className="text-lg font-semibold text-gray-800 mb-3">
            Réponse :
          </h3>
          <div className="prose prose-gray max-w-none text-gray-700">
            <ReactMarkdown>{response}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
}