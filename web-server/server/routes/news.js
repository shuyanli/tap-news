var express = require('express');
var router = express.Router();
var rpc_client = require('../rpc_client/rpc_client');

/* GET news summary list. */
//url中, 问号表示问号后面的东西都是一个key-value的组合, 在这里指的是访问/, 并且给一些参数
//参数之间使用&分隔, 冒号后面的表示这个值是在req.params中的, 可以直接读
router.get('/userId=:userId&pageNum=:pageNum', function(req, res, next) {
    var user_id = req.params['userId'];  //不写var的会被自动default为var
    var page_num = req.params['pageNum'];

    rpc_client.getNewsSummariesForUser(user_id, page_num, function(response) {  //todo 试试如果改成arrow function会怎么样
       res.json(response)
    });
});

router.post( '/userId=:userId&newsId=:newsId', function(req, res, next) {
   var user_id = req.params['userId'];
   var news_id = req.params['newsId'];

   rpc_client.logNewsClickForUser(user_id, news_id); //前端不作处理,所以不需要返回值
   res.status(200)

});

module.exports = router;
