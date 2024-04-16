import React, { useState } from "react";
import {
  Autocomplete,
  AutocompleteItem,
  Button,
  Input,
  Spinner,
  Textarea,
} from "@nextui-org/react";

interface InsertTextProps {
  onInsert: (text: string) => void;
}

const TextComponent: React.FC<InsertTextProps> = ({ onInsert }) => {
  const [text, setText] = useState("");
  const [source, setSource] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleInputChange = (value: string) => {
    setText(value);
  };

  const handleInsertClick = () => {
    setLoading(true);
    setSuccess(false);
    const data = {
      link: text,
      source: source,
    };

    fetch("https://tutorai-k0k2.onrender.com/insert/YT/", {
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
    <div className="w-2/3 mt-5 justify-center items-center">
        <p className="mb-3">YouTube Link:</p>
      <Textarea
        label="Description"
        className="w-full h-10"
        placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley"
        value={text}
        onValueChange={handleInputChange}
      />
      <div className="mt-10">
        <Autocomplete
          defaultItems={items}
          label="Source"
          color="default"
          placeholder="Search Source"
          className="max-w-xs"
          onSelectionChange={(item) => setSource(item.label)}
        >
          {(item) => (
            <AutocompleteItem className="text-black color-black" key={item.key}>
              {item.label}
            </AutocompleteItem>
          )}
        </Autocomplete>
      </div>
      <div className="w-full mt-5 flex justify-center">
      <Button
        className="ml-5 mt-2"
        size="md"
        color="warning"
        onClick={handleInsertClick}
      >
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
