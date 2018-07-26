import mongodb_client as client


def test_basic():
    #db=client.get_db('test')  #这两句是等价的
    db=client.get_db()['test']
    db.test.drop()

    assert db.test.count() == 0

    db.test.insert_one({'test': 1})
    assert db.test.count() == 1

    db.test.drop()
    assert db.test.count() == 0

    print('test basic pass')


#如果在terminal直接被调用, 而不是被其他文件import时
if __name__ == "__main__":
    test_basic()