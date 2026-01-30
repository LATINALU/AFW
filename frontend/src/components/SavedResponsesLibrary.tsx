/**
 * Saved Responses Library v1.0.0
 * ===============================
 * Biblioteca de respuestas guardadas con búsqueda y categorización.
 */

'use client';

import React, { useState, useEffect } from 'react';
import { 
  Bookmark, 
  Search, 
  Filter, 
  Download, 
  Share2, 
  Trash2,
  Star,
  Copy,
  Check,
  X
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

interface SavedResponse {
  response_id: string;
  agent_id: string;
  agent_name: string;
  content: string;
  title: string;
  tags: string[];
  category: string;
  created_at: string;
  is_favorite: boolean;
}

interface SavedResponsesLibraryProps {
  isOpen: boolean;
  onClose: () => void;
}

export function SavedResponsesLibrary({ isOpen, onClose }: SavedResponsesLibraryProps) {
  const [responses, setResponses] = useState<SavedResponse[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  useEffect(() => {
    if (isOpen) {
      loadResponses();
    }
  }, [isOpen, selectedCategory]);

  const loadResponses = async () => {
    try {
      const token = localStorage.getItem('token');
      const url = selectedCategory
        ? `/api/conversations/responses/list?category=${selectedCategory}`
        : '/api/conversations/responses/list';

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setResponses(data.responses || []);
      }
    } catch (error) {
      console.error('Error loading saved responses:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (responseId: string) => {
    if (!confirm('¿Eliminar esta respuesta guardada?')) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/conversations/responses/${responseId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setResponses(responses.filter(r => r.response_id !== responseId));
      }
    } catch (error) {
      console.error('Error deleting response:', error);
    }
  };

  const handleCopy = async (content: string, responseId: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedId(responseId);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (error) {
      console.error('Error copying:', error);
    }
  };

  const handleExport = (response: SavedResponse) => {
    const blob = new Blob([response.content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${response.title.replace(/[^a-z0-9]/gi, '_')}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const filteredResponses = responses.filter(response =>
    response.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    response.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
    response.agent_name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const categories = Array.from(new Set(responses.map(r => r.category).filter(Boolean)));

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="fixed inset-4 md:inset-10 lg:inset-20 bg-background rounded-lg border border-border z-50 flex flex-col overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border">
              <div className="flex items-center gap-3">
                <Bookmark className="w-6 h-6 text-primary" />
                <div>
                  <h2 className="text-xl font-bold">Respuestas Guardadas</h2>
                  <p className="text-sm text-muted-foreground">
                    {responses.length} respuesta{responses.length !== 1 ? 's' : ''} guardada{responses.length !== 1 ? 's' : ''}
                  </p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="p-2 hover:bg-accent rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Search and Filters */}
            <div className="p-4 border-b border-border space-y-3">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Buscar respuestas..."
                  className="w-full pl-10 pr-4 py-2 bg-accent rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                />
              </div>

              {categories.length > 0 && (
                <div className="flex items-center gap-2 flex-wrap">
                  <Filter className="w-4 h-4 text-muted-foreground" />
                  <button
                    onClick={() => setSelectedCategory(null)}
                    className={`px-3 py-1 rounded-full text-xs transition-colors ${
                      selectedCategory === null
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-accent hover:bg-accent/80'
                    }`}
                  >
                    Todas
                  </button>
                  {categories.map((category) => (
                    <button
                      key={category}
                      onClick={() => setSelectedCategory(category)}
                      className={`px-3 py-1 rounded-full text-xs transition-colors ${
                        selectedCategory === category
                          ? 'bg-primary text-primary-foreground'
                          : 'bg-accent hover:bg-accent/80'
                      }`}
                    >
                      {category}
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Responses List */}
            <div className="flex-1 overflow-y-auto p-4">
              {loading ? (
                <div className="text-center py-12 text-muted-foreground">
                  Cargando...
                </div>
              ) : filteredResponses.length === 0 ? (
                <div className="text-center py-12">
                  <Bookmark className="w-16 h-16 mx-auto mb-4 text-muted-foreground opacity-50" />
                  <p className="text-muted-foreground">
                    {searchQuery ? 'No se encontraron respuestas' : 'No hay respuestas guardadas'}
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                  {filteredResponses.map((response) => (
                    <ResponseCard
                      key={response.response_id}
                      response={response}
                      onDelete={() => handleDelete(response.response_id)}
                      onCopy={() => handleCopy(response.content, response.response_id)}
                      onExport={() => handleExport(response)}
                      isCopied={copiedId === response.response_id}
                    />
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

interface ResponseCardProps {
  response: SavedResponse;
  onDelete: () => void;
  onCopy: () => void;
  onExport: () => void;
  isCopied: boolean;
}

function ResponseCard({ response, onDelete, onCopy, onExport, isCopied }: ResponseCardProps) {
  const [expanded, setExpanded] = useState(false);

  return (
    <motion.div
      layout
      className="bg-accent rounded-lg border border-border overflow-hidden"
    >
      {/* Header */}
      <div className="p-4 border-b border-border">
        <div className="flex items-start justify-between gap-2 mb-2">
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-sm sm:text-base truncate">
              {response.title}
            </h3>
            <p className="text-xs text-muted-foreground">
              {response.agent_name}
            </p>
          </div>
          {response.is_favorite && (
            <Star className="w-4 h-4 text-yellow-500 fill-yellow-500 flex-shrink-0" />
          )}
        </div>

        {response.tags && response.tags.length > 0 && (
          <div className="flex flex-wrap gap-1">
            {response.tags.map((tag, index) => (
              <span
                key={index}
                className="px-2 py-0.5 bg-primary/10 text-primary text-xs rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Content Preview */}
      <div className="p-4">
        <div
          className={`prose prose-sm max-w-none text-xs sm:text-sm ${
            !expanded ? 'line-clamp-3' : ''
          }`}
        >
          <ReactMarkdown>{response.content}</ReactMarkdown>
        </div>
        {response.content.length > 200 && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-xs text-primary hover:underline mt-2"
          >
            {expanded ? 'Ver menos' : 'Ver más'}
          </button>
        )}
      </div>

      {/* Footer */}
      <div className="p-3 bg-background/50 border-t border-border flex items-center justify-between">
        <span className="text-xs text-muted-foreground">
          {new Date(response.created_at).toLocaleDateString('es-ES')}
        </span>
        <div className="flex items-center gap-1">
          <button
            onClick={onCopy}
            className="p-2 hover:bg-accent rounded transition-colors"
            title="Copiar"
          >
            {isCopied ? (
              <Check className="w-4 h-4 text-green-500" />
            ) : (
              <Copy className="w-4 h-4" />
            )}
          </button>
          <button
            onClick={onExport}
            className="p-2 hover:bg-accent rounded transition-colors"
            title="Exportar"
          >
            <Download className="w-4 h-4" />
          </button>
          <button
            onClick={onDelete}
            className="p-2 hover:bg-accent rounded transition-colors text-red-500"
            title="Eliminar"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </motion.div>
  );
}
