import React from 'react';

export function Greeting() {
  const hour = new Date().getHours();
  let text = 'Olá, visitante!';

  if (hour < 12) text = 'Bom dia, visitante!';
  else if (hour < 18) text = 'Boa tarde, visitante!';
  else text = 'Boa noite, visitante!';

  return <p className="text-gray-600 mb-4 text-center">{text}</p>;
}

