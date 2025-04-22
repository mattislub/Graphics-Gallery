הקובץ המרוכז ל-Next.js יראה כך:

./app/theme/static_src/node_modules/camelcase-css/index.js
-----
const pattern = /-(\w|$)/g;

const callback = (dashChar, char) => char.toUpperCase();

const camelCaseCSS = (property) => {
	property = property.toLowerCase();

	// NOTE :: IE8's "styleFloat" is intentionally not supported
	if (property === "float") {
		return "cssFloat";
	}
	// Microsoft vendor-prefixes are uniquely cased
	else if (property.charCodeAt(0) === 45 && property.charCodeAt(1) === 109 && property.charCodeAt(2) === 115 && property.charCodeAt(3) === 45) {
		return property.substr(1).replace(pattern, callback);
	} else {
		return property.replace(pattern, callback);
	}
};

export default camelCaseCSS;

-----

השינויים הם החלפת "use strict" בקובץ המקורי עם שימוש בקוד ES6, והחלפת module.exports = camelCaseCSS; עם export default camelCaseCSS; כדי להתאים למערכת המודולים של ES6 שמשתמשת Next.js.