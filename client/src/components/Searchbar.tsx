import React, { useCallback, useEffect, useRef } from "react";
import "../styles/Searchbar.css"
import { debounce } from "lodash";

type SearchbarProps = {
  handleSearch: (query: string) => void;
};

const Searchbar: React.FC<SearchbarProps> = ({ handleSearch }) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const debouncedSearch = debounce((query: string) => {
    handleSearch(query);
  }, 500);

  // Cancel debounce on unmount to avoid memory leaks
  useEffect(() => {
    return () => {
      debouncedSearch.cancel();
    };
  }, [debouncedSearch]);

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
      placeholder="Search a player..."
    />
  );
};

export default Searchbar;
