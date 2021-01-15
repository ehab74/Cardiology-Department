import Validations from './Validations';
export default class SignupValidations {
    constructor(email, password) {
        this.email = email;
        this.password = password;
    }
    checkValidations() {
        let errors = [];
        //email validations
        if (!Validations.checkEmail(this.email)) {
            errors['email'] = 'Invalid Email';
        }
        //password Validations
        if (!Validations.minLength(this.password, 6)) {
            errors['password'] = 'Password should be of 6 characters at least';
        }
        return errors;
    }
    static getErrorMessageFromCode(errorCode){
        switch(errorCode) {
            case 'EMAIL_EXISTS' :
                return 'Email already exists';
            case 'EMAIL_NOT_FOUND' :
                return 'Email Not Found';
            case 'INVALID_PASSWORD':
                return 'Invalid password';
            default:
                return 'unexpected error occured. Please try again';
        }
    }
}