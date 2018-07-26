//这个client server是隔在client和backend中间的, client只能看见这个client server, 而后面的后端都看不到
var jayson = require('jayson');

// create a client, 向4040的server发送请求
var client = jayson.client.http({
    port: 4040,
    hostname: 'localhost'
});

// use the example on jayson website

function add (a, b, callback) {
    client.request('add', [a, b], function(err, response) {  //sending post request to backend server
        if(err) throw err;
        console.log(response.result); // 2
        callback(response.result);
    });
}


function getNewsSummariesForUser(user_id, page_num, callback) {
    client.request('getNewsSummariesForUser', [user_id, page_num], function(err, response) {
        if(err) throw err;
        console.log(response.result);
        callback(response.result);
    });
}

function logNewsClickForUser(user_id, news_id){//没有callback因为我们client约定了不作任何处理
    client.request('logNewsClickForUser', [user_id, news_id], function(err, response) {
        if (err) throw err;
        console.log(response);
    })
}
module.exports = {
    add : add,
    getNewsSummariesForUser : getNewsSummariesForUser,
    logNewsClickForUser : logNewsClickForUser
}