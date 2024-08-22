import { debounce } from "lodash";
import React, { useCallback, useEffect, useRef } from "react";

type SearchbarProps = {
    handleSearch: (query:string) => void
}

const Searchbar2:React.FC<SearchbarProps> = ({handleSearch}) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDebounce = () => {
    if (inputRef.current){
        debounceFunc(inputRef.current.value)
    }
  }

  const debounceFunc = debounce((query:string)=>{
    handleSearch(query);
  }, 500)

  useEffect(()=> {
    return ()=>{
        debounceFunc.cancel()
    }
  }, [debounceFunc])
  


  return (
    <input
      id="input"
      type="text"
      ref={inputRef}
      onChange={handleDebounce}
      placeholder="Search a player..."
    />
  );
}

export default Searchbar2;
