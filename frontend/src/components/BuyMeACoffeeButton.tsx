import React from 'react';

interface BuyMeACoffeeButtonProps {
  className?: string;
}

const BuyMeACoffeeButton: React.FC<BuyMeACoffeeButtonProps> = ({ className }) => {
  return (
    <a
      href="https://buymeacoffee.com/bilt.au"
      target="_blank"
      rel="noopener noreferrer"
      className={`bmc-button ${className || ''}`}
      style={{
        display: 'inline-block',
        padding: '8px 16px',
        backgroundColor: '#FFDD00',
        color: '#000000',
        textDecoration: 'none',
        borderRadius: '8px',
        fontFamily: 'Cookie, cursive',
        fontWeight: 'bold',
        border: '2px solid #000000',
        transition: 'all 0.3s ease'
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.backgroundColor = '#FFE55C';
        e.currentTarget.style.transform = 'translateY(-2px)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.backgroundColor = '#FFDD00';
        e.currentTarget.style.transform = 'translateY(0)';
      }}
    >
      ☕ Buy me a coffee
    </a>
  );
};

export default BuyMeACoffeeButton;