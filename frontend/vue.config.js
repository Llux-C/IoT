module.exports = {
    devServer:{
        open:true,
        port:8888,
        proxy: {  //配置跨域
          '/api': {
            //看一下你后端的端口
            target: 'http://localhost:5000',
            changOrigin: true,  //允许跨域
            pathRewrite: {
              '^/api': '' 
            }
          },
    },
    }
}