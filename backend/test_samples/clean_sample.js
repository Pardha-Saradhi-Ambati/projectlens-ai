// Clean, secure JavaScript module
function calculateSquareRoot(value) {
    if (typeof value !== "number" || isNaN(value)) {
        throw new TypeError("Parameter must be a valid number");
    }

    if (value < 0) {
        throw new RangeError("Cannot calculate real square root of negative number");
    }

    const result = Math.sqrt(value);
    return result;
}

export { calculateSquareRoot };
