const nums = [14, 23, 12, 32, 12, 3];

function solve(nums) {
    let map = {};
    let res = [];
    for (let i = 0; i < nums.length; i++) {
        if (!map[nums[i]]) {
            map[nums[i]] = true;
            res.push(nums[i]);
        }
    }
    console.log("Array after removing duplicates:", res);
}
// const fs = require("fs");
// const input = fs.readFileSync(0, "utf-8").trim();
// nums = input.split(" ").map(Number)
solve(nums);
