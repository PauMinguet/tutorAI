"use client"
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar1 from '../components/navbar1';
import "../globals.css";

export default function Chat() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const sendMessage = async () => {
    try {
      const res = await axios.post('/api/chat', { message });
      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    if (message !== '') {
      sendMessage();
    }
  }, [message]);

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <Navbar1 />
      <div className="flex flex-col items-center justify-center py-2 text-center flex-grow">
        <div className="z-10 max-w-5xl w-full p-6 bg-gray-800 rounded-xl shadow-md space-y-4">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your message here"
            className="w-full p-2"
          />
          <div className="w-full p-2 bg-gray-700 rounded-xl">
            {response}
          </div>
        </div>
      </div>
    </div>
  );
}