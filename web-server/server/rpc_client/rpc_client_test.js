var client = require('./rpc_client');

client.add(1,2, (res)=>{    //doubt this
    console.assert(res === 3);
});

client.getNewsSummariesForUser('user1', 1, (res)=>{
    console.assert(res != null)
});

client.logNewsClickForUser('test_user', 'test_news');