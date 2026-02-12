// Page FAQ : affiche la liste complète des questions/réponses
import FAQList from '@/components/FAQList';

export default function FAQPage() {
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-4xl mx-auto">
        {/* max-w-4xl : un peu plus large que la page d'accueil pour la liste */}
        
        {/* Titre de la page */}
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          FAQ Complète
        </h1>
        
        {/* Description */}
        <p className="text-center text-gray-600 mb-8">
          Retrouvez toutes les questions fréquemment posées et leurs réponses
        </p>
        
        {/* Composant qui affiche la liste des FAQ */}
        <FAQList />
      </div>
    </div>
  );
}