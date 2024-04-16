"use client";
import "../globals.css";
import React from "react";
import { Tabs, Tab, Card, CardBody } from "@nextui-org/react";
import NavBar1 from "../components/navbar1";
import PdfComponent from "./uploadpdf";
import TextComponent from "./uploadtext";
import YouTubeComponent from "./uploadyoutube";

export default function Upload() {
  const [selectedTab, setSelectedTab] = React.useState("pdf");

  const tabs = [
    { id: "pdf", label: "PDF File" },
    { id: "yt", label: "YouTube Link" },
    { id: "text", label: "Text" },
  ];

  return (
    <>
      <NavBar1 />
      <div className="min-h-screen bg-gray-900 text-white flex flex-col">
        <div className="flex justify-center items-center mt-10">
          <Tabs
            aria-label="Options"
            color="warning"
            size="lg"
            onSelectionChange={(id) => setSelectedTab(id)}
          >
            {tabs.map((tab) => (
              <Tab key={tab.id} title={tab.label}></Tab>
            ))}
          </Tabs>
        </div>
        <div className="ml-20 mr-20 mt-10 p-6 bg-gray-800 rounded-xl shadow-md space-y-4 flex justify-center items-center">
          {selectedTab === "pdf" && <PdfComponent />}
          {selectedTab === "yt" && <YouTubeComponent />}
          {selectedTab === "text" && <TextComponent />}
        </div>
      </div>
    </>
  );
}
