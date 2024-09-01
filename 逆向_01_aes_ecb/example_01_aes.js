const CryptoJS = require('crypto-js');
var hh = 'http://ggzy.zwfwb.tj.gov.cn:80/jyxxcggg/1157403.jhtml'
// function req(hh){
var aa = hh.split("/");
var aaa = aa.length;
var bbb = aa[aaa - 1].split('.');
var ccc = bbb[0];
var cccc = bbb[1];
var r = /^\+?[1-9][0-9]*$/;
var s = 'qnbyzzwmdgghmcnm'
if (r.test(ccc) && cccc.indexOf('jhtml') != -1) {
    var srcs = CryptoJS.enc.Utf8.parse(ccc);
    var k = CryptoJS.enc.Utf8.parse(s);
    var en = CryptoJS.AES.encrypt(srcs, k, {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });
    var ddd = en.toString();
    ddd = ddd.replace(/\//g, "^");
    ddd = ddd.substring(0, ddd.length - 2);
    var bbbb = ddd + '.' + bbb[1];
    aa[aaa - 1] = bbbb;
    var uuu = '';
    for (i = 0; i < aaa; i++) {
        uuu += aa[i] + '/'
    }
    uuu = uuu.substring(0, uuu.length - 1);
}
    // // console.log("uuu",uuu)
    // return uuu}
//
//
// console.log(req('http://ggzy.zwfwb.tj.gov.cn:80/jyxxcggg/1157403.jhtml'))
console.log(srcs)
// { words: [ 825308471, 875574016 ], sigBytes: 7 }
console.log(CryptoJS.enc.Utf8.stringify(srcs))     // 解密srcs  1157403

console.log(CryptoJS.lib.WordArray.create([ 825308471, 875574016 ]).toString(CryptoJS.enc.Utf8))    // 解密srcs  1157403
// ==============================================================================
console.log("url:", 'http://ggzy.zwfwb.tj.gov.cn:80/jyxxcggg/1157403.jhtml');
function req(hh) {
    // 第一步：分割 URL
    var aa = hh.split("/");
    console.log("Step 1: 分割后的数组 (aa):", aa);

    // 第二步：获取数组长度
    var aaa = aa.length;
    console.log("Step 2: 数组长度 (aaa):", aaa);

    // 第三步：提取最后一个部分（文件名部分）
    var bbb = aa[aaa - 1].split('.');
    var ccc = bbb[0];  // 数字部分
    var cccc = bbb[1]; // 文件扩展名部分
    console.log("Step 3: 文件名分割结果 (bbb):", bbb);
    console.log("Step 3: 数字部分 (ccc):", ccc, "扩展名部分 (cccc):", cccc);

    // 正则表达式匹配正整数
    var r = /^\+?[1-9][0-9]*$/;
    var s = 'qnbyzzwmdgghmcnm';
    console.log("Step 3: 正则表达式 (r):", r);
    console.log("Step 3: 密钥 (s):", s);

    // 第四步：条件检查
    if (r.test(ccc) && cccc.indexOf('jhtml') != -1) {
        console.log("Step 4: 条件满足，进行加密操作");

        // 加密操作
        var srcs = CryptoJS.enc.Utf8.parse(ccc);
        var k = CryptoJS.enc.Utf8.parse(s);
        var en = CryptoJS.AES.encrypt(srcs, k, {
            mode: CryptoJS.mode.ECB,
            padding: CryptoJS.pad.Pkcs7
        });
        var ddd = en.toString();
        console.log("Step 4: 原始数字 (srcs):", srcs);
        console.log("Step 4: 加密密钥 (k):", k);
        console.log("Step 4: 加密后的结果 (ddd):", ddd);

        // 替换字符并截断
        ddd = ddd.replace(/\//g, "^");
        ddd = ddd.substring(0, ddd.length - 2);
        console.log("Step 4: 加密结果替换字符后的结果 (ddd):", ddd);

        // 第五步：替换原文件名部分
        var bbbb = ddd + '.' + bbb[1];
        aa[aaa - 1] = bbbb;
        console.log("Step 5: 替换后的文件名部分 (bbbb):", bbbb);
        console.log("Step 5: 替换后的数组 (aa):", aa);

        // 第六步：重组 URL
        var uuu = '';
        for (i = 0; i < aaa; i++) {
            uuu += aa[i] + '/'
        }
        uuu = uuu.substring(0, uuu.length - 1);
        console.log("Step 6: 最终的 URL (uuu):", uuu);

        // 返回最终结果
        return uuu;
    } else {
        console.log("Step 4: 条件不满足，返回原 URL (hh):", hh);
        return hh;
    }
}

// 示例调用
var hh = 'http://ggzy.zwfwb.tj.gov.cn:80/jyxxcggg/1157403.jhtml';
var result = req(hh);
console.log("最终结果 (result):", result);
