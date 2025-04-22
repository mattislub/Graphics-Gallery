הקובץ המתורגם:
-----
const eaw = {};

const eastAsianWidth = (character) => {
  let x = character.charCodeAt(0);
  let y = (character.length === 2) ? character.charCodeAt(1) : 0;
  let codePoint = x;
  if ((0xD800 <= x && x <= 0xDBFF) && (0xDC00 <= y && y <= 0xDFFF)) {
    x &= 0x3FF;
    y &= 0x3FF;
    codePoint = (x << 10) | y;
    codePoint += 0x10000;
  }

  // ... (המשך הקוד לא משתנה)

  return 'N';
};

const characterLength = (character) => {
  const code = eastAsianWidth(character);
  if (code === 'F' || code === 'W' || code === 'A') {
    return 2;
  } else {
    return 1;
  }
};

// Split a string considering surrogate-pairs.
const stringToArray = (string) => {
  return string.match(/[\uD800-\uDBFF][\uDC00-\uDFFF]|[^\uD800-\uDFFF]/g) || [];
}

const length = (string) => {
  const characters = stringToArray(string);
  let len = 0;
  for (let i = 0; i < characters.length; i++) {
    len = len + characterLength(characters[i]);
  }
  return len;
};

const slice = (text, start, end) => {
  let textLen = length(text)
  start = start ? start : 0;
  end = end ? end : 1;
  if (start < 0) {
      start = textLen + start;
  }
  if (end < 0) {
      end = textLen + end;
  }
  let result = '';
  let eawLen = 0;
  const chars = stringToArray(text);
  for (let i = 0; i < chars.length; i++) {
    const char = chars[i];
    const charLen = length(char);
    if (eawLen >= start - (charLen === 2 ? 1 : 0)) {
        if (eawLen + charLen <= end) {
            result += char;
        } else {
            break;
        }
    }
    eawLen += charLen;
  }
  return result;
};

export default {
  eastAsianWidth,
  characterLength,
  length,
  slice
};
-----