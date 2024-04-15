"use client";
import "../globals.css";
import NavBar1 from "../components/navbar1";
import { auth, currentUser } from "@clerk/nextjs";
import {
  Accordion,
  AccordionItem,
  Button,
  Card,
  CardBody,
} from "@nextui-org/react";

export default function Home() {
  var classes = ["CSC 480", "CSC 366", "Knowledge Discovery from Data"];
  var docs = {
    "CSC 480": [
      "Introduction to CSC 480",
      "CSC 480 Lecture Notes",
      "CSC 480 Assignment 1",
    ],
    "CSC 366": [
      "CSC 366 Syllabus",
      "CSC 366 Midterm Review",
      "CSC 366 Final Project",
      "CSC 366 Homework 2",
    ],
    "Knowledge Discovery from Data": [
      "Data Preprocessing Techniques",
      "Data Mining Algorithms",
      "Visualization in Data Discovery",
    ],
  };

  const handleDelete = (c, d) => () => {
    if (window.confirm("Are you sure you want to delete " + d + "?")) {
      fetch('https://your-api-url.com/delete', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ docName: d }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          docs[c].splice(j, 1);
        } else {
          alert('Failed to delete document.');
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
  };



  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <NavBar1 />
      <main className="flex flex-col items-center mt-10 py-2 text-center flex-grow">
        <div className="z-10 max-w-5xl w-full p-6 bg-gray-800 rounded-xl shadow-md space-y-4">
          <h1 className="text-4xl font-extrabold text-white mb-4">
            My Classes
          </h1>
          <div className="text-lg text-white">
            <Accordion>
              {classes.map((c, i) => (
                <AccordionItem
                  key={i}
                  aria-label={c}
                  title={<span className="text-white">{c}</span>}
                >
                  {docs[c].map((d, j) => (
                    <div key={j} className="flex items-center mt-4">
                      <Card className="flex-grow">
                        <CardBody>
                          <p>{d}</p>
                        </CardBody>
                      </Card>
                      <Button
                        className="ml-4 bg-rose-500"
                        color="success"
                        onClick={handleDelete(c, d)}
                      >
                        Delete
                      </Button>
                    </div>
                  ))}
                </AccordionItem>
              ))}
            </Accordion>
          </div>
        </div>
      </main>
      <footer className="bg-gray-800 p-4 text-center text-sm">
        <p>&copy; 2024 tutorAI. All rights reserved.</p>
        <p>123 Main St, Anytown, USA</p>
        <p>Email: info@tutorai.com</p>
      </footer>
    </div>
  );
}
