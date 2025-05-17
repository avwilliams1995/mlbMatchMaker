import React, { useCallback, useEffect, useRef, useState } from "react";
import "../styles/Searchbar.css"
import { debounce } from "lodash";

type SearchbarProps = {
  handleSearch: (query: string) => void;
};

const Searchbar: React.FC<SearchbarProps> = ({ handleSearch }) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const debouncedSearch = debounce((query: string) => {
    handleSearch(query);
  }, 50);

  // Cancel debounce on unmount to avoid memory leaks
  const placeholderStages = ["Search a player.", "Search a player..", "Search a player..."];
  const [placeholderIndex, setPlaceholderIndex] = useState(0);

useEffect(() => {
  const interval = setInterval(() => {
    setPlaceholderIndex((prev) => (prev + 1) % placeholderStages.length);
  }, 500); // Change every 500ms

  return () => clearInterval(interval); // Cleanup
}, []);

  const handleDebounce = () => {
    if (inputRef.current) {
      debouncedSearch(inputRef.current.value);
    }
  };

  return (
    <input
      id="input"
      type="text"
      ref={inputRef}
      onChange={handleDebounce}
      placeholder={placeholderStages[placeholderIndex]} 
      />
  );
};

export default Searchbar;
