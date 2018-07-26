import React from 'react';
import SignUpForm from "./SignUpForm";


class SignUpPage extends React.Component {
    constructor(props) {
        super(props);

        // set the initial component state
        this.state = {
            errors: {},
            user: {
                email: '',
                password: '',
                confirm_password: ''
            }
        };
    }

    changeUser(event) {
        const field = event.target.name;
        const user = this.state.user;

        user[field] = event.target.value;
        this.setState (
            {user}
        );
        // this.setState({//todo: 试试这样行不行
        //     user: this.state.user
        // });

        const errors = this.state.errors;
        if (this.state.user.password !== this.state.user.confirm_password) {
            errors.password = "Password and Confirm Password don't match.";
        } else {
            errors.password = '';
        }

        this.setState({errors});
    }



    processForm (event) {
        // prevent default action. in this case, action is the form submission event
        event.preventDefault();
        const email = this.state.user.email;
        const password = this.state.user.password;
        const confirm_password = this.state.user.confirm_password;

        //todo
        console.log('email is: ' + email);
        console.log('password is: ' + password);
        console.log('confirm password is : ' + confirm_password);
        if (password !== confirm_password) {
            return;
        }

        //start processing data(post registration data)
        const url = 'http://' + window.location.hostname + ':3000/auth/signup';
        const request = new Request(
            url,
            {method:'POST', headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: this.state.user.email,//todo 不可以用前面那个user吗?试一试
                    password: this.state.user.password
                })
            });

        fetch(request).then(response => { //response and status supported by mozella
            console.log('response get!');
            if (response.status === 200) {
                this.setState({
                    errors: {}  //if passed, clear the possible errors
                });

                //change current url to /login, so need log in after sign up
                //所以签发token的所有动作都是在login完成的
                window.location.replace('/login')
            } else {
                console.log('log in fail!');  //todo 这里的错误传递好奇怪,运行起来以后要看这个错误时怎么传回去的
                response.json().then (json =>{
                    console.log(json);
                    const errors = json.errors? json.errors: {};
                    errors.summary = json.message;
                    console.log(this.state.errors);
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
        return (  //记住了下面html是没有逗号分隔的
            <SignUpForm
                onSubmit = {(e) => this.processForm(e)}s
                onChange = {(e) => this.changeUser(e)}
                errors = {this.state.errors}
            />
        )
    }

}

export default SignUpPage;