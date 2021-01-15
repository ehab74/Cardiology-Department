import axios from 'axios';
//import SignupValidations from '../../../services/SignupValidations';
import { LOADING_SPINNER_SHOW_MUTATION, LOGIN_ACTION, SET_USER_TOKEN_DATA_MUTATION, SIGNUP_ACTION } from '../../storeconstants';
export default {
    async [LOGIN_ACTION](context, payload){
        let postData = {
            ...payload.body,
            returnSecureToken: true,
        };
        let response = '';
        context.commit(LOADING_SPINNER_SHOW_MUTATION, true, {root: true});
        try {
            response = await axios.post(payload.url, 
                postData);
    } catch(err) {
        context.commit(LOADING_SPINNER_SHOW_MUTATION, false, {root:true});
        //let errorMessage = SignupValidations.getErrorMessageFromCode(err.response.data.error.errors[0].message);
        let errorMessage = err.response.data.message;
        throw errorMessage;
    }
    context.commit(LOADING_SPINNER_SHOW_MUTATION, false, {root: true});
    if (response.status === 200) {
        localStorage.setItem('token', response.data.access_token);
        console.log(localStorage.getItem('token'));
        context.commit(SET_USER_TOKEN_DATA_MUTATION, {
            email: response.data.email,
            token: response.data.idToken,
            expiresIn: response.data.expiresIn,
            refreshToken: response.data.refreshToken,
            userId: response.data.localId,
        });
    }

    },
    async [SIGNUP_ACTION](context, payload){
        let postData = {
            ...payload.body,
            returnSecureToken: true,
        };
        let response = '';
        context.commit(LOADING_SPINNER_SHOW_MUTATION, true, {root: true});
        try {
                response = await axios.post(payload.url, 
                    postData);
        } catch(err) {
            context.commit(LOADING_SPINNER_SHOW_MUTATION, false, {root:true});
            // let errorMessage = SignupValidations.getErrorMessageFromCode(err.response.data.error.errors[0].message);
            let errorMessage = err.response.data.message;
            throw errorMessage;
        }
        context.commit(LOADING_SPINNER_SHOW_MUTATION, false, {root: true});
        if (response.status === 200) {
            context.commit(SET_USER_TOKEN_DATA_MUTATION, {
                email: response.data.email,
                token: response.data.idToken,
                expiresIn: response.data.expiresIn,
                refreshToken: response.data.refreshToken,
                userId: response.data.localId,
            });
        }
    },
};