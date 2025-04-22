/**
 * Tailwind config.
 **/

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         **/

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         **/
        '../../**/templates/**/*.html',

        /**
         * JS. Paths to JS files that will contain Tailwind CSS classes (BASE_DIR/static/static/js).
         **/
        '../../static/static/js/*.js',

    ],
    theme: {
        container: {
          center: true,
        },
        extend: {
          colors: {
            blue: '#030339',
            green: '#21FEC7',
            orange: '#FA972A',
            light_blue: '#1939F8',
          },
          backgroundImage: ({ theme }) => ({
            'gradient-1': `linear-gradient(90deg, #FA972A, #1939F8, #21FEC7, #F84AC0)`,
            'gradient-2': `linear-gradient(90deg, #FA972A, #1939F8, #21FEC7)`,
          }),
        },
      },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
