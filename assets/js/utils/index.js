import Urls from './urls';

const reorder = (list, startIndex, endIndex) => {
  const result = Array.from(list);
  const [removed] = result.splice(startIndex, 1);
  result.splice(endIndex, 0, removed);

  return result;
};

function indexHelper(name) {
  switch (name) {
    case 'firstPokemon':
      return 0;
    case 'secondPokemon':
      return 1;
    case 'thirdPokemon':
      return 2;
    default:
      return null;
  }
}

// https://stackoverflow.com/a/25490531/4526204
function getCookieValue(a) {
  const b = document.cookie.match(`(^|;)\\s*${a}\\s*=\\s*([^;]+)`);
  return b ? b.pop() : '';
}

export {
  Urls,
  reorder,
  indexHelper,
  getCookieValue,
};
