import {isAdmin} from '../helpers/auth.helper';

export const adminOnly = (target, propertyKey, descriptor) => {
    if (isAdmin(target.user)) {
        return descriptor;
    } else {
        throw `User ${name} has no corresponding rights to complete this request`;
    }
};