export const arrayToObj = (arr) => {
    return arr.reduce( (result, item) => {
        result[item.id] = item;
        return result;
    }, Object.create(null)) //watch out the empty {}, which is passed as "result"
};
