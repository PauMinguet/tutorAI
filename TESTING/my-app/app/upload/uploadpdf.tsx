import {
  Autocomplete,
  AutocompleteItem,
  Button,
  Input,
  Spinner,
} from "@nextui-org/react";
import React, { useState } from "react";

interface UploadPDFProps {
  onUpload: (file: File) => void;
}

const UploadPDF: React.FC<UploadPDFProps> = ({ onUpload }) => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [message, setMessage] = useState("");

  const items = [
    {
      key: "lecture",
      label: "Lecture",
    },
    {
      key: "slides",
      label: "Slides",
    },
    {
      key: "paper",
      label: "Paper",
    },
    {
      key: "notes",
      label: "Notes",
    },
    {
      key: "book",
      label: "Book",
    },
  ];

  const [text, setText] = useState("");
  const [name, setName] = useState("");
  const [author, setAuthor] = useState("");
  const [source, setSource] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFile(file);
      onUpload(file);
    }
  };

  const handleInsertClick = () => {
    setLoading(true);
    setSuccess(false);
    const data = {
      text: text,
      name: name,
      author: author,
      source: source,
    };

    // Create a new FormData instance
    const formData = new FormData();

    // Append the data fields
    for (const key in data) {
      formData.append(key, data[key]);
    }

    // Append the file
    // Note: `file` should be the File object for the PDF file
    // You might need to store this in your component's state when the file is selected
    formData.append("file", file);

    fetch("https://tutorai-k0k2.onrender.com/insert/PDF", {
      method: "POST",
      body: formData, // Send the FormData instance as the request body
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        setLoading(false);
        setSuccess(true);
      })
      .catch((error) => {
        console.error("Error:", error);
        setLoading(false);
      });

    setText("");
    setName("");
    setAuthor("");
    setSource("");
  };

  return (
    <div className="w-2/3">
      <div className="mt-5">
        <p className="mb-3">Name:</p>
        <Input
          type="email"
          label=""
          placeholder="Lecture 1: Jerkin"
          height="300"
          onValueChange={(value) => setMessage(value)}
        />
      </div>
      <div className="mt-5">
        <p className="mb-3">Author:</p>
        <Input
          type="email"
          label=""
          placeholder="Prof. Deez Nuts"
          height="300"
          onValueChange={(value) => setMessage(value)}
        />
      </div>
      <div className="mt-10 flex items-center">
        <Autocomplete
          defaultItems={items}
          label="Source"
          placeholder="Search source"
          className="max-w-xs"
        >
          {(item) => (
            <AutocompleteItem className="text-black" key={item.key}>
              {item.label}
            </AutocompleteItem>
          )}
        </Autocomplete>
      </div>
      <div className="mt-10">
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
        />
      </div>
      <div className="w-full mt-5 flex justify-center">
        <Button size="lg" color="warning" onClick={handleInsertClick}>
          Insert
        </Button>
      </div>
      <div className="w-full mt-5 flex justify-center">
        {loading && <Spinner />}
        {success && <p>Success!</p>}
      </div>
    </div>
  );
};

export default UploadPDF;
