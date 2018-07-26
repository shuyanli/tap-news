var bodyParser = require('body-parser');
var cors = require('cors');
//连接databse:
//第一次见这么用的, 记一下
var config = require('./config/config');
var express = require('express');
var path = require('path');
var passport = require('passport');

//router
var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');

var app = express();
app.use(bodyParser.json());

require('./models/main').connect(config.mongoDbUri);
var authChecker = require('./middleware/auth_checker');

// TODO: remove this after development is done (允许开发阶段的跨域)
app.use(cors());

//passport init
app.use(passport.initialize());
passport.use('local-signup', require('./passport/signup_passport'));
passport.use('local-login', require('./passport/login_passport'));


// view engine setup
//build 是用了npm run build产生的压缩过的所有源文件, 用于发送给用户
app.set('views', path.join(__dirname, '../client/build'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static')));//静态文件请去client里面拿


//todo important
//react的机制是dynamic routing. 所以里面有预先定好许多分支, 每一次运行时先全部load,然后根据条件选择怎么走
//所以即使我们访问不同的页面,也不是每一次都从头到尾走, 而是根据当前的情况判断走哪一个分支
//这也解释了下面use authchecker以后authchecker的next去了哪里,在react内部其实知道应该去哪里,用了use很多东西上层是看不到的
app.use('/', index);
app.use('/auth', auth);
app.use('/news', authChecker);  //先过我的看门狗,如果通过, 回到33行继续loadnews, 注意顺序
app.use('/news', news);


// catch 404 and forward to error handler
app.use(function(req, res, next) {
    res.status(404);
});

module.exports = app;


