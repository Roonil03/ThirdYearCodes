   
const nums = [14,23,12,32,12,3];

function solve(nums){
    let res = nums[0];
    for(let i = 1; i < nums.length; i++){
        if(nums[i] > res){
            res = nums[i];
        }
    }
    console.log("The largest element is: ", res);
}
solve(nums);
