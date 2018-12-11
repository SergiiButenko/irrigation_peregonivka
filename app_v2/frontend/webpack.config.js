const webpack = require('webpack');
const HtmlWebPackPlugin = require('html-webpack-plugin');
module.exports = {
    entry: './src/index.js',
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: require.resolve('babel-loader'),
                    options: {
                        presets: [['@babel/preset-env', {
                            targets: {
                                browsers: 'last 2 versions',
                            },
                            modules: false
                        }], '@babel/preset-react'],
                        cacheDirectory: true,
                        plugins: ['react-hot-loader/babel'],
                    }
                }
            },
            {
                test: /\.html$/,
                use: [
                    {
                        loader: 'html-loader',
                        options: {minimize: true}
                    }
                ]
            },
            {
                test: /\.(css|scss)$/,
                use: [
                    {
                        loader: 'style-loader'
                    },
                    {
                        loader: 'css-loader'
                    },
                    {
                        loader: 'sass-loader'
                    }
                ]
            },
            {
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'url-loader?limit=10000&minetype=application/font-woff'
            },
            {
                test: /\.(jpg|png|gif|ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'file-loader'
            },
            {
                test: /\.txt$/,
                use: 'raw-loader'
            },
        ]
    },
    resolve: {
        extensions: ['*', '.js', '.jsx']
    },
    output: {
        path: __dirname + '/dist',
        publicPath: '/',
        filename: 'bundle.js'
    },
    // plugins: [
    //   new webpack.HotModuleReplacementPlugin()
    // ],
    plugins: [
        new HtmlWebPackPlugin({
            template: './src/index.html',
            filename: './index.html',
            // favicon: './public/favicon.png',
        })
    ],
    devServer: {
        contentBase: './dist',
        host: '0.0.0.0',
        port: 8008,
        hot: true
    }
};
