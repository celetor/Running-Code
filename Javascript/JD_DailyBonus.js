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

async function start() {
  if (!KEY) {
    console.log('请填写 key 后在继续')
    return
  }
  // 下载最新代码
  await downFile();
  console.log(`${new Date(new Date().getTime()+8*60*60*1000).toLocaleString()} 下载代码完毕`)
  // 替换变量
  await changeFile();
  console.log(`${new Date(new Date().getTime()+8*60*60*1000).toLocaleString()} 替换变量完毕`)
  // 执行
  console.log(`${new Date(new Date().getTime()+8*60*60*1000).toLocaleString()} 开始执行脚本`)
  await exec("node JD_DailyBonus.js >> result.txt");
  console.log(`${new Date(new Date().getTime()+8*60*60*1000).toLocaleString()} 脚本执行完毕`)

  // 读取执行结果
  const path = "./result.txt";
  let content = "";
  if (fs.existsSync(path)) {
    content = fs.readFileSync(path, "utf8");
  }
  
  //console.log("" + ` ${res2} ` + ` ${res} ` + new Date().toLocaleDateString(), content);
  console.log(`${new Date(new Date().getTime()+8*60*60*1000).toLocaleString()} 签到结果：\n${content}`);

  if (serverJ) {
    let t = content.match(/【签到概览】:((.|\n)*)【签到总计】/)
    let res = t ? t[1].replace(/\n/,'') : '失败'
    let t2 = content.match(/【签到总计】:((.|\n)*)【账号总计】/)
    let res2 = t2 ? t2[1].replace(/\n/,'') : '总计0'
    await sendNotify("" + ` ${res2} ` + ` ${res} ` + new Date().toLocaleDateString(), content);
  }
}

start()
