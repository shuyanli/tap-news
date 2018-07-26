// this is not a component, its just a helper class, like a assistance service

//static function: Static method calls are made directly on the class and
//are not callable on instances of the class. Static methods are often used to create utility functions.
//for more info: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes/static
class Auth{
    static authenticateUser (token, email){
        localStorage.setItem('token', token);
        localStorage.setItem('email', email);
    }

    static isUserAuthenticated(){//todo 后面看怎么知道谁call了这个函数
        return localStorage.getItem('token') !== null;
    }

    static deauthenticateUser(){
        localStorage.removeItem('token');
        localStorage.removeItem('email');
    }

    static getToken(){
        return localStorage.getItem('token')
    }

    static getEmail(){
        return localStorage.getItem('email')
    }

}

export default Auth;