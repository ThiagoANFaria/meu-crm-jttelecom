import React from 'react';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface LeadScoringProps {
  score: number;
  showDetails?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

const LeadScoring: React.FC<LeadScoringProps> = ({ 
  score, 
  showDetails = false, 
  size = 'md' 
}) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'bg-green-500';
    if (score >= 60) return 'bg-yellow-500';
    if (score >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Quente';
    if (score >= 60) return 'Morno';
    if (score >= 40) return 'Frio';
    return 'Gelado';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 60) return <TrendingUp className="w-3 h-3" />;
    if (score >= 40) return <Minus className="w-3 h-3" />;
    return <TrendingDown className="w-3 h-3" />;
  };

  const sizeClasses = {
    sm: 'text-xs px-1 py-0.5',
    md: 'text-sm px-2 py-1',
    lg: 'text-base px-3 py-1.5'
  };

  if (!showDetails) {
    return (
      <Badge 
        variant="secondary" 
        className={`${getScoreColor(score)} text-white ${sizeClasses[size]} flex items-center gap-1`}
      >
        {getScoreIcon(score)}
        {score}
      </Badge>
    );
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium">Lead Score</span>
        <Badge 
          variant="secondary" 
          className={`${getScoreColor(score)} text-white flex items-center gap-1`}
        >
          {getScoreIcon(score)}
          {score} - {getScoreLabel(score)}
        </Badge>
      </div>
      <Progress value={score} className="h-2" />
      <div className="text-xs text-gray-500">
        Baseado em: perfil, engajamento, comportamento e timing
      </div>
    </div>
  );
};

export default LeadScoring;

