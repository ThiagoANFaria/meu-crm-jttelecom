import React from 'react';

export function Greeting() {
  const hour = new Date().getHours();
  let text = 'Olá, visitante!';
  let emoji = '👋';

  if (hour < 12) {
    text = 'Bom dia, visitante!';
    emoji = '🌅';
  } else if (hour < 18) {
    text = 'Boa tarde, visitante!';
    emoji = '☀️';
  } else {
    text = 'Boa noite, visitante!';
    emoji = '🌙';
  }

  return (
    <div className="text-center mb-4">
      <p className="text-gray-600 text-sm flex items-center justify-center gap-2">
        <span className="text-lg" role="img" aria-label={`Emoji ${emoji}`}>
          {emoji}
        </span>
        <span>{text}</span>
      </p>
    </div>
  );
}

