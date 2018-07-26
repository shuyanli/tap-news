const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
const config = require('../config/config.json');

module.exports = new PassportLocalStrategy({  // requiredField: name_we_defined  todo 看看怎么调用这个的和怎么传参数的
    usernameField: 'email',
    passwordField: 'password',
    session: false,
    passReqToCallback: true
}, (req, email, password, done) => {
    const userData = {
        email: email.trim(),
        password: password
    };

    // find a user by email address
    return User.findOne({ email: userData.email }, (err, user) => {
        if (err) { return done(err); }

        if (!user) {
            const error = new Error('Incorrect email or password');
            error.name = 'IncorrectCredentialsError';

            return done(error);
        }

        // check if a hashed user's password is equal to a value saved in the database
        return user.comparePassword(userData.password, (err, isMatch) => {
            if (err) { return done(err); }

            if (!isMatch) {
                const error = new Error('Incorrect email or password');
                error.name = 'IncorrectCredentialsError';

                return done(error);
            }
            //验证通过,签发token
            const payload = {//确保独一无二
                sub: user._id
            };

            // create a token string
            const token = jwt.sign(payload, config.jwtSecret);

            return done(null, token, null);  //passport是一个middleware, done就是next, passport作者叫他done
        });
    });
});
