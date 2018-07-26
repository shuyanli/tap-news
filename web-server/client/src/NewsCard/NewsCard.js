import './NewsCard.css'
import React from 'react'
import Auth from '../Auth/Auth'

class NewsCard extends React.Component {

    redirectToUrl (url, event) {
        event.preventDefault();
        window.open(url, '_blank');  //新窗口中打开url
    }

    sendClickLog() {  //newspanel有上次写的例子
        const url = 'http://' + window.hostname.location + ':3000/news/'
            + 'userId=' + Auth.getEmail() + '&newsId' + this.props.news.digest;  //newsmonitor中已经把每一个news加上了digest成为id

        const request = new Request(
            encodeURI(url),
            {
                method: 'POST',
                headers: {
                    Authentication: 'bearer' + Auth.getToken()
                }
            });
        fetch(request); //干脆就不处理, 如果死了后端就不管他了, 这样不会暴露给前端我们后端的一些信息, 后端接到信息闷头干活就可以了
    }

    render() {
        return (
            <div className="news-container" onClick={(e) => this.redirectToUrl(this.props.news.url, e)}>
                <div className='card-panel z-depth-3'>
                    <div className="row">
                        <div className='col s4 fill'>
                            <img src={this.props.news.urlToImage} alt='news'/>
                        </div>
                        <div className="col s1"/>
                        <div className="col s7">
                            <div className="news-intro-col">
                                <div className="news-intro-panel">
                                    <h4>{this.props.news.title}</h4>
                                    <div className="news-description">
                                        <p>{this.props.news.description}</p>
                                        <div>
                                            {this.props.news.source != null && <div className='chip light-blue news-chip'>{this.props.news.source}</div>}
                                            {this.props.news.reason != null && <div className='chip light-green news-chip'>{this.props.news.reason}</div>}
                                            {this.props.news.time != null && <div className='chip amber news-chip'>{this.props.news.time}</div>}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}
//上面那个&& a && b意思是 if(a){b}

export default NewsCard;