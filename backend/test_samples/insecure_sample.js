// Dangerous eval (ESLint: no-eval)
function executeStudentFormula(userInputFormula) {
    const calculation = eval(userInputFormula);
    
    // Loose equality check (ESLint: eqeqeq)
    if (userInputFormula == 0) {
        // Undeclared variable leak (ESLint: no-undef)
        statusFlag = "Special condition met";
        // Debugger statement (ESLint: no-debugger)
        debugger;
    }
    
    return calculation;
}
