//UI, children, loginpage包含了loginform
import './LoginForm.css';
import React from 'react';
//注意要用大括号因为源文件没有default
import {Link} from 'react-router-dom'

const LoginForm = ({  //下面这些就是prop
     onSubmit,
     onChange, //通过定义这个,既可以在儿子里改变它的值或者call它, 并且在父亲里面能通过<LoginForm>更新父亲的state, 实现从儿子到父亲的传递
     errors,
}) => (  //表达式就可以吧前面的return和大括号删掉: (obj)=>{return (表达式)} 等价于:  (obj)=>(表达式)
    <div className="container">
        <div className="card-panel login-panel">
            <form className="col s12" action="/" onSubmit={onSubmit}>
                <h4 className="center-align">Login</h4>
                {errors.summary && <div className="row"><p className="error-message">{errors.summary}</p></div>}
                <div className="row">
                    <div className="input-field col s12">
                        <input className="validate" id="email" type="email" name="email" onChange={onChange}/>
                        <label htmlFor='email'>Email</label>
                    </div>
                </div>
                {errors.email && <div className="row"><p className="error-message">{errors.email}</p></div>}
                <div className="row">
                    <div className="input-field col s12">
                        <input className="validate" id="password" type="password" name="password" onChange={onChange}/>
                        <label htmlFor='password'>Password</label>
                    </div>
                </div>
                {errors.password && <div className="row"><p className="error-message">{errors.password}</p></div>}
                <div className="row right-align">
                    <input type="submit" className="waves-effect waves-light btn indigo lighten-1" value='Log in'/>
                </div>
                <div className="row">
                    <p className="right-align"> New to Tap News?  <Link to="/signup">Sign Up</Link></p>
                </div>
            </form>
        </div>
    </div>
);

export default LoginForm;


// ES5
//var multiply = function(x, y) { return x * y;
//}
// ES6
//var multiply = (x, y) => {return x * y;} // ES6 简写
//var multiply = (x, y) => x * y;