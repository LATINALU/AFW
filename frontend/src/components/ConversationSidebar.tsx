/**
 * Conversation Sidebar v1.0.0
 * ===========================
 * Sidebar de historial de conversaciones estilo ChatGPT/Gemini.
 */

'use client';

import React, { useState, useEffect } from 'react';
import { 
  MessageSquare, 
  Plus, 
  Search, 
  MoreVertical, 
  Pin, 
  Archive, 
  Trash2,
  Edit2,
  Check,
  X
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Conversation {
  conversation_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
  is_pinned: boolean;
  is_archived: boolean;
}

interface ConversationSidebarProps {
  isOpen: boolean;
  onClose?: () => void;
  onNewChat: () => void;
  onSelectConversation: (conversationId: string) => void;
  currentConversationId?: string;
}

export function ConversationSidebar({
  isOpen,
  onClose,
  onNewChat,
  onSelectConversation,
  currentConversationId,
}: ConversationSidebarProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');

  useEffect(() => {
    if (isOpen) {
      loadConversations();
    }
  }, [isOpen]);

  const loadConversations = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('/api/conversations/list?limit=100', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setConversations(data.conversations || []);
      }
    } catch (error) {
      console.error('Error loading conversations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadConversations();
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(
        `/api/conversations/search?q=${encodeURIComponent(searchQuery)}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setConversations(data.results || []);
      }
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  const handleUpdateTitle = async (conversationId: string, newTitle: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/conversations/${conversationId}/title`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: newTitle }),
      });

      if (response.ok) {
        setConversations(conversations.map(conv =>
          conv.conversation_id === conversationId
            ? { ...conv, title: newTitle }
            : conv
        ));
        setEditingId(null);
      }
    } catch (error) {
      console.error('Error updating title:', error);
    }
  };

  const handleDelete = async (conversationId: string) => {
    if (!confirm('¿Eliminar esta conversación?')) return;

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/conversations/${conversationId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setConversations(conversations.filter(c => c.conversation_id !== conversationId));
      }
    } catch (error) {
      console.error('Error deleting conversation:', error);
    }
  };

  const handlePin = async (conversationId: string, pinned: boolean) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/conversations/${conversationId}/pin`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pinned }),
      });

      if (response.ok) {
        loadConversations();
      }
    } catch (error) {
      console.error('Error pinning conversation:', error);
    }
  };

  const handleArchive = async (conversationId: string, archived: boolean) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/conversations/${conversationId}/archive`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ archived }),
      });

      if (response.ok) {
        loadConversations();
      }
    } catch (error) {
      console.error('Error archiving conversation:', error);
    }
  };

  const filteredConversations = conversations.filter(conv =>
    conv.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const pinnedConversations = filteredConversations.filter(c => c.is_pinned);
  const regularConversations = filteredConversations.filter(c => !c.is_pinned && !c.is_archived);

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: -300 }}
          animate={{ x: 0 }}
          exit={{ x: -300 }}
          transition={{ type: 'spring', damping: 30, stiffness: 300 }}
          className="fixed left-0 top-0 bottom-0 w-80 bg-background border-r border-border z-40 flex flex-col"
        >
          {/* Header */}
          <div className="p-4 border-b border-border">
            <button
              onClick={onNewChat}
              className="w-full flex items-center gap-2 px-4 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
            >
              <Plus className="w-5 h-5" />
              <span className="font-medium">Nueva Conversación</span>
            </button>
          </div>

          {/* Search */}
          <div className="p-4 border-b border-border">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Buscar conversaciones..."
                className="w-full pl-10 pr-4 py-2 bg-accent rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
              />
            </div>
          </div>

          {/* Conversations List */}
          <div className="flex-1 overflow-y-auto">
            {loading ? (
              <div className="p-4 text-center text-muted-foreground">
                Cargando...
              </div>
            ) : (
              <>
                {/* Pinned */}
                {pinnedConversations.length > 0 && (
                  <div className="mb-4">
                    <div className="px-4 py-2 text-xs font-semibold text-muted-foreground">
                      FIJADAS
                    </div>
                    {pinnedConversations.map((conv) => (
                      <ConversationItem
                        key={conv.conversation_id}
                        conversation={conv}
                        isActive={conv.conversation_id === currentConversationId}
                        isEditing={editingId === conv.conversation_id}
                        editTitle={editTitle}
                        onSelect={() => onSelectConversation(conv.conversation_id)}
                        onEdit={() => {
                          setEditingId(conv.conversation_id);
                          setEditTitle(conv.title);
                        }}
                        onSaveEdit={() => handleUpdateTitle(conv.conversation_id, editTitle)}
                        onCancelEdit={() => setEditingId(null)}
                        onEditTitleChange={setEditTitle}
                        onPin={() => handlePin(conv.conversation_id, false)}
                        onArchive={() => handleArchive(conv.conversation_id, true)}
                        onDelete={() => handleDelete(conv.conversation_id)}
                      />
                    ))}
                  </div>
                )}

                {/* Regular */}
                {regularConversations.length > 0 && (
                  <div>
                    {pinnedConversations.length > 0 && (
                      <div className="px-4 py-2 text-xs font-semibold text-muted-foreground">
                        RECIENTES
                      </div>
                    )}
                    {regularConversations.map((conv) => (
                      <ConversationItem
                        key={conv.conversation_id}
                        conversation={conv}
                        isActive={conv.conversation_id === currentConversationId}
                        isEditing={editingId === conv.conversation_id}
                        editTitle={editTitle}
                        onSelect={() => onSelectConversation(conv.conversation_id)}
                        onEdit={() => {
                          setEditingId(conv.conversation_id);
                          setEditTitle(conv.title);
                        }}
                        onSaveEdit={() => handleUpdateTitle(conv.conversation_id, editTitle)}
                        onCancelEdit={() => setEditingId(null)}
                        onEditTitleChange={setEditTitle}
                        onPin={() => handlePin(conv.conversation_id, true)}
                        onArchive={() => handleArchive(conv.conversation_id, true)}
                        onDelete={() => handleDelete(conv.conversation_id)}
                      />
                    ))}
                  </div>
                )}

                {filteredConversations.length === 0 && (
                  <div className="p-8 text-center text-muted-foreground">
                    <MessageSquare className="w-12 h-12 mx-auto mb-3 opacity-50" />
                    <p>No hay conversaciones</p>
                  </div>
                )}
              </>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

interface ConversationItemProps {
  conversation: Conversation;
  isActive: boolean;
  isEditing: boolean;
  editTitle: string;
  onSelect: () => void;
  onEdit: () => void;
  onSaveEdit: () => void;
  onCancelEdit: () => void;
  onEditTitleChange: (title: string) => void;
  onPin: () => void;
  onArchive: () => void;
  onDelete: () => void;
}

function ConversationItem({
  conversation,
  isActive,
  isEditing,
  editTitle,
  onSelect,
  onEdit,
  onSaveEdit,
  onCancelEdit,
  onEditTitleChange,
  onPin,
  onArchive,
  onDelete,
}: ConversationItemProps) {
  const [showMenu, setShowMenu] = useState(false);

  return (
    <div
      className={`group relative px-4 py-3 hover:bg-accent transition-colors ${
        isActive ? 'bg-accent' : ''
      }`}
    >
      {isEditing ? (
        <div className="flex items-center gap-2">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => onEditTitleChange(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') onSaveEdit();
              if (e.key === 'Escape') onCancelEdit();
            }}
            className="flex-1 px-2 py-1 bg-background border border-border rounded text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            autoFocus
          />
          <button
            onClick={onSaveEdit}
            className="p-1 hover:bg-background rounded"
          >
            <Check className="w-4 h-4 text-green-500" />
          </button>
          <button
            onClick={onCancelEdit}
            className="p-1 hover:bg-background rounded"
          >
            <X className="w-4 h-4 text-red-500" />
          </button>
        </div>
      ) : (
        <>
          <div
            onClick={onSelect}
            className="flex items-start gap-3 cursor-pointer"
          >
            <MessageSquare className="w-4 h-4 mt-1 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2">
                {conversation.is_pinned && (
                  <Pin className="w-3 h-3 text-primary" />
                )}
                <p className="text-sm font-medium truncate">
                  {conversation.title}
                </p>
              </div>
              <p className="text-xs text-muted-foreground">
                {conversation.message_count} mensajes · {formatDate(conversation.updated_at)}
              </p>
            </div>
          </div>

          <button
            onClick={() => setShowMenu(!showMenu)}
            className="absolute right-2 top-3 p-1 opacity-0 group-hover:opacity-100 hover:bg-background rounded transition-opacity"
          >
            <MoreVertical className="w-4 h-4" />
          </button>

          {showMenu && (
            <div className="absolute right-2 top-10 bg-background border border-border rounded-lg shadow-lg z-50 py-1 min-w-[150px]">
              <button
                onClick={() => {
                  onEdit();
                  setShowMenu(false);
                }}
                className="w-full px-3 py-2 text-left text-sm hover:bg-accent flex items-center gap-2"
              >
                <Edit2 className="w-4 h-4" />
                Renombrar
              </button>
              <button
                onClick={() => {
                  onPin();
                  setShowMenu(false);
                }}
                className="w-full px-3 py-2 text-left text-sm hover:bg-accent flex items-center gap-2"
              >
                <Pin className="w-4 h-4" />
                {conversation.is_pinned ? 'Desfijar' : 'Fijar'}
              </button>
              <button
                onClick={() => {
                  onArchive();
                  setShowMenu(false);
                }}
                className="w-full px-3 py-2 text-left text-sm hover:bg-accent flex items-center gap-2"
              >
                <Archive className="w-4 h-4" />
                Archivar
              </button>
              <button
                onClick={() => {
                  onDelete();
                  setShowMenu(false);
                }}
                className="w-full px-3 py-2 text-left text-sm hover:bg-accent flex items-center gap-2 text-red-500"
              >
                <Trash2 className="w-4 h-4" />
                Eliminar
              </button>
            </div>
          )}
        </>
      )}
    </div>
  );
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Ahora';
  if (diffMins < 60) return `${diffMins}m`;
  if (diffHours < 24) return `${diffHours}h`;
  if (diffDays < 7) return `${diffDays}d`;
  
  return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' });
}
