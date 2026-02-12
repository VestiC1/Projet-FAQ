// Page d'accueil : interface de chat pour poser des questions
import Chat from '@/components/Chat';

export default function HomePage() {
  return (
    <div className="container mx-auto px-4 py-8">
      {/* container : centrage avec largeur maximale */}
      {/* mx-auto : marge automatique gauche/droite pour centrer */}
      {/* px-4 : padding horizontal, py-8 : padding vertical */}
      
      <div className="max-w-3xl mx-auto">
        {/* max-w-3xl : largeur maximale de 768px pour une meilleure lisibilité */}
        
        {/* Titre de la page */}
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          ASSISTANT FAQ
        </h1>
        
        {/* Composant Chat qui gère les questions/réponses */}
        <Chat />
      </div>
    </div>
  );
}