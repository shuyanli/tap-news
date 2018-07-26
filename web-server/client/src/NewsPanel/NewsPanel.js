import React from 'react';
import './NewsPanel.css';
import NewsCard from '../NewsCard/NewsCard';
import _ from 'lodash';
import Auth from "../Auth/Auth";

class NewsPanel extends React.Component {
    constructor() {
        super();
        this.state = {
            news:null,
            pageNum:1,
            loadAllNews:false
        }
    }

    componentDidMount () {
        this.loadMoreNews();
        this.loadMoreNews = _.debounce(this.loadMoreNews, 1000);//way to use debounce
        window.addEventListener('scroll', () => this.handleScroll());
    }
    handleScroll() {
        let scrollY = window.scrollY || window.pageYOffset || document.documentElement.scrollTop;
        if ((window.innerHeight + scrollY) >= (document.body.offsetHeight - 50 )) {
            console.log('requesting more news when reaching end.');
            this.loadMoreNews();
        }
    }

    //bearer是一种验证方式,在本project中没有实际意义因为是自产自销的, 如果和别的网站合作的话, 需要匹配这个bearer接口
    //注意bearer后面有个空格 :    Authorization: ' Bearer <Token>'
    loadMoreNews () {
        console.log('Actually triggered loading more news');
        if (this.state.loadAllNews) {
            return;
        }
        const news_url = 'http://' + window.location.hostname +
            ':3000/news/userId=' + Auth.getEmail() + '&pageNum=' + this.state.pageNum;

        const request = new Request(encodeURI(news_url), { //避免useremail重奇怪字符对params的干扰
            method: 'GET',
            headers: {
                'Authorization': 'bearer ' + Auth.getToken(),
            }
        });

        fetch(request)
            .then(res => res.json())
            .then(news => {
                if (!news || news.length === 0) {
                    this.setState({loadAllNews:true})
                }
                this.setState({
                    news: this.state.news? this.state.news.concat(news) : news,
                    pageNum: this.state.pageNum + 1
                });
            });
    }



    renderNews () { //todo 这个地方有点奇怪为什么要再包裹一层,需要看一下实战课文档有没有解释
        const news_list = this.state.news.map(news=>{
            return (  //将news传进newscard, newscard就可以调用news的各种state, 如url, title等
                <a className='list-group-item' href='#'>
                    <NewsCard news={news} />
                </a>
            )
        });

        return ( //todo 老师上课说这个是group list变成一个group, 变成一个collaction存起来
            <div className='container-fluid'>
                <div className='list-group'>
                    {news_list}
                </div>
            </div>
        )

    }
    render () { //主函数,initialize以后先call这个函数
       if (this.state.news) {
           return(
              <div>
                  {this.renderNews()}
              </div>
           )
       } else{
            return (
                <div id= 'msg-app-loading'>
                    loading......
                </div>
            )
       }
    }
}

export default NewsPanel