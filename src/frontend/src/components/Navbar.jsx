// Composant Navbar : barre de navigation fixe
import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="fixed top-0 left-0 right-0 bg-white shadow-md z-50">
      {/* z-50 : s'affiche au-dessus des autres éléments */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* max-w-7xl : largeur maximale responsive */}
        <div className="flex justify-between items-center h-16">
          {/* h-16 : hauteur de 64px */}
          
          {/* Titre principal */}
          <div className="text-xl font-bold text-gray-800">
            ASSISTANT FAQ
          </div>
          
          {/* Liens de navigation */}
          <div className="flex space-x-6">
            {/* space-x-6 : espace horizontal entre les liens */}
            <Link 
              href="/" 
              className="text-gray-600 hover:text-gray-900 transition"
            >
              Accueil
            </Link>
            <Link 
              href="/faq" 
              className="text-gray-600 hover:text-gray-900 transition"
            >
              FAQ Complète
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}