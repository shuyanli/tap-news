//真正实现逻辑的部分, parent

import React from 'react';
import LoginForm from './LoginForm';
import Auth from '../Auth/Auth'

class LoginPage extends React.Component {
    constructor () {
        super();

        this.state = {
            errors:{}
            ,
            user: {
                email: '',
                password: ''
            }

        };
    }


    changeUser (event) { //UI中任何输入的变化都会改变state的值, event.target是web api, mozella支持的,
                        // 这个event是由浏览器生成的, 如果我们不去处理,就会做一些浏览器默认的事件
        const field = event.target.name;  //直接通过这个api得到loginform里这个事件的name, 在这里是17行html的name和24行的password
        const user = this.state.user;
        user[field] = event.target.value; //同时替换两个值

        this.setState({user});
    }
    processForm(event) {
        event.preventDefault();//这一行不加会导致一提交整个页面刷新, 下面这个值一闪而过看不见
        const email = this.state.user.email;
        const password = this.state.user.password;

        console.log('email is: ' + email);
        console.log('password is: ' + password);


        //actually sending data from here
        const url = 'http://'+ window.location.hostname+ ':3000/auth/login';
        const request = new Request(
            url,
            {
                method:'POST',
                headers:{
                    'Accept' : 'application/json',
                    'Content-Type' : 'application/json'
                },
                body: JSON.stringify({
                    email: this.state.user.email, //todo 不可以用前面那个email吗?试一试
                    password: this.state.user.password
                })

            });
        fetch(request).then(response => { //response and status supported by mozella
            if (response.status === 200) {
                this.setState({
                    errors: {}  //if passed, clear the possible errors
                });

                response.json().then(json=>{
                    console.log(json);
                    Auth.authenticateUser(json.token, email);
                    window.location.replace('/');
                });
            } else {
                console.log('log in fail!');  //todo 这里的错误传递好器官,运行起来以后要看这个错误时怎么传回去的
                response.json().then (json =>{
                    const errors = json.errors? json.errors: {};
                    errors.summary = json.message;
                    this.setState({errors});  //todo 新的问题.这里怎么把error set好的
                                                //目前猜想,这个是简写 errors : errors, 将每个error feild都赋值了
                                                //对的, 名字相同可以只写一个
                })
            }
            /*回答上面那个todo问题,错误传递:
            我们和后端约好,他会给我们传回来这么一个东西:
            {
             'token' : 'adsuroidjr',
             'errors' : 'this is the error',
             'message' : 'blablabla'
            }
             */

        })
    }

    render(){
        return (  //通过这里将这三个值传给儿子
            <LoginForm
                onSubmit = {(e)=>this.processForm(e)}
                onChange = {(e)=>this.changeUser(e)}
                errors= {this.state.errors}
            />
        )
    }

}

export default LoginPage;
//这里的使用读这个帖子,说的和明白:
//https://stackoverflow.com/questions/27991366/what-is-the-difference-between-state-and-props-in-react