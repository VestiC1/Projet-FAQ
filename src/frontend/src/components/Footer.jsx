// Composant Footer : pied de page minimaliste
export default function Footer() {
  return (
    <footer className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200">
      {/* border-t : bordure en haut */}
      <div className="max-w-7xl mx-auto px-4 py-4 text-center text-sm text-gray-500">
        © {new Date().getFullYear()} Assistant FAQ. Tous droits réservés.
        {/* {new Date().getFullYear()} : année dynamique (2025) */}
      </div>
    </footer>
  );
}