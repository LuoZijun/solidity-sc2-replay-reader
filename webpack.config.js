var webpack = require("webpack");

module.exports = {
    entry: "./src/main.js",
    output: {
        filename: "bundle.min.js",
        path: __dirname + "/build"
    },
    // Enable sourcemaps for debugging webpack's output.
    devtool: "source-map",

    plugins: [
        new webpack.optimize.UglifyJsPlugin({minimize: true})
    ],

    resolve: {
        extensions: ['', '.js', '.jsx', '.json']
    },

    module: {
        loaders: [
            // All files with a '.ts' or '.tsx' extension will be handled by 'awesome-typescript-loader'.
            { test: /\.js|jsx$/, loaders: ['babel-loader'] },
            { test: /\.json$/, loader: "json-loader" }
        ],

        preLoaders: [
            // All output '.js' files will have any sourcemaps re-processed by 'source-map-loader'.
            { test: /\.js$/, loader: "source-map-loader" }
        ]
    },

    // When importing a module whose path matches one of the following, just
    // assume a corresponding global variable exists and use that instead.
    // This is important because it allows us to avoid bundling all of our
    // dependencies, which allows browsers to cache those libraries between builds.
    externals: {
        "react"    : "React",
        "react-dom": "ReactDOM",
        "antd"     : "antd",
        "web3"     : "Web3"
    },
};
