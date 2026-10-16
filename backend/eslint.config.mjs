export default [
  {
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        // Browser globals
        window: "readonly",
        document: "readonly",
        navigator: "readonly",
        fetch: "readonly",
        console: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly",
        setInterval: "readonly",
        clearInterval: "readonly",
        localStorage: "readonly",
        sessionStorage: "readonly",
        alert: "readonly",
        URL: "readonly",
        FormData: "readonly",
        // Node.js globals
        process: "readonly",
        require: "readonly",
        module: "readonly",
        exports: "readonly",
        __dirname: "readonly",
        __filename: "readonly",
        Buffer: "readonly",
        global: "readonly"
      }
    },
    rules: {
      "no-eval": "error",
      "no-implied-eval": "error",
      "no-new-func": "error",
      "no-caller": "error",
      "no-script-url": "error",
      "no-proto": "error",
      "no-iterator": "error",
      "no-self-compare": "error",
      "no-unreachable": "error",
      "no-unused-vars": ["warn", { "args": "none", "varsIgnorePattern": "^_" }],
      "eqeqeq": ["warn", "smart"],
      "no-undef": "error",
      "no-debugger": "warn",
      "no-alert": "warn",
      "no-empty": "warn"
    }
  }
];
