import React, { useState } from "react";
import {
  Autocomplete,
  AutocompleteItem,
  Button,
  Input,
  Textarea,
  Spinner,
} from "@nextui-org/react";

interface InsertTextProps {
  onInsert: (text: string) => void;
}

const TextComponent: React.FC<InsertTextProps> = ({ onInsert }) => {
  const [text, setText] = useState("");
  const [name, setName] = useState("");
  const [author, setAuthor] = useState("");
  const [source, setSource] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleInsertClick = () => {
    setLoading(true);
    setSuccess(false);
    const data = {
      text: text,
      name: name,
      author: author,
      source: source,
    };

    fetch("https://tutorai-k0k2.onrender.com/insert/text", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
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

  return (
    <div className="w-2/3">
      <div className="mt-5">
        <p className="mb-3">Name:</p>
        <Input
          type="email"
          label=""
          placeholder="Lecture 1: Jerkin"
          height="300"
          onValueChange={(value) => setName(value)}
        />
      </div>
      <div className="mt-5">
        <p className="mb-3">Author:</p>
        <Input
          type="email"
          label=""
          placeholder="Prof. Deez Nuts"
          height="300"
          onValueChange={(value) => setAuthor(value)}
        />
      </div>
      <div className="mt-10 flex items-center">
        <Autocomplete
          defaultItems={items}
          label="Source"
          color="default"
          placeholder="Search Source"
          className="max-w-xs"
          onSelectionChange={(item) => setSource(item.label)}
        >
          {(item) => (
            <AutocompleteItem className="text-black" key={item.key}>
              {item.label}
            </AutocompleteItem>
          )}
        </Autocomplete>
      </div>
      <div className="mt-5">
        <p className="mb-3">Text:</p>
        <Input
          type="email"
          label=""
          placeholder="Text here"
          onValueChange={(value) => setText(value)}
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

export default TextComponent;
