"use client";
import { useDropzone } from "react-dropzone";
import { useState } from "react";
import Link from "next/link";
import axios from "axios";

import "../globals.css";

export default function UploadComponent() {
  const [name, setName] = useState("");
  const [author, setAuthor] = useState("");
  const [sourceType, setSourceType] = useState("");
  const [files, setFiles] = useState([]);


  const { getRootProps, getInputProps } = useDropzone({
    accept: 'application/pdf',
    onDrop: (acceptedFiles) => {
      setFiles(acceptedFiles);
    },
  });

  const handleUpload = async () => {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('file', file);
    });

    try {
      const response = await axios.post('/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
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
      <div className="min-h-screen bg-gray-900 text-white flex flex-col p-10 w-3/5 mx-auto">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Name"
          className="p-2 mb-4 bg-gray-800 text-white rounded"
        />
        <input
          type="text"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          placeholder="Author"
          className="p-2 mb-4 bg-gray-800 text-white rounded"
        />
        <select
          value={sourceType}
          onChange={(e) => setSourceType(e.target.value)}
          className="p-2 mb-4 bg-gray-800 text-white rounded"
        >
          <option value="">Select source type</option>
          <option value="book">Book</option>
          <option value="article">Article</option>
          <option value="website">Website</option>
        </select>
        <div className="flex items-center justify-center mx-auto w-40 bg-gray-800 text-white rounded cursor-pointer mb-10 mt-5">
          <div
            {...getRootProps()}
            className="p-5 bg-white rounded shadow-lg text-center h-40 w-40 flex flex-col items-center justify-center cursor-pointer"
          >
            <input {...getInputProps()} />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a4 4 0 01-4-4V7a4 4 0 014-4h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V17a4 4 0 01-4 4z"
              />
            </svg>
            <p className="mt-1 text-sm text-gray-600">
              <button className="font-medium text-indigo-600 hover:text-indigo-500 focus:outline-none focus:underline transition duration-150 ease-in-out">
                Upload a file
              </button>
              or drag and drop
            </p>
            <p className="mt-1 text-xs text-center text-gray-500">
              PNG, JPG, GIF up to 10MB
            </p>
            
          </div>
        </div>

        <button className="mx-auto w-60 p-2 bg-blue-500 text-white rounded active:bg-blue-700">
          Upload
        </button>
      </div>
    </div>
  );
}
