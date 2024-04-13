import Link from 'next/link';
import React from 'react';



const NavBar: React.FC = () => {
  return (
    <nav className="bg-gray-800 p-4">
        <div className="flex justify-between items-center">
          <div className="text-2xl font-extrabold">tutorAI</div>
          <div className="flex space-x-20 mr-16 font-ubuntu">
            <Link legacyBehavior href="/home">
              <a className="text-md">Home</a>
            </Link>
            <Link legacyBehavior href="/upload">
              <a className="text-md">Upload</a>
            </Link>
            <Link legacyBehavior href="/chat">
              <a className="text-md">Chat</a>
            </Link>
            <Link legacyBehavior href="/settings">
              <a className="text-md">Settings</a>
            </Link>
            <Link legacyBehavior href="/about">
              <a className="text-md">About</a>
            </Link>
          </div>
        </div>
      </nav>
  );
};

export default NavBar;