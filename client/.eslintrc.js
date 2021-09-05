module.exports = {
  root: true,

  env: {
    node: true,
  },

  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended',
    '@vue/typescript/recommended',
    'prettier',
  ],

  parserOptions: {
    'prettier/prettier': ['error', require('./.prettierrc')],
  },

  plugins: ['vue'],

  rules: {
    'no-console': 'off',
    'no-debugger': 'off',
    'no-var': ['error'],
    'eol-last': ['error', 'always'],
    'vue/component-tags-order': [
      'warn',
      {
        order: [['template', 'script'], 'style'],
      },
    ],
    'vue/brace-style': [
      'error',
      '1tbs',
      {
        allowSingleLine: true,
      },
    ],
  },

  overrides: [
    {
      files: [
        '**/__tests__/*.{j,t}s?(x)',
        '**/tests/unit/**/*.spec.{j,t}s?(x)',
      ],
      env: {
        jest: true,
      },
    },
  ],
};
