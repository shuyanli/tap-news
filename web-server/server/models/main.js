//connect to mongoose model
//第一个项目是在nodeserver主程序server.js中, 使用mongoose.connect('malb中的url') 来连接的
//这里换一种连接方法,不在主函数主连接

const mongoose = require('mongoose');

module.exports.connect = (uri) => {  //todo 这是一种便捷的定义方式?
    mongoose.connect(uri, { useNewUrlParser: true });
    //注意,这里没有用if fail 而是注册了一个method 'error'
    mongoose.connection.on('error', (err) => {
        console.error(`Mongoose connection error: $(err)`);
        process.exit(1);
    });

    // load models.
    require('./user');
}


