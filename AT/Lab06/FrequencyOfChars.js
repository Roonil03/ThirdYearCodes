function solve(str) {
    const frequency = new Map();
    for (const char of str) {
        frequency.set(char, (frequency.get(char) || 0) + 1);
    }
    return frequency;
}
const text = "hello world";
console.log(solve(text));
console.log(solve("banana"));