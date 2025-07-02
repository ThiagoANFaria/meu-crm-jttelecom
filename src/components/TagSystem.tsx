import React, { useState } from 'react';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Plus, X, Tag as TagIcon } from 'lucide-react';
import { Tag } from '@/types';

interface TagSystemProps {
  tags: Tag[];
  selectedTags?: Tag[];
  onTagsChange?: (tags: Tag[]) => void;
  editable?: boolean;
}

const TagSystem: React.FC<TagSystemProps> = ({
  tags,
  selectedTags = [],
  onTagsChange,
  editable = false
}) => {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [newTagName, setNewTagName] = useState('');
  const [newTagColor, setNewTagColor] = useState('#3B82F6');

  const predefinedColors = [
    '#3B82F6', // Blue
    '#10B981', // Green
    '#F59E0B', // Yellow
    '#EF4444', // Red
    '#8B5CF6', // Purple
    '#F97316', // Orange
    '#06B6D4', // Cyan
    '#84CC16', // Lime
    '#EC4899', // Pink
    '#6B7280'  // Gray
  ];

  const handleTagToggle = (tag: Tag) => {
    if (!onTagsChange) return;
    
    const isSelected = selectedTags.some(t => t.id === tag.id);
    if (isSelected) {
      onTagsChange(selectedTags.filter(t => t.id !== tag.id));
    } else {
      onTagsChange([...selectedTags, tag]);
    }
  };

  const handleCreateTag = () => {
    if (!newTagName.trim() || !onTagsChange) return;

    const newTag: Tag = {
      id: Date.now().toString(),
      name: newTagName.trim(),
      color: newTagColor,
      created_at: new Date().toISOString()
    };

    // Adicionar à lista de tags disponíveis (isso seria feito via API)
    onTagsChange([...selectedTags, newTag]);
    setNewTagName('');
    setNewTagColor('#3B82F6');
    setIsCreateModalOpen(false);
  };

  const handleRemoveTag = (tagToRemove: Tag) => {
    if (!onTagsChange) return;
    onTagsChange(selectedTags.filter(t => t.id !== tagToRemove.id));
  };

  return (
    <div className="space-y-3">
      {/* Tags Selecionadas */}
      {selectedTags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedTags.map((tag) => (
            <Badge
              key={tag.id}
              variant="secondary"
              style={{ backgroundColor: tag.color, color: 'white' }}
              className="flex items-center gap-1"
            >
              <TagIcon className="w-3 h-3" />
              {tag.name}
              {editable && (
                <button
                  onClick={() => handleRemoveTag(tag)}
                  className="ml-1 hover:bg-black/20 rounded-full p-0.5"
                >
                  <X className="w-3 h-3" />
                </button>
              )}
            </Badge>
          ))}
        </div>
      )}

      {/* Tags Disponíveis */}
      {editable && (
        <div className="space-y-2">
          <Label className="text-sm font-medium">Tags Disponíveis</Label>
          <div className="flex flex-wrap gap-2">
            {tags
              .filter(tag => !selectedTags.some(st => st.id === tag.id))
              .map((tag) => (
                <Badge
                  key={tag.id}
                  variant="outline"
                  style={{ borderColor: tag.color, color: tag.color }}
                  className="cursor-pointer hover:bg-gray-50"
                  onClick={() => handleTagToggle(tag)}
                >
                  <TagIcon className="w-3 h-3 mr-1" />
                  {tag.name}
                </Badge>
              ))}
            
            {/* Botão Criar Nova Tag */}
            <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
              <DialogTrigger asChild>
                <Badge
                  variant="outline"
                  className="cursor-pointer hover:bg-gray-50 border-dashed"
                >
                  <Plus className="w-3 h-3 mr-1" />
                  Nova Tag
                </Badge>
              </DialogTrigger>
              <DialogContent className="sm:max-w-md">
                <DialogHeader>
                  <DialogTitle>Criar Nova Tag</DialogTitle>
                </DialogHeader>
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="tagName">Nome da Tag</Label>
                    <Input
                      id="tagName"
                      value={newTagName}
                      onChange={(e) => setNewTagName(e.target.value)}
                      placeholder="Ex: Cliente VIP"
                      className="mt-1"
                    />
                  </div>
                  
                  <div>
                    <Label>Cor da Tag</Label>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {predefinedColors.map((color) => (
                        <button
                          key={color}
                          onClick={() => setNewTagColor(color)}
                          className={`w-8 h-8 rounded-full border-2 ${
                            newTagColor === color ? 'border-gray-800' : 'border-gray-300'
                          }`}
                          style={{ backgroundColor: color }}
                        />
                      ))}
                    </div>
                    <Input
                      type="color"
                      value={newTagColor}
                      onChange={(e) => setNewTagColor(e.target.value)}
                      className="mt-2 w-full h-10"
                    />
                  </div>

                  <div className="flex justify-end gap-2">
                    <Button
                      variant="outline"
                      onClick={() => setIsCreateModalOpen(false)}
                    >
                      Cancelar
                    </Button>
                    <Button
                      onClick={handleCreateTag}
                      disabled={!newTagName.trim()}
                    >
                      Criar Tag
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </div>
      )}
    </div>
  );
};

export default TagSystem;

