// version v0.0.2
// create by ruicky
// detail url: https://github.com/ruicky/jd_sign_bot

const exec = require('child_process').execSync;
const fs = require('fs');
const rp = require('request-promise');
const download = require('download');

// 公共变量
const KEY = process.env.JD_COOKIE;
const serverJ = process.env.PUSH_KEY;
const DualKey = process.env.JD_COOKIE_2;


async function downFile () {
    // const url = 'https://cdn.jsdelivr.net/gh/NobyDa/Script@master/JD-DailyBonus/JD_DailyBonus.js'
    const url = 'https://raw.githubusercontent.com/NobyDa/Script/master/JD-DailyBonus/JD_DailyBonus.js';
    await download(url, './');
}

async function changeFile () {
   let content = await fs.readFileSync('./JD_DailyBonus.js', 'utf8')
   content = content.replace(/var Key = ''/, `var Key = '${KEY}'`);
   if (DualKey) {
    content = content.replace(/var DualKey = ''/, `var DualKey = '${DualKey}'`);
   }
   await fs.writeFileSync( './JD_DailyBonus.js', content, 'utf8')
}

async function sendNotify (text,desp) {
  const options ={
    uri:  `https://sc.ftqq.com/${serverJ}.send`,
    form: { text, desp },
    json: true,
    method: 'POST'
  }
  await rp.post(options).then(res=>{
    console.log(res)
  }).catch((err)=>{
    console.log(err)
  })
}

function getTime() {
  let utc = (-8) - new Date().getTimezoneOffset() / 60;             //当地时间与东八区相差几小时
  let date = new Date(new Date().getTime() - utc * 60 * 60 * 1000); //东八区时间

  let year = date.getFullYear();
  let month = date.getMonth() + 1;
  month = month < 10 ? '0' + month : month;

  let day = date.getDate();
  day = day < 10 ? '0' + day : day;

  let h = date.getHours();
  h = h < 10 ? '0' + h : h;

  let m = date.getMinutes();
  m = m < 10 ? '0' + m : m;

  let s = date.getSeconds();
  s = s < 10 ? '0' + s : s;

  let ms = date.getMilliseconds();
  if (ms < 10) {
      ms = '00' + ms;
  }
  else if (ms < 100) {
      ms = '0' + ms;
  }

  return `[${year}-${month}-${day} ${h}:${m}:${s}.${ms}] `;
}

async function start() {
  if (!KEY) {
    console.log('请填写 key 后在继续')
    return
  }
  // 下载最新代码
  await downFile();
  console.log(`${getTime()} 下载代码完毕`)
  // 替换变量
  await changeFile();
  console.log(`${getTime()} 替换变量完毕`)
  // 执行
  console.log(`${getTime()} 开始执行脚本`)
  await exec("node JD_DailyBonus.js >> result.txt");
  console.log(`${getTime()} 脚本执行完毕`)

  // 读取执行结果
  const path = "./result.txt";
  let content = "";
  if (fs.existsSync(path)) {
    content = fs.readFileSync(path, "utf8");
  }
  
  //console.log("" + ` ${res2} ` + ` ${res} ` + new Date().toLocaleDateString(), content);
  console.log(`${getTime()} 签到结果：\n${content}`);
    
  if (serverJ) {
    let t = content.match(/【签到概览】:((.|\n)*)【签到总计】/)
    let res = t ? t[1].replace(/\n/,'') : '失败'
    let t2 = content.match(/【签到总计】:((.|\n)*)【账号总计】/)
    let res2 = t2 ? t2[1].replace(/\n/,'') : '总计0'
    await sendNotify(` ${res2}  ${res} ${getTime()}`, content);
  }
}

start()
