//schema for the MongoDB, 来自官网的例子
const bcrypt = require('bcrypt');
const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema({
    email: {
        type: String,
        index: { unique:true }
    },
    password: String,
});


//this.password is the hashed password stored in the db
UserSchema.methods.comparePassword = function comparePassword(password, callback){
    bcrypt.compare(password, this.password, callback)
};

//注意这里不能用arrow function, 否则拿不到this, 详细:
//https://stackoverflow.com/questions/36957440/mongoose-pre-post-midleware-cant-access-this-instance-using-es6
UserSchema.pre('save', function saveHook(next) { //这个方程是往数据库里存,先用一些pre middleware做一些预处理,然后执行method:'save'
    const user = this;  //得到当前pymongo的context
    if(!user.isModified('password')) {  //todo 这句的逻辑不太明白, 后面都懂
        return next();  //目前觉得这句话的意思是第一次存入密码(好像有不太对)
    }

    return bcrypt.genSalt((saltError, salt)=>{
        if (saltError){
            return next(saltError);
        }

        return bcrypt.hash(user.password, salt, function(hashErr, hash) { //todo 这里不加return会怎么样(参照下面网址)
            // Store hash in your password DB.
            //http://codetheory.in/using-the-node-js-bcrypt-module-to-hash-and-safely-store-passwords/
            if (hashErr) {
                next(hashErr);
            }
            user.password = hash;
            return next();
        });
    })


});
//创建一个叫User的schema

//todo 这里User不一定能用, 改成userrecord试试
const User = mongoose.model('User', UserSchema);
module.exports = {
    User
}
//module.exports = mongoose.model('User', UserSchema);