"use client";
import React, { useState, useEffect } from "react";
import axios from "axios";
import Navbar1 from "../components/navbar1";
import "../globals.css";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Input,
  Tabs,
  Tab,
  Button,
  Textarea,
  Listbox,
  ListboxSection,
  ListboxItem,
} from "@nextui-org/react";

export default function Chat() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const handleSend = async (message: string) => {
    console.log(message);
    if (message === "") return;
    try {
      const res = await axios.get("https://tutorai-k0k2.onrender.com/", {
        params: {
          message: message
        }
      });
      setResponse(res.data.response);
      console.log(res.data.response);
    } catch (error) {
      console.error(error);
    }
  };

  let tabs = [
    {
      id: "CSC 480",
      label: "CSC 480",
      content:
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    },
    {
      id: "CSC 366",
      label: "CSC 366",
      content:
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
    },
    {
      id: "Knowledge Discovery from Data",
      label: "Knowledge Discovery from Data",
      content:
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <Navbar1 />
      <div className="flex flex-col items-center py-2 text-center flex-grow mt-10">
        <div className="mb-10">
          <div className="w-full">
            <Tabs aria-label="Options" color="warning" size="lg" align="center">
              {tabs.map((tab) => (
                <Tab key={tab.id} title={tab.label}></Tab>
              ))}
            </Tabs>
          </div>
        </div>
        <div className="z-10 max-w-5xl w-full p-6 bg-gray-800 rounded-xl shadow-md space-y-4">
          <div className="flex w-full flex-wrap md:flex-nowrap mb-6 md:mb-0 gap-4">
            <div className="flex w-full flex-wrap md:flex-nowrap gap-4">
              <Input
                type="email"
                label=""
                placeholder="Ask tutorAI!"
                height="300"
                onValueChange={(value) => setMessage(value)}
              />
              <Button
                size="md"
                className="ml-4 bg-rose-500"
                color="success"
                onClick={() => handleSend(message)}
              >
                Send
              </Button>
            </div>
          </div>
          <div className="flex w-full flex-wrap md:flex-nowrap mb-6 md:mb-0 gap-4">
            <Textarea label="Description" placeholder={response} />
          </div>
        </div>
      </div>
    </div>
  );
}
