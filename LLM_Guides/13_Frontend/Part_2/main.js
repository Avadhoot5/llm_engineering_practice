const user = {id:7, name: 'ada', likes: ['math', 'coffee'], address: {city:'mumbai'}};
const {name, likes: [firstLike]} = user;

console.log(name)
console.log(firstLike)

const more = {...user, active:true};
const [head, ...tail] = [1,2,3,4];

console.log(more);
console.log(head, tail)


const city = user?.address?.city ?? "Unknown";
console.log(city)

const scores = [5, 3, 9];
const sorted = scores.toSorted();         // [3,5,9]
const replaced = scores.with(1, 42);      // [5,42,9]
const spliced  = scores.toSpliced(1, 1);  // remove index 1, returns new

console.log('scores', scores)
console.log('sorted', sorted)
console.log('replaced', replaced)
console.log('spliced', spliced)