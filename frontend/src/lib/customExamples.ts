export interface Example {
  id: string;
  title: string;
  prompt: string;
  image: string;
}

const KEY = 'customExamples';

export function loadCustomExamples(): Example[] {
  const data = localStorage.getItem(KEY);
  return data ? (JSON.parse(data) as Example[]) : [];
}

export function addCustomExample(ex: Omit<Example, 'id'>): Example {
  const list = loadCustomExamples();
  const item: Example = { id: Date.now().toString(), ...ex };
  list.push(item);
  localStorage.setItem(KEY, JSON.stringify(list));
  return item;
}
