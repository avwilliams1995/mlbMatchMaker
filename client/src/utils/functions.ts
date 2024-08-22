type DebounceProps = {
  func: (...args:any[]) => any
  delay?: number
}

export function debounce(func:(...args:any[]) => any, delay:number=500): (...args: any[]) => void {
  let timeoutId: ReturnType<typeof setTimeout>;

  return function (...args: any[]) {
    clearTimeout(timeoutId);

    timeoutId = setTimeout(() => {
      func(...args);
    }, delay);
  };
}