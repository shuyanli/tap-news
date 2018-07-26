const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;

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

    const newUser = new User(userData);  //因为sign up所以要创建新客户
    newUser.save( (err)=>{   //因为定义schema说了user 要unique, 所以我们强行存, 如果不unique就会报错,否则就存进去了(简单粗暴)
        console.log('saving new user');
        if (err) {
            return done(err);
        }

        return done(null);

    });

});
