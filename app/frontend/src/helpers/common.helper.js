export const arrayToObj = (arr) => {
    return arr.reduce( (result, item) => {
        result[item.id] = item;
        return result;
    }, Object.create(null)) //watch out the empty {}, which is passed as "result"
};

export const localizeTime = (DateTime) => {
    const date = new Date(DateTime);
    const offset = date.getTimezoneOffset();
    return new Date(date.getTime() - offset*60*1000);
};
