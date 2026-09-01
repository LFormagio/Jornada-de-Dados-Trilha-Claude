import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  wide?: boolean;
}

export function Card({ children, className = '', wide = false }: CardProps) {
  return (
    <div className={`card ${wide ? 'wide' : ''} ${className}`}>
      {children}
    </div>
  );
}

export function CardHeader({ children, className = '' }: { children: React.ReactNode, className?: string }) {
  return <div className={`card-title ${className}`}>{children}</div>;
}

export function CardContent({ children, className = '' }: { children: React.ReactNode, className?: string }) {
  return <div className={className}>{children}</div>;
}
