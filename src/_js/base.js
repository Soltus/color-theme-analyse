
class WebRequest extends React.Component {

    constructor() {
        super();
        this.state = {
            files: [''],
            infiles: [''],
            datetime: [''],
            costtime: ['']
        }
    }

    // get请求
    componentDidMount() {
        fetch("[[reportpath]]")
            .then(res => res.json())
            .then(data => {
                console.log(data)
                this.setState({
                    files: data.origin_list,
                    infiles: data.in_files,
                    datetime: data.date + ' ' + data.time,
                    costtime: data.cost_times
                })
            })
    }

    showthis() {
        let text = '报告时间' + this.state.datetime + '\n本次分析文件数量' + this.state.infiles + '\n本次处理耗时' + this.state.costtime;
        console.log(text);
        swal('处理概要', text);
    }

    render() {
        return (
            <div onClick={() => { this.showthis() }}>
                <hr />
                <h1>Directory listing</h1>
                {
                    this.state.files.map((element, index) => {
                        return (
                            <ul key={index}>
                                <h5>{index + 1}/{this.state.infiles}</h5>
                                <h4>{element}</h4>
                            </ul>
                        )
                    })
                }
            </div>
        )
    }
}

function renderview() {
    const element = (
        <div>
            <button onClick={() => { changeview() }}>切换模式</button>
        </div>
    );
    ReactDOM.render(element, document.getElementById('viewmode'));

}
var isDir = false;
function changeview() {
    if (isDir == true) {
        ReactDOM.render(<ImgShow />, document.getElementById('imgs'));
        isDir = false;
    }
    else {
        ReactDOM.render(<WebRequest />, document.getElementById('imgs'));
        isDir = true;
    }
    // document.documentElement.scrollTop = 0;  //ie下
    // document.body.scrollTop = 0;  //非ie
}

function listshow() {
    ReactDOM.render(<WebRequest />, document.getElementById('imgs'));
}

function tick() {
    const element = (
        <div>
            <h2>It is {new Date().toLocaleTimeString()}</h2>
        </div>
    );
    // highlight-next-line
    ReactDOM.render(element, document.getElementById('time'));
}

renderview();
setInterval(tick, 1000);
