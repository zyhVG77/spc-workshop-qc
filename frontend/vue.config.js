module.exports = {
    // 输出目录
    assetsDir: 'static',
    // 基本路径
    // baseUrl: './',
    // 配置代理

    devServer: {
        proxy: {
            '^/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                secure:false,
                pathRewrite: {'^/api': '/api'},
                logLevel: 'debug'
            },
            'analysis_report_detail': {
                target: 'http://localhost:8000/analysis_report_detail',
                changeOrigin: true,
                secure: false,
                logLevel: 'debug'
            },
            '^/myapi': {
                target: 'http://localhost:8088',
                changeOrigin: true,
                secure:false,
                pathRewrite: {'^/myapi': '/myapi'},
                logLevel: 'debug'
            }
        }
    }
};